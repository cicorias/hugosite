---
title: "A Skeletal Streamlit App on Databricks: From Parquet to Approval Workflow"
date: 2026-05-05T09:00:00-04:00
draft: false
slug: "databricks-skeletal-streamlit-app"
tags: ["databricks", "streamlit", "unity-catalog", "python", "databricks-apps"]
summary: "A walkthrough of a skeletal Streamlit application running on Databricks Apps — covering its Makefile-driven setup, dual-auth strategy, layered data architecture with volumes, tables, materialized views, and SQL views, and the flexibility to run locally or deploy to the platform with a single command."
image: /images/databricks.jpg
---

![Databricks](/images/databricks.jpg)

The full source code is available at [github.com/cicorias/databricks-skeletal-streamlit-app](https://github.com/cicorias/databricks-skeletal-streamlit-app).

This post walks through the project, a proof-of-concept that lands parquet files in a Unity Catalog Volume, aggregates them through materialized views, and serves the results through a Streamlit app with a multi-step approval workflow. The project is deliberately skeletal — it provides enough structure to be immediately useful while staying thin enough to understand in one sitting. It demonstrates patterns documented in the [Databricks Apps developer guide](https://docs.databricks.com/gcp/en/dev-tools/databricks-apps/) and uses conventions aligned with the [Databricks AppKit](https://databricks.github.io/appkit/) library for building production-grade applications on the platform.

## Getting Running in One Line

The project prioritizes a frictionless first experience. After cloning the repository and having the Databricks CLI configured with a profile, the entire setup — from dependency installation through sample data generation, volume upload, SQL object creation, environment file generation, to a running local Streamlit server — collapses into a single command:

```bash
make install gen-data upload-data sql-setup env dev
```

Each target in that chain does one discrete thing. `install` runs `uv sync` to create the virtual environment. `gen-data` produces 24 months of synthetic sales parquet files plus pipeline audit JSON artifacts. `upload-data` creates the Unity Catalog volumes if they don't exist and pushes the generated files into them. `sql-setup` runs a templated DDL script that creates the Delta table, materialized views, workflow tables, seed data, and an audit view. `env` introspects the Databricks CLI profile to auto-detect the workspace host, fetch a fresh OAuth token, and resolve the first available SQL warehouse — writing everything into a `.env` file. Finally, `dev` launches Streamlit with `python-dotenv` loading those variables transparently.

The Makefile variables (`PROFILE`, `CATALOG`, `SCHEMA`, `SILVER_VOL`, `APP_NAME`, `APP_PORT`) all have defaults but accept overrides on the command line. Pointing the same codebase at a different workspace or catalog is a one-argument change:

```bash
make env PROFILE=staging CATALOG=prod SCHEMA=analytics
```

This approach eliminates the "read the README for twenty minutes before you can see anything" problem. A developer can have the app running against real data inside their Databricks workspace within minutes of cloning.

The Makefile is the best starting point for understanding what the project can do. Running `make help` prints every available target:

```text
  install        Install project dependencies into .venv
  dev            Run Streamlit locally (reads .env via python-dotenv)
  dev-run        Run with the true entry point app/run.py
  dev-fresh      Runs token, env, and dev in one command
  token          Print a fresh OAuth token for the dev profile
  gen-data       Generate sample parquet files AND silver audit JSON files
  env            Generate .env from the dev Databricks profile
  create-volume  Create the Unity Catalog volumes (raw_data + silver)
  upload-data    Upload parquet + silver files to Databricks Volumes
  sql-setup      Create tables, materialized views, and audit view
  refresh        Refresh materialized views (re-reads sales_raw)
  deploy         Deploy the Databricks App via DABs bundle
  deploy-cli     Deploy via plain CLI (no DABs/Terraform)
  deploy-code    Upload code + create/deploy app (no resource registration)
  deploy-perms   Emit SQL grants for the app service principal
  stop           Stop the Databricks App (saves compute cost)
  delete-app     Delete the Databricks App entirely
  clean-runtime  Tier 1: delete workflow submissions (keep tables)
  clean-data     Tier 2: drop all tables/views/files (keep app)
  clean-all      Tier 3: full teardown (app + volume + workspace files)
```

Each target is composable — chain them in a single `make` invocation or run them individually. The local development loop (`dev-fresh` → edit code → reload browser) and the full deploy cycle (`deploy` or `deploy-cli`) are both single-command operations.

The project uses [uv](https://docs.astral.sh/uv/) with `pyproject.toml` for dependency management locally. This aligns well with the Databricks Apps runtime, which natively supports `uv` — when the platform detects a `pyproject.toml` without a `requirements.txt`, it installs dependencies using `uv` automatically. This skeletal app does include an `app/requirements.txt` (mirroring the same dependencies from `pyproject.toml`), so the deployed app uses the traditional pip path. Removing that file and letting the platform pick up `pyproject.toml` directly is a one-line change for teams that want to consolidate on a single dependency manifest for both local development and production deployment.

## How Volumes, Tables, Materialized Views, and SQL Views Fit Together

The data architecture uses four distinct Unity Catalog object types, each chosen for a specific reason rather than a uniform "everything is a table" approach.

**Volumes** serve as the managed landing zone. The `raw_data` volume receives monthly parquet files — the bronze layer. A separate `silver` volume stores pipeline audit JSON artifacts organized in a `YYYY-MM/UNIT/job_timestamp/` hierarchy. Volumes give you governed, path-based storage inside Unity Catalog without requiring the data to be tabular. The Streamlit app reads the silver volume directly using the Databricks SDK's `files.list_directory_contents()` and `files.download()` APIs, treating it as a file system for audit artifacts that don't naturally fit a columnar schema.

**Delta tables** hold the ingested sales data (`sales_raw`) and the transactional workflow state (`workflow`, `workflow_steps`, `workflow_config`). The setup SQL ingests parquet from the volume using `read_files()`:

```sql
CREATE OR REPLACE TABLE dev.default.sales_raw AS
SELECT * FROM read_files(
  '/Volumes/dev/default/raw_data/sales/',
  format => 'parquet'
);
```

The workflow tables use Delta with Change Data Feed enabled on the primary `workflow` table, providing a built-in audit trail of every row mutation without additional CDC infrastructure.

**Materialized views** aggregate the raw sales data into two gold-layer datasets: `mv_monthly_summary` (revenue, orders, and refund totals by year/month/region/product) and `mv_rep_leaderboard` (ranked sales rep performance by month). The Streamlit app never queries `sales_raw` directly — every dashboard query hits a materialized view that contains pre-aggregated rows. On a Serverless SQL Warehouse with Photon, these queries return in under a second regardless of the raw data volume. A scheduled Databricks Workflow job (`sql/02_refresh_job.py`) refreshes both views on a cadence, so the app reads pre-computed results rather than scanning parquet on every page load.

**A SQL view** (`vw_workflow_audit`) provides a live join across the `workflow` and `workflow_steps` tables. Unlike the materialized views, this view is re-evaluated on every query, which is the correct choice for transactional data that changes on every approve or reject action. The audit log page always shows current state without waiting for a refresh cycle.

This layered design means batch analytics data is fast because it's pre-aggregated, while transactional workflow data is always current because it's read through a live view. The two concerns don't interfere with each other.

## Dual-Auth Strategy: Service Principal and On-Behalf-Of

The application maintains two separate SQL Warehouse connections with different trust boundaries — a pattern worth understanding because it's central to how Databricks Apps handle identity.

The `auth.py` module detects whether the code is running inside Databricks Apps (by checking for the `DATABRICKS_APP_NAME` environment variable) or locally. When deployed, the platform injects Service Principal credentials (`DATABRICKS_CLIENT_ID`, `DATABRICKS_CLIENT_SECRET`) and forwards the end-user's identity through `X-Forwarded-Email` and `X-Forwarded-Access-Token` headers. Locally, the code falls back to `DATABRICKS_TOKEN` from the `.env` file.

The `db.py` module builds on this to expose three functions:

```python
def query_df(sql_text, params=None) -> pd.DataFrame:
    """Read using the Service Principal (cached, shared)."""

def query_df_as_user(sql_text, params=None) -> pd.DataFrame:
    """Read on behalf of the end-user (OBO token, per-call)."""

def execute_as_sp(sql_text, params=None) -> None:
    """Write using the Service Principal."""
```

The SP connection is cached with `@st.cache_resource` because it's long-lived and shared across all user sessions. The user OBO connection is created per-call because the forwarded access token can go stale across Streamlit WebSocket reconnections. Writes always go through the Service Principal since it owns the workflow tables, but the real user's email is recorded in the row data for audit purposes.

This separation means you can configure `user_api_scopes: ["sql"]` in the app's resource configuration to have reads execute against the user's own Unity Catalog permissions — useful when row-level or column-level security policies need to apply to the logged-in user rather than the SP.

## Application Architecture: Five Pages, Three Modules

The Streamlit app is a single `app.py` file with five pages routed through a sidebar radio button, supported by three focused modules.

The **Dashboard** page reads exclusively from materialized views. It renders KPI cards, monthly revenue and order bar charts, a region-by-product pivot table, and a rep leaderboard — all parameterized by year, region, and product filters. The bottom of the page includes a "Submit Month for Approval" action that kicks off the workflow.

The **Review Queue** page is role-scoped. A sidebar dropdown selects the reviewer's role (manager, finance, director), and the queue shows only items waiting for that role's approval step. Each item displays a step trail with badge indicators (`⏳ pending`, `✅ approved`, `❌ rejected`), an inline data preview pulled from the materialized view, and approve/reject buttons with an optional comments field. The three-step flow — Manager → Finance → Director — is defined entirely in the `workflow_config` seed data, so changing the approval chain means updating three rows in a table rather than modifying application code.

The **Audit Log** page queries `vw_workflow_audit` — the live SQL view — and renders the full history of every workflow action, filterable by status.

The **Pipeline Lineage** page demonstrates Volume browsing. It provides a hierarchical drill-down (Reporting Period → Business Code → Job Run) into the silver volume, reads `sales-check.json` files, and renders them as styled HTML dashboards showing data-quality tick-and-tie checks across pipeline stages. This page uses the Databricks SDK's file APIs rather than SQL, showing that Volumes can serve as a first-class data source alongside tables.

The **Session Debug** page is a diagnostic tool that displays environment variables, request headers, decoded JWT tokens (both user OBO and SP), the current user's SCIM profile with group membership, and the app's declared Unity Catalog permissions. This page exists because authentication is the most common source of deployment issues with Databricks Apps, and having the token claims and header values visible in the UI eliminates guesswork.

The `workflow.py` module encapsulates the submit/approve/reject state machine. It reads the configurable step definitions from `workflow_config`, inserts workflow and step records on submission, and advances or terminates the workflow on each reviewer action. All reads go through `query_df` (SP) and all writes through `execute_as_sp`, with the reviewer's identity recorded in each row.

## Flexible Deployment: Bundles or CLI

The project supports two deployment paths. The first uses Databricks Asset Bundles (DABs) via `databricks.yml`, which defines the app as a bundle resource. Running `make deploy` executes `databricks bundle deploy`, registers the Unity Catalog table resources through a templated JSON file (`meta/app-resources.json.tpl`), and starts the app.

Because Databricks Apps are currently in preview, the DABs bundle format does not yet support declaring Unity Catalog **table** resource permissions that the app's Service Principal needs access to. The [bundle resource reference for `app.resources.uc_securable`](https://docs.databricks.com/gcp/en/dev-tools/bundles/resources#appresourcesuc_securable) only supports `securable_type: VOLUME` with `READ_VOLUME` and `WRITE_VOLUME` permissions — there is no way to declare `TABLE`-type securables (SELECT or MODIFY on tables, materialized views, or SQL views) through the bundle YAML. The `databricks bundle deploy` step handles the SQL warehouse resource defined in `databricks.yml`, but the table and view grants must be registered separately. The `make deploy` target works around this by running a second step after the bundle deploy: it renders `meta/app-resources.json.tpl` with the catalog, schema, and warehouse placeholders substituted via `sed`, then calls `databricks apps update` to push the full resource manifest including those table-level permissions. This two-phase approach — bundle deploy for the app definition, then `apps update` for UC table resources — is the current workaround until DABs extends `uc_securable` beyond volumes.

The template itself (`meta/app-resources.json.tpl`) declares every securable the SP needs in one place:

```json
{
  "user_api_scopes": ["sql"],
  "resources": [
    { "name": "sql-warehouse",       "sql_warehouse": { ... } },
    { "name": "mv-monthly-summary",  "uc_securable": { "permission": "SELECT" } },
    { "name": "mv-rep-leaderboard",  "uc_securable": { "permission": "SELECT" } },
    { "name": "workflow-table",      "uc_securable": { "permission": "MODIFY" } },
    { "name": "workflow-steps",      "uc_securable": { "permission": "MODIFY" } },
    { "name": "workflow-config",     "uc_securable": { "permission": "SELECT" } },
    { "name": "workflow-audit",      "uc_securable": { "permission": "SELECT" } },
    { "name": "silver-volume",       "uc_securable": { "permission": "WRITE_VOLUME" } }
  ]
}
```

The second path (`make deploy-cli`) uses the Databricks CLI directly — no bundle framework required. It stages the app source into a temp directory, uploads it to the user's workspace path with `databricks workspace import-dir`, creates the app if it doesn't exist, registers the same UC resources through the same template workaround, and deploys. This path exists for environments where DABs aren't available or where operators prefer imperative CLI commands over declarative bundle definitions.

Both paths produce the same result: a running Databricks App with its auto-provisioned Service Principal, configured warehouse access, and declared Unity Catalog permissions. A separate `make deploy-perms SP=<guid>` target emits the equivalent SQL GRANT statements for environments where the admin needs to apply permissions manually — a third fallback when neither the `apps update` resource registration nor the auto-grant mechanism triggers correctly.

## Where AppKit and the Databricks Apps Platform Fit

The [Databricks AppKit](https://databricks.github.io/appkit/) library provides higher-level abstractions for building applications on Databricks — including pre-built components for authentication flows, resource management, and workspace integration. This skeletal app implements many of the same patterns at a lower level (direct SDK calls, manual header parsing, explicit connection management), which makes it a useful reference for understanding what AppKit automates under the hood. Teams evaluating AppKit can compare its abstractions against the explicit implementations in this project to decide which level of control they need.

The [Databricks Apps documentation](https://docs.databricks.com/gcp/en/dev-tools/databricks-apps/) covers the platform mechanics that this project relies on: the `app.yaml` configuration format, environment variable injection, the reverse proxy that forwards user identity headers, Service Principal auto-provisioning, and the `databricks apps deploy` lifecycle. The app's `app.yaml` demonstrates `valueFrom` references that resolve named resources (like `sql-warehouse`) at deploy time rather than hardcoding warehouse IDs — a pattern the documentation recommends for portability across workspaces.

## Tiered Cleanup as a First-Class Concern

The Makefile includes three cleanup tiers that reflect a deliberate design choice: teardown should be as intentional as setup. `make clean-runtime` (Tier 1) deletes workflow submissions while preserving all tables and seed data — useful between demo runs. `make clean-data` (Tier 2) drops all tables, views, and uploaded files while keeping the volumes and app definition. `make clean-all` (Tier 3) removes everything: the app, the volumes, and the workspace source files. Each tier is idempotent — running it twice doesn't error. This graduated approach prevents the "I just wanted to reset the demo data but accidentally deleted the entire environment" scenario.

The skeletal structure here — volumes for file-based data, tables for transactional state, materialized views for analytics, live views for audit, and a Makefile that stitches it all together — provides a foundation that can be extended without rearchitecting. Swap the synthetic parquet generator for a real ETL pipeline, replace the sidebar role selector with actual Entra ID group claims, add more approval steps by inserting rows into `workflow_config`, or point the lineage viewer at a different volume path.

The repository also includes a `flaskapp/` directory containing a Flask backend with a React frontend, added to validate that Databricks Apps can host a full JavaScript UI alongside a Python backend — not just Streamlit. It has its own `Makefile` with a parallel set of targets tailored to the Flask + Vite toolchain:

```text
  install              Install Python (uv) + Node deps
  install-py           Install Python deps via uv (creates .venv)
  install-node         Install npm deps at the flaskapp/ root
  lock                 Regenerate uv.lock
  dev-backend          Run Flask locally on :8000 (loads .env)
  dev-frontend         Run Vite locally on :5173, proxy /api → localhost
  dev-frontend-remote  Run Vite locally, proxy /api → deployed app
  build-frontend       Build the React app to frontend/dist
  typecheck            Run TypeScript type-check only
  test                 Run backend pytest suite
  token                Print a fresh OAuth bearer token
  validate             Validate the DABs bundle
  deploy               Deploy via DABs (uploads + registers UC resources)
  deploy-perms         Emit SQL grants for the app SP
  run                  Re-run the deployed app
  stop                 Stop the deployed app
  clean                Remove local build artifacts
```

The Flask app does not duplicate the data setup. It depends on the root-level Makefile for creating volumes, uploading sample data, running the SQL DDL that creates tables, materialized views, and the audit view. A typical first-time setup runs the root targets first, then switches into `flaskapp/`:

```bash
# From the repo root — set up all Databricks objects
make gen-data upload-data sql-setup

# Then build and run the Flask + React app
cd flaskapp
make install dev-backend   # terminal 1
make dev-frontend          # terminal 2
```

This separation keeps the data layer as a shared foundation. Both the Streamlit app and the Flask app query the same materialized views and workflow tables — swapping the UI framework doesn't require re-provisioning anything in Unity Catalog.

The skeleton is the point.
