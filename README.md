# template-python-automation

A GitHub **template** for Python automation / CLI projects. It scaffolds a
lint-and-test-green Python CLI with a standard set of conventions: pip/venv + `pyproject.toml`, ruff, pytest, a **dry-run-by-default / `--apply`
to mutate** CLI, committed `config.example.yaml` → gitignored `config.yaml` with
secrets via env only, a launchd plist + wrapper stub, and the portable-core
context files (AGENTS.md + thin CLAUDE.md shim + CLAUDE.local.md.example).

This is a scaffold, not a real tool: it ships one `run` subcommand and a handful
of tests so CI passes out of the box. Replace the placeholder logic with yours.

## Create a project from this template

```bash
gh repo create <name> --template smithadifd/template-python-automation --private
cd <name>
```

Then instantiate:

1. Rename the package dir `toolname/` and update the three references to it in
   `pyproject.toml` (`name`, `[project.scripts]`) and the CLI `prog=`.
2. Fill the `AGENTS.md` skeleton (all 10 sections) and replace `<PROJECT>` in
   `AGENTS.md` / `CLAUDE.md` / `CLAUDE.local.md.example`.
3. `cp config.example.yaml config.yaml` and edit for your machine.
4. Adjust `.python-version` if you need a different interpreter.
5. For scheduling, fill the `__PLACEHOLDER__` values in `launchd/` (label, paths,
   log dir, notify script) — the wrapper hardcodes nothing.

## Develop

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
ruff check .
ruff format --check .
pytest

toolname run            # dry-run: prints the plan, changes nothing
toolname run --apply    # actually acts (once you trust the dry-run)
```

## What's inside

| Path | Purpose |
|------|---------|
| `pyproject.toml` / `.python-version` | packaging + interpreter pin (3.13) |
| `toolname/` | package: `config.py`, `core.py` (pure), `cli.py` (argparse) |
| `tests/` | offline pytest + fixture |
| `config.example.yaml` | committed config template; `config.yaml` is gitignored |
| `launchd/` | plist template + run-wrapper stub (placeholders only) |
| `.github/workflows/ci.yml` | install → ruff check → ruff format --check → pytest |
| `.github/FUNDING.yml`, `dependabot.yml` | funding + dependency updates |
| `AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md.example` | portable-core context |
| `.claude/settings.json` | permission allowlist baseline (no secrets) |

## Conventions (see `AGENTS.md`)

- Dry-run is the default; `--apply` is the mutation gate.
- Secrets via env only — config files name the env var, never hold the value.
- `import toolname` stays stdlib-only; third-party imports go inside functions so
  tests are network-free.

MIT licensed.
