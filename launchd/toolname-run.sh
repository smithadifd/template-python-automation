#!/usr/bin/env bash
# toolname-run.sh — scheduled-run wrapper STUB for launchd.
#
# This is a template. It HARDCODES NOTHING — every environment- or machine-
# specific value is a placeholder or comes from the environment. Fill the
# placeholders when you instantiate, and do NOT commit real paths, tokens, or
# webhook URLs into it (standards/security.md: no secrets in committed files;
# secrets come from the environment / a secrets helper the command reads at
# runtime, never inline).
#
# PHASE 3 NOTE: the slot-guard (single-run lock), log-dir rotation, and
# Discord-notify blocks below are hand-rolled PLACEHOLDERS. Phase 3 extracts a
# shared `launchd-kit/lib.sh`; this wrapper will then just `source` that lib and
# call its helpers (slot_guard / notify / etc.) instead of duplicating them.
# Until then, keep the shape but hardcode nothing.
set -uo pipefail

# --- environment (launchd gives a minimal env) --------------------------------
# PATH/HOME/TZ arrive from the plist's EnvironmentVariables; fall back sanely.
export PATH="${PATH:-/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin}"
export HOME="${HOME:?HOME must be set by the plist}"
export TZ="${TZ:-America/New_York}"

# --- paths (fill these in; do not commit real values) -------------------------
APP_DIR="__APP_DIR__"                 # absolute path to this clone
BIN="$APP_DIR/.venv/bin/toolname"     # the installed console script
LOG_DIR="__LOG_DIR__"                 # e.g. $HOME/.claude/logs/toolname
NOTIFY="__NOTIFY_SCRIPT__"            # e.g. $HOME/.claude/scripts/discord-notify.sh
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$(date +%Y-%m-%d_%H%M%S).log"

# --- slot guard (PLACEHOLDER; Phase 3 -> launchd-kit/lib.sh) -------------------
# macOS has no flock; mkdir is atomic. Steal a stale lock so a crashed run can't
# wedge the schedule forever.
LOCK="$LOG_DIR/.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  if [ -d "$LOCK" ] && [ "$(( $(date +%s) - $(stat -f %m "$LOCK") ))" -gt 1200 ]; then
    rmdir "$LOCK" 2>/dev/null || true
    mkdir "$LOCK" 2>/dev/null || exit 0
  else
    exit 0   # another run holds the lock — skip this tick
  fi
fi
trap 'rmdir "$LOCK" 2>/dev/null || true' EXIT

# --- notify (PLACEHOLDER; Phase 3 -> launchd-kit/lib.sh) ----------------------
# Success is silent; only failure pings Discord. The webhook URL is NOT here —
# the notify script reads it from the environment / a secrets file at runtime.
alert(){ [ -x "$NOTIFY" ] && tail -n 25 "$LOG" 2>/dev/null | "$NOTIFY" "$1" 15158332 || true; }

echo "=== toolname run $(date) (host $(hostname)) ===" >>"$LOG"
cd "$APP_DIR" || { echo "APP_DIR missing: $APP_DIR" >>"$LOG"; alert "toolname — bad dir"; exit 1; }

# --- the actual work ----------------------------------------------------------
# Run the tool. Add --apply here only once you trust the dry-run output.
if ! "$BIN" run -c config.yaml >>"$LOG" 2>&1; then
  echo "run FAILED" >>"$LOG"; alert "toolname — run failed"; exit 1
fi

echo "ok $(date)" >>"$LOG"
find "$LOG_DIR" -name '*.log' -mtime +30 -delete 2>/dev/null || true
