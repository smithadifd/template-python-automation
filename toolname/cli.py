"""Command line for toolname.

  toolname run          plan the actions; DRY-RUN by default (mutates nothing).
                        Pass --apply to actually perform them.

Dry-run is the default across every mutating subcommand — the tool prints the
plan and changes nothing unless you pass `--apply` (feed-condenser's proven
`--archive`/`--apply` pattern). Arm `--apply` only after eyeballing the dry-run
output. This convention is stated in `--help` so it's discoverable.
"""

from __future__ import annotations

import json

from .config import load_config
from .core import plan_actions


def main(argv: "list[str] | None" = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="toolname",
        description="toolname — a Python automation scaffold. "
        "Mutating commands DRY-RUN by default; pass --apply to make changes.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="plan actions; DRY-RUN unless --apply")
    p_run.add_argument("-c", "--config", default="config.yaml")
    p_run.add_argument(
        "--apply",
        action="store_true",
        help="actually perform the actions (default: dry-run, mutates nothing)",
    )

    args = parser.parse_args(argv)

    if args.cmd == "run":
        cfg = load_config(args.config)
        actions = plan_actions(cfg)
        dry = not args.apply
        result = {
            "dry_run": dry,
            "planned": actions,
            "applied": [] if dry else actions,
        }
        if not dry:
            # A real tool performs its side effects here, gated on --apply.
            pass
        print(json.dumps(result, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
