---
title: "A Spaghetti Study Aid for Databricks and Spark That Somehow Became a Platform"
date: 2026-06-23T16:30:00-04:00
slug: "databricks-study-aid-spaghetti"
draft: false
tags: ["databricks", "spark", "pyspark", "copilot", "mise", "developer-tools"]
summary: "I set out to write a few study notes for a Databricks interview and ended up with a four-part study platform: a notes vault, dual-track PySpark notebooks, a git-tracked HTML lesson runner, and a Copilot SDK chat app that answers questions grounded in the repo itself. Here is how the pieces fit, and where the spaghetti lives."
aliases:
  - /databricks-study-aid-spaghetti/
feature_image: "/images/2026/06/databricks-study-aid-spaghetti-hero.jpg"
---

I started with a single Markdown file of interview notes. What I have now is a repository ([cicorias/spark-databricks-study](https://github.com/cicorias/spark-databricks-study)) with nineteen cross-linked study notes, two parallel tracks of runnable PySpark notebooks, a self-paced lesson runner that tracks progress through git commits, and a local chat web app that answers questions about the repo by driving my already-authenticated GitHub Copilot CLI. None of this was planned. Each piece solved a friction I hit while studying, and the next piece solved a friction the previous one created. The result is useful and a little tangled, which is the honest state of most tools that grow from real use rather than a design doc.

This post walks through the four working parts, the single mechanism that holds them together, and the places where the seams show.

## The thing that actually holds it together is mise

Before the features, the glue. Every part of this repo is wired through [`mise`](https://mise.jdx.dev) tasks, and that decision is what kept four loosely related subprojects from drifting into four separate setup rituals. The `mise.toml` pins the toolchain to match Databricks Serverless Environment v4 (Python 3.12, JDK 17 via Temurin, PySpark 3.5.x) and adds Node LTS and pnpm for the web app. When you `cd` into the directory, mise installs and pins those tools, auto-creates a `uv`-managed `.venv`, loads a gitignored `.env`, and exports the PySpark environment variables that otherwise bite you on WSL and macOS:

```toml
[tools]
python    = "3.12"
java      = "temurin-17"
uv        = "latest"
databricks-cli = "latest"
node = "lts"
pnpm = "latest"

[env]
_.python.venv = { path = ".venv", create = true }
_.file = ".env"
PYSPARK_PYTHON = "{{ config_root }}/.venv/bin/python"
PYSPARK_DRIVER_PYTHON = "{{ config_root }}/.venv/bin/python"
SPARK_LOCAL_IP = "127.0.0.1"
```

Pinning `PYSPARK_PYTHON` and `PYSPARK_DRIVER_PYTHON` to the same interpreter inside the venv removes the most common local PySpark failure, where the driver and the worker disagree about which Python they are running and the job dies with a cryptic version mismatch. Setting `SPARK_LOCAL_IP` to the loopback address sidesteps the "could not bind to local IP" startup error that WSL2 networking produces about half the time.

The tasks are the actual interface. `mise run smoke` builds a local `SparkSession` and prints the version to prove the toolchain works. `mise run db:import` pushes the Databricks notebooks into a Free Edition workspace through the CLI. `mise run teach:next` opens the next lesson. `mise run webapp` installs the Node dependencies and starts the chat server. Each subproject documents itself as a verb rather than a paragraph of setup instructions, and that uniformity is the only reason a reader can move between the four features without relearning how to start each one.

## The study vault: nineteen notes that link like a wiki

The oldest layer is a set of nineteen numbered Markdown files, written to be read either on GitHub or in [Obsidian](https://obsidian.md). They cover Spark mental models, an optimization playbook built around six concrete levers, a Delta Lake deep dive, a twelve-entry error playbook, SQL drills, and a self-assessment rubric you score yourself against after a dress rehearsal. Every cross-reference is a standard relative Markdown link, `[Spark Mental Models](03-Spark-Mental-Models.md)`, so the same files render correctly in a plain GitHub view and in Obsidian's graph without any conversion step.

That portability constraint shaped the content. Obsidian wikilinks (`[[03-Spark-Mental-Models]]`) would have been more ergonomic to write, but they break on GitHub, so the repo commits to relative links everywhere and documents the find-and-replace if you prefer wikilinks locally. The lesson here is mundane and worth stating: choosing the lowest-common-denominator link format cost a little authoring comfort and bought the notes a second rendering target for free.

## Two notebook tracks, including the ones that are broken on purpose

The notebooks live in two parallel directories because the two ways I study Spark have incompatible file formats. The `notebooks/databricks/` track uses `.py` files with `# COMMAND ----------` cell markers, the format the Databricks workspace importer understands. The `notebooks/local/` track uses [jupytext](https://jupytext.readthedocs.io) percent format, which opens directly in VS Code or converts to `.ipynb` with `mise run to-ipynb`. The same Spark concept gets a notebook in whichever track I happen to be working in that day.

The detail I am most fond of is that several notebooks are deliberately slow or broken. `03_optimization_challenge_start.py` is a running PySpark application with four to six real performance problems planted in it, paired with `04_optimization_challenge_solution.py`. The study method is to set a twenty-five minute timer, find the issues, fix them, and narrate why each fix matters before opening the solution. The `databricks-fde-prep/notebooks/` directory takes the same shape with `slow_spark_app_BROKEN.py` and `slow_spark_app_SOLUTION.py`. Writing a notebook that is wrong in instructive ways is harder than writing one that is right, because the bugs have to be realistic, independently fixable, and explainable in business terms rather than just "you forgot to broadcast." That constraint is what makes them good practice material.

## A lesson runner that stores progress in git

The third piece is a self-paced teaching system under `teach/`: nineteen rendered HTML lessons with in-browser quizzes, plus a small Python CLI (`scripts/teach.py`) exposed through `mise run teach:*` tasks. The interesting decision is where it keeps your progress. There is no database and no local state file. Completion is recorded as a committed Markdown "learning record," so the source of truth for "which lessons have I finished" is the git history itself.

That choice falls directly out of how I actually study, which is across several machines. Finishing a lesson writes a record and you commit it; picking up elsewhere is `git pull` followed by `mise run teach:status`. The status logic is deliberately simple. A lesson is complete when a learning record exists for it and no longer contains the string `in-progress`:

```python
def record_for(padded: str) -> Path | None:
    matches = sorted(RECORDS_DIR.glob(f"*-lesson-{padded}-*.md"))
    return matches[-1] if matches else None  # newest record wins

def is_complete(padded: str) -> bool:
    rec = record_for(padded)
    if rec is None:
        return False
    return "in-progress" not in rec.read_text()
```

Using "newest record wins" plus a substring check instead of structured front matter is exactly the kind of shortcut that reads as spaghetti, and it is. It also means progress sync is free, conflict-tolerant, and auditable, because it rides on a version control system I already trust and already run on every machine. The mess and the usefulness are the same line of code.

## A repo-grounded chat app built on the Copilot SDK

The newest and most experimental piece is `webapp/`, a local single-page chat UI that answers questions about this repository and cites the files it drew from. It is built on the [GitHub Copilot SDK](https://github.com/github/copilot-sdk), which means it drives the Copilot CLI I am already authenticated against. There is no separate API key and no vector database. The "retrieval" is the Copilot agent using its own read and search tools against the repo on disk.

![The Study Q&A web app answering a question about broadcast joins, with clickable file citations back to the source lesson and playbook](/images/2026/06/databricks-study-qa-webapp.png)

The server is a single `src/server.ts` Express file. It starts one `CopilotClient` pointed at the repository root through `workingDirectory`, then relays the agent's streaming output to the browser as Server-Sent Events. The part worth copying into your own projects is the permission handler. The SDK lets you intercept every action the agent wants to take, so making the assistant strictly read-only is a few lines:

```ts
function readOnlyPermissionHandler(
  request: PermissionRequest,
): PermissionRequestResult {
  switch (request.kind) {
    case "read":
    case "memory":
      return { kind: "approve-once" };
    default:
      return {
        kind: "reject",
        feedback: "This assistant is read-only; only reading repository files is permitted.",
      };
  }
}
```

Anything that is not a read or a memory operation gets rejected with feedback the agent can see, so it cannot write, delete, or run shell commands no matter what a question asks it to do. Grounding comes from a system prompt that tells the agent to answer only from repository files, to treat the HTML lesson pages as first-class sources alongside the Markdown, and to cite the specific file behind every answer.

Two integration details cost real debugging time and are the kind of thing you only learn by shipping. First, pnpm's isolated `node_modules` layout breaks the SDK's built-in lookup of its bundled CLI, so the server resolves the `copilot` binary explicitly off `PATH`, and the project needs `node-linker=hoisted` in `.npmrc` plus an `allowBuilds` entry in `pnpm-workspace.yaml` before the dependencies install and run. Second, the clickable citations are not magic. `GET /api/files` lists citable files via `git ls-files` filtered to documentation and code extensions, the browser linkifies any of those filenames that appear in an answer, and `POST /api/open` validates that the requested path stays inside the repository before handing it to the host's default opener:

```ts
const abs = resolve(REPO_ROOT, requested);
const rel = relative(REPO_ROOT, abs);
if (rel.startsWith("..") || rel.startsWith(sep) || resolve(REPO_ROOT, rel) !== abs) {
  res.status(403).json({ error: "path escapes repository" });
  return;
}
```

That confinement check is the one piece of this app I would not skip. The open endpoint runs a host program against a path the browser supplied, so rejecting anything that resolves outside the repo root is what keeps a convenience feature from becoming a path-traversal hole. The opener itself mirrors the same WSL2, macOS, and Linux logic the lesson runner uses, so a citation opens the same way whether you clicked it in the chat or reached it through `mise run teach:next`.

## Where the spaghetti is, and why it stays

The honest assessment is that the boundaries between these four parts are softer than they should be. The web app and the lesson runner both reimplement cross-platform file opening, once in TypeScript and once in Python, because neither was built to depend on the other. Progress tracking leans on a substring match rather than parsed metadata. The two notebook tracks duplicate concepts in two file formats. A clean rewrite would extract a shared "open this file on this host" utility, give the lesson records real schema, and pick one notebook format with generated variants.

I am not going to do that, and the reason is the point of the post. This repository is a study aid that I use, and every tangled seam in it marks a place where solving the actual problem mattered more than the architecture. The git-backed progress tracker exists because I study on three machines. The broken notebooks exist because reading a fix teaches less than producing one under a timer. The Copilot chat app exists because the fastest way to recall what the optimization playbook says is to ask it in plain English and click straight through to the source. `mise` ties it together because I refuse to remember four setup procedures. The spaghetti is the residue of a tool that grew from use, and the usefulness is worth the tangle.

If you are preparing for Spark or Databricks work, clone it, run `mise install && mise run setup && mise run smoke`, and start with `mise run teach:next`. If you are building any small agent-backed tool, the read-only permission handler and the path-confinement check are the two pieces I would lift first. They are small, they are correct, and they are the parts that keep a convenient toy from doing something you did not intend.
