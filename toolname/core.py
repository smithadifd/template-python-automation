"""Domain logic for the tool.

This scaffold ships one trivial, pure function so the CLI and tests have
something real to exercise. Replace `plan_actions` with your tool's actual work.
Keep the pure/planning part separate from the side-effecting part so the CLI can
show a dry-run plan without mutating anything (see cli.py).
"""

from __future__ import annotations

from .config import Config


def plan_actions(cfg: Config) -> list[str]:
    """Compute the list of actions the tool *would* take, without doing them.

    Pure and side-effect-free on purpose: the CLI prints this in dry-run mode,
    and only executes it under `--apply`. A real tool builds this from live
    state (files to move, records to update, …)."""
    return [f"process {item!r}" for item in cfg.items]
