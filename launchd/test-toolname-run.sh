#!/usr/bin/env bash
# Static checks for the inert wrapper template; no job is started.
set -euo pipefail

wrapper="${1:-$(dirname "$0")/toolname-run.sh}"
fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }

grep -Eq '^[[:space:]]*source[[:space:]]+"__LAUNCHD_KIT__/lib\.sh"' "$wrapper" || fail 'wrapper must source the placeholder launchd-kit lib.sh'
grep -Eq '^[[:space:]]*launchd_kit_init([[:space:]]|$)' "$wrapper" || fail 'wrapper must initialize launchd-kit'
awk '
  /^launchd_kit_init$/ { found = 1; if (getline && $0 == "lk_enable_crash_alert") valid = 1 }
  END { exit !(found && valid) }
' "$wrapper" || fail 'wrapper must register the crash alert immediately after launchd_kit_init'
grep -Eq '^[[:space:]]*lk_slot_guard[[:space:]]' "$wrapper" || fail 'wrapper must call lk_slot_guard'
grep -Eq '^[[:space:]]*lk_notify[[:space:]]' "$wrapper" || fail 'wrapper must call lk_notify directly'

if grep -Eq '(^|[[:space:];(|&])(mkdir|rmdir|flock|lockfile)[[:space:]]|curl[[:space:]].*(webhook|WEBHOOK)' "$wrapper"; then
  fail 'wrapper contains a hand-rolled lock or curl-to-webhook'
fi
grep -Eq '^[[:space:]]*lk_single_lock[[:space:]]' "$wrapper" || fail 'wrapper must call lk_single_lock'

bash -n "$wrapper" || fail 'wrapper has invalid bash syntax'
printf 'PASS: wrapper sources launchd-kit, calls lk_slot_guard and lk_notify, and has no hand-rolled lock or curl-to-webhook\n'
