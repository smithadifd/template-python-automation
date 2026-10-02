# AGENTS.md — <PROJECT>

Canonical, tool-agnostic orientation for any AI coding agent or human working in
this repo (Claude Code, Codex, Cursor, Aider, …). Self-contained: you can run,
build, test, and navigate <PROJECT> from what's here. Human-facing overview is in
[`README.md`](README.md).

> Claude Code users: `CLAUDE.md` imports this file and adds Claude-only notes.
> Don't duplicate content from here into `CLAUDE.md`.
>
> This file is a SKELETON from `template-python-automation`. Fill each section,
> delete these guidance blockquotes, and rename `<PROJECT>` / `toolname`.

---

## 1. What <PROJECT> is

> Purpose in 2–3 sentences. Deployment posture (local CLI? launchd-scheduled on
> the Studio? one-shot?). Then the hard non-goals — the things this tool
> deliberately does NOT do, so an agent doesn't scope-creep into them.

## 2. Tech stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.13 (pinned in `.python-version`) |
| Packaging | pip + venv, `pyproject.toml` (setuptools) |
| Lint / format | ruff |
| Tests | pytest (`tests/`) |
| Config | `config.example.yaml` (committed) → `config.yaml` (gitignored) |
| Scheduling | launchd plist + wrapper (`launchd/`) |

## 3. Commands

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .[dev]          # editable install with dev tools
ruff check .                   # lint (matches CI)
ruff format --check .          # format check (matches CI)
pytest                         # tests — must stay green and network-free

toolname run                   # DRY-RUN: prints the plan, mutates nothing
toolname run --apply           # actually performs the actions  <-- hits live state
```

> Flag every command that touches a live service or mutates state (the `--apply`
> line above). Dry-run is the default everywhere; `--apply` is the safety gate.

## 4. Repo map

```text
toolname/
  __init__.py    package marker; keep import-time stdlib-only
  config.py      load_config() -> Config dataclass (yaml, lazy import)
  core.py        pure domain logic (plan_actions) — no side effects
  cli.py         argparse subcommands; dry-run default, --apply to mutate
tests/           pytest, offline, fixtures in tests/fixtures/
launchd/         plist template + run-wrapper stub (placeholders only)
config.example.yaml   committed config template (config.yaml is gitignored)
```

> Rename the package dir and update this map as the tool grows. One
> responsibility per module.

## 5. Architecture in brief

> The data flow in a few lines: input → the components that transform it →
> output. Name the seam an agent must not bypass (e.g. "all mutations go through
> cli.py's --apply gate"; "the pure planner in core.py has no I/O").

## 6. Database / storage

> If the tool has durable state (SQLite, a JSON store, files), name the schema
> source of truth and how it migrates. Delete this section if the tool is
> stateless.

## 7. Conventions

- `import toolname` (and every module) stays **stdlib-only at import time** — put
  third-party imports (yaml, HTTP libs, an LLM client) *inside* the functions
  that use them, so tests run with no network and no extra installs.
- **Dry-run is the default**; mutating actions are gated behind `--apply`. Never
  make a subcommand mutate by default.
- **Secrets via env only** — config files name the env var (`token_env`), never
  hold the value. See standards/security.md.
- Keep the pure/planning logic (core.py) separate from side effects (cli.py).
- ruff for lint + format; Conventional Commits.
- Ship documentation updates with the code changes they describe.

## 8. Critical gotchas

> The highest value-per-token section. Every incident that cost a session goes
> here, stated as a rule. Start it as you hit them; empty is fine at scaffold time.

## 9. Environment

> Env vars the tool reads and what each is for (e.g. `TOOLNAME_TOKEN` — API token).
> Where prod env lives (a secrets file / 1Password) — the LOCATION, never the
> values. The committed config names the env vars; nothing secret is committed.

## 10. Licensing / posture

> State the license (MIT default per standards/licensing.md) or, if deliberately
> unlicensed, say why (private repo, personal-use, all rights reserved). If the
> tool reads any ToS-fragile or personal-data source, document the posture here.
