---
description: "Python tooling rules — use uv + venv exclusively"
applyTo: "**/*.py,**/pyproject.toml,**/requirements*.txt,**/uv.lock,**/.python-version"
---

# Python Tooling Rules

**Hard constraint:** All Python work in this workspace MUST use [`uv`](https://docs.astral.sh/uv/) for package and project management, and a local `.venv/` virtual environment for isolation. Do NOT use `pip`, `pipx`, `poetry`, `pipenv`, `conda`, `pyenv`, or system Python directly.

## Required commands

| Task | Command |
|---|---|
| Create venv | `uv venv` (creates `.venv/` using project's pinned Python) |
| Activate venv | `source .venv/bin/activate` (Linux/macOS/WSL) |
| Pin Python version | `uv python pin 3.12` |
| Add a dependency | `uv add <package>` |
| Add a dev dependency | `uv add --dev <package>` |
| Remove a dependency | `uv remove <package>` |
| Sync from lockfile | `uv sync` |
| Run a script/tool | `uv run <command>` (auto-uses `.venv`) |
| Run a one-off tool | `uvx <tool>` (ephemeral, like `pipx run`) |
| Install Python itself | `uv python install 3.12` |

## Rules for agents

1. **Never** invoke `pip install`, `python -m pip`, `pip3`, or `easy_install`. Use `uv add` / `uv pip install` instead.
2. **Never** create a venv with `python -m venv`. Use `uv venv`.
3. **Never** run scripts with bare `python script.py`. Use `uv run python script.py` so the project venv is guaranteed.
4. **Never** introduce `poetry`, `pipenv`, `conda`, or `requirements.txt` as the source of truth. Use `pyproject.toml` + `uv.lock`.
5. If `pyproject.toml` does not exist when adding Python code, initialize it with `uv init` (or `uv init --lib` for a library).
6. If a legacy `requirements.txt` is present, migrate with `uv add -r requirements.txt` and then remove the file.
7. Always commit `pyproject.toml` and `uv.lock`. Never commit `.venv/`.
8. When suggesting install commands in documentation or READMEs, show the `uv` form first.

## Rationale

`uv` is the project-wide standard because it is significantly faster than `pip`/`poetry`, resolves and locks deterministically, manages Python interpreters itself, and replaces the entire `pip` + `venv` + `pyenv` + `pipx` stack with a single tool.
