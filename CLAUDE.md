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
