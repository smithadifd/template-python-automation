# CLAUDE.md — <PROJECT> (Claude Code)

@AGENTS.md

Everything about <PROJECT> — stack, commands, repo map, architecture,
conventions, and gotchas — lives in the imported [`AGENTS.md`](AGENTS.md). It is
tool-agnostic and self-contained; read it first. This file adds only the
Claude-Code-specific bits. Personal/session config lives in the gitignored
`CLAUDE.local.md` — read it first if it exists (deploy details, secrets
locations, session log).

## Notes for Claude

- Run a fresh-eyes review (`reviewer` agent or `/review`) on the diff before
  declaring work done; apply mechanical fixes silently, surface real questions.
- Doc updates (AGENTS.md, README) ship in the same PR as the code change.
- `toolname run --apply` hits live state — be deliberate, never loop it; prefer
  the dry-run default when verifying.
- Conventional Commits; never auto-push; confirm before destructive ops.

## End-of-session workflow

- Feature branch → Conventional Commit → push → PR (`gh pr create`) → wait for CI
  → squash-merge, delete branch → update `CLAUDE.local.md` session log (and
  AGENTS.md if durable facts changed) in the same PR as the code.
