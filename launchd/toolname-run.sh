#!/usr/bin/env bash
# Scheduled-run wrapper template. Replace every __PLACEHOLDER__ before use.
# Keep host paths and secrets out of committed files.
set -uo pipefail

export TOOL_NAME=toolname
APP_DIR="__APP_DIR__"
BIN="$APP_DIR/.venv/bin/toolname"
export LOG_DIR="__LOG_DIR__"
export NOTIFY_SCRIPT="__NOTIFY_SCRIPT__"

# shellcheck source=/dev/null
source "__LAUNCHD_KIT__/lib.sh" || exit 1
launchd_kit_init
lk_enable_crash_alert
lk_single_lock 20

# Set TOOL_SLOT to a launchd-kit window (for example, daily or slots:8,12,16,20)
# when scheduling a calendar job. The template plist uses StartInterval, so its
# default is to run on every tick, as before.
if [[ -n "${TOOL_SLOT:-}" ]]; then
  lk_slot_guard "$TOOL_SLOT"
fi

cd "$APP_DIR" || {
  lk_log "APP_DIR missing: $APP_DIR"
  exit 1
}

# Add --apply only after checking the dry-run output.
if ! "$BIN" run -c config.yaml >>"$LOG" 2>&1; then
  lk_log "run FAILED"
  exit 1
fi

lk_log "run complete"
if [[ "${TOOL_NOTIFY_ON_SUCCESS:-0}" == 1 ]]; then
  lk_notify "toolname — run complete" "$LK_COLOR_GREEN" <<<"Run complete. Log: $LOG"
fi
LOG_RETENTION_DAYS=30 lk_rotate_logs
