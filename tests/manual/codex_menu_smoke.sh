#!/usr/bin/env bash
# Launch-surface smoke for all five packaged agents in fresh Codex CLI sessions.
#
# The maintained 1102tools-host profile owns the complete nine-server union so
# duplicate MCP declarations from five installed agents cannot drop operations.
# Every launch runs with credential variables absent and permits only the local
# presence-only readiness calls before the complete menu or mode list.
#
# Usage: bash tests/manual/codex_menu_smoke.sh [outdir]
# Requires: all five agents installed and ~/.codex/1102tools-host.config.toml.

set -uo pipefail
OUT="${1:-/tmp/codex-menu-smoke}"
PROFILE="${CODEX_1102TOOLS_PROFILE:-1102tools-host}"
FAILED=0
mkdir -p "$OUT"

ask() {
  local file="$1"
  local invocation="$2"
  env -u SAM_API_KEY -u BLS_API_KEY -u PERDIEM_API_KEY \
    -u GSA_API_KEY -u REGULATIONS_GOV_API_KEY \
    codex -a never exec --profile "$PROFILE" --ephemeral -C "$PWD" \
      -s read-only -c 'model_reasoning_effort="low"' --color never \
      -o "$file" "$invocation

Follow the workflow's startup data-access readiness contract with credentials
absent, then state the complete set of choices exactly as the skill defines
them. Do not perform research, retrieval, file operations, or any MCP operation
other than the required local get_access_status calls. Output the readiness
block, choices, and closing question." \
      </dev/null >"$file.log" 2>&1
}

check_readiness() {
  local label="$1"
  shift
  local file="$OUT/$label.txt"
  local missing=0
  local phrase
  for phrase in "$@"; do
    if grep -Fqi "$phrase" "$file"; then printf '    readiness found: %s\n' "$phrase"
    else printf '    READINESS MISSING: %s\n' "$phrase"; missing=$((missing+1)); fi
  done
  if [ "$missing" -ne 0 ]; then FAILED=$((FAILED+1)); fi
}

check_count() {
  local label="$1"
  local invocation="$2"
  local expected="$3"
  local file="$OUT/$label.txt"
  printf '=== %s (numbered menu, expect %s items)\n' "$label" "$expected"
  if ! ask "$file" "$invocation"; then
    printf '    RESULT: FAIL (Codex invocation failed; see %s.log)\n' "$file"
    FAILED=$((FAILED+1))
    return
  fi
  local count
  count=$(grep -cE '^[[:space:]]*(\*\*)?[0-9]+\.' "$file")
  printf '    numbered items: %s\n' "$count"
  if [ "$count" -eq "$expected" ]; then printf '    RESULT: PASS\n'
  else printf '    RESULT: FAIL (expected %s)\n' "$expected"; FAILED=$((FAILED+1)); fi
  printf '    transcript: %s\n' "$file"
}

check_terms() {
  local label="$1"
  local invocation="$2"
  shift 2
  local file="$OUT/$label.txt"
  printf '=== %s (expect all modes offered)\n' "$label"
  if ! ask "$file" "$invocation"; then
    printf '    RESULT: FAIL (Codex invocation failed; see %s.log)\n' "$file"
    FAILED=$((FAILED+1))
    return
  fi
  local missing=0
  local term
  for term in "$@"; do
    if grep -qiE "$term" "$file"; then printf '    found: %s\n' "$term"
    else printf '    MISSING: %s\n' "$term"; missing=$((missing+1)); fi
  done
  if [ "$missing" -eq 0 ]; then printf '    RESULT: PASS\n'
  else printf '    RESULT: FAIL (%s missing)\n' "$missing"; FAILED=$((FAILED+1)); fi
  printf '    transcript: %s\n' "$file"
}

check_count market-research '$market-research-workflow' 6
check_count govcon-growth '$govcon-growth-workflow' 9
check_count acquisition-policy '$acquisition-policy-workflow' 10

check_terms pre-award '$pre-award-workflow' \
  'scope only' 'pricing only' 'end[ -]to[ -]end' 'revision'
check_terms other-transaction '$other-transaction-workflow' \
  'project description only' 'cost analysis only' 'end[ -]to[ -]end' 'revision|recost'

check_readiness market-research 'Data access readiness' 'SAM_API_KEY is not configured'
check_readiness govcon-growth 'Data access readiness' 'SAM_API_KEY is not configured'
check_readiness pre-award 'Data access readiness' 'BLS_API_KEY is not configured' 'PERDIEM_API_KEY is not configured'
check_readiness other-transaction 'Data access readiness' 'BLS_API_KEY is not configured' 'PERDIEM_API_KEY is not configured'
check_readiness acquisition-policy 'Data access readiness' 'REGULATIONS_GOV_API_KEY is not configured'

printf '\n%s\n' "failures: $FAILED"
exit "$FAILED"
