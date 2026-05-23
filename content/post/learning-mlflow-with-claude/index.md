---
title: "MLflow Learning Plan: Claude, Classic ML, GenAI, Local and Databricks"
date: 2026-05-23T16:50:00-04:00
slug: "learning-mlflow-with-claude"
draft: false
tags: ["mlflow", "databricks", "claude", "anthropic", "genai", "machine-learning", "python", "uv", "mise"]
summary: "A runnable MLflow sandbox covering classic ML and GenAI, identical code locally and on Databricks. Plan, notebooks, scripts, and tooling all scaffolded with Anthropic Claude in an afternoon."
feature_image: /images/2026/05/mlflow-databricks-hero.png
aliases:
  - /learning-mlflow-with-claude/
---

Repo: [github.com/cicorias/mlflow-learning-plan](https://github.com/cicorias/mlflow-learning-plan).

I went deep on MLflow because I like to understand the plumbing. Tracking, registry, projects, tracing, evaluation, judges, prompts. Locally and on Databricks. Same code.

The whole thing was scaffolded in an afternoon with [Anthropic Claude](https://claude.ai/): two learning plans, executable notebooks for every lesson, `mise` tasks, `uv` setup, local tracking server scripts, Databricks notebook format. Reviewed, ran, refined, committed.

## What's in it

- **`docs/start/mlflow-learning-plan-01.md`** - 4-week classic ML plan. Tracking, Models, Registry, Projects.
- **`docs/start/mlflow-learning-plan-02.md`** - GenAI plan for MLflow 3.x. Tracing, eval datasets, LLM-as-a-judge, human feedback, prompt registry, continuous eval.
- **`docs/01-classical-ml-background.md`** and **`02-generative-ai-background.md`** - background reading.
- **`notebooks/01-classical-ml/`** - `00-setup`, `01-foundations-setup`, `02-experiment-tracking`, `03-models-and-registry`, `04-projects-reproducibility`.
- **`notebooks/02-generative-ai/`** - `00-setup`, `01-tracing-observability`, `02-evaluation-datasets`, `03-llm-judges-scorers`, `04-human-feedback-prompts`, `05-continuous-evaluation`.
- **`scripts/`** - `setup.sh`, `env.sh`, `mlflow-server.sh`, `mlflow-stop.sh`, `verify.sh`, `run-classical.sh`, `run-genai.sh`, `clean.sh`.
- **`mise.toml`** - tools and tasks. **`pyproject.toml` + `uv.lock`** - deps pinned with `uv`.

Notebooks are `.py` files in Databricks notebook format. They run locally with `uv run python` and import cleanly as Databricks notebooks when synced to a Repo.

## First run

```bash
mise install               # Python, uv, Azure CLI, Databricks CLI
mise run setup             # uv sync + .env from template
mise run mlflow-server     # local tracking server on :5000
mise run verify            # smoke-test both tracks
```

Databricks auth is Azure CLI federated. No PATs:

```bash
az login
databricks auth login --host https://<your-workspace>.azuredatabricks.net
databricks current-user me
```

## One env var bridges local and Databricks

```python
import os, mlflow
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "databricks"))
mlflow.set_experiment("01-classical-ml-02-experiment-tracking")
```

Local: `MLFLOW_TRACKING_URI=http://localhost:5000`. Databricks: leave unset, the `"databricks"` default routes to the workspace runtime.

## Sample lesson: experiment tracking

```python
def train_and_log(C: float, max_iter: int, solver: str) -> str:
    with mlflow.start_run(run_name=f"lr-C{C}-{solver}") as run:
        mlflow.log_params({"C": C, "max_iter": max_iter, "solver": solver})
        mlflow.set_tag("dataset", "iris")

        model = LogisticRegression(C=C, max_iter=max_iter, solver=solver, random_state=42)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        mlflow.log_metrics({
            "accuracy": accuracy_score(y_test, preds),
            "f1_weighted": f1_score(y_test, preds, average="weighted"),
        })

        for fold, score in enumerate(cross_val_score(model, iris.data, iris.target, cv=5)):
            mlflow.log_metric("cv_accuracy", score, step=fold)

        return run.info.run_id
```

Same function runs against local SQLite-backed MLflow or against Databricks Managed MLflow without a code change.

## `mise.toml`

```toml
[tools]
python = "3.14"
uv = "latest"
azure-cli = "latest"
databricks-cli = { version = "latest", exe = "databricks" }

[tasks.sync]        ; run = "uv sync"
[tasks.env]         ; run = "./scripts/env.sh"
[tasks.setup]       ; depends = ["sync", "env"]
[tasks."mlflow-server"]
[tasks."mlflow-stop"]
[tasks.verify]
[tasks."run-classical"]
[tasks."run-genai"]
[tasks.clean]
```

(Real file has full `description` and `run` lines per task. See [`mise.toml`](https://github.com/cicorias/mlflow-learning-plan/blob/main/mise.toml).)

## On using Claude to build this

Pre-recorded courses optimize for the median learner and the curriculum that was current 6-18 months ago. They cannot adapt to my stack, my cloud, my package manager, or the parts I already know.

Claude can. The loop is:

1. State the goal: end-to-end MLflow, classic + GenAI, local + Databricks on Azure, no PATs, `uv` + `mise`.
2. Ask for the plans as Markdown with links to canonical docs.
3. Ask for the notebooks per lesson in Databricks notebook format.
4. Ask for the tooling layer: tasks, scripts, `.env`, verify.
5. Run, break it, ask follow-ups, refine, commit.

The artifacts are mine. In my GitHub. Re-runnable, extensible, shareable. That loop beats Udemy, Coursera, and most YouTube playlists for any developer who can drive a focused conversation. The bottleneck stopped being access to a good explanation a while ago. It is now willingness to ask the next question and run the next thing.

Clone it: `git clone https://github.com/cicorias/mlflow-learning-plan && cd mlflow-learning-plan && mise install && mise run setup`. Start with `docs/start/mlflow-learning-plan-01.md`.
