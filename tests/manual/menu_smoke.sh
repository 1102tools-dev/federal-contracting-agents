#!/usr/bin/env bash
# Launch-surface smoke for all five packaged agents in fresh Claude Code sessions.
#
# Each session runs with all four credential variables absent. The only MCP
# calls permitted before the menu or mode list are the local presence-only
# get_access_status operations required by the packaged workflow.
#
# Two assertion shapes, because the five skills are not uniform:
#
#   count N   The skill defines a numbered launch menu. Assert exactly N
#             numbered items. Applies to market-research-workflow (6),
#             govcon-growth-workflow (9), acquisition-policy-workflow (10).
#
#   terms ... The skill defines no menu and infers the mode from the request.
#             Assert every mode name is offered. Applies to the two agent-level
#             orchestrators, pre-award-workflow and other-transaction-workflow,
#             neither of which contains the word "menu" in its SKILL.md.
#
# Usage: bash tests/manual/menu_smoke.sh [outdir]
# Requires: the five agents installed from the marketplace under test.
# Set CLAUDE_BIN to exercise a specific CLI or Desktop-bundled runtime.

set -uo pipefail
OUT="${1:-/tmp/menu-smoke}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
mkdir -p "$OUT"
FAILED=0

ask() {
  local file="$1"
  local invocation="$2"
  env -u SAM_API_KEY -u BLS_API_KEY -u PERDIEM_API_KEY -u REGULATIONS_GOV_API_KEY \
    "$CLAUDE_BIN" -p "$invocation

Follow the workflow's startup data-access readiness contract with credentials
absent, then state the complete set of choices exactly as the skill defines
them. Do not perform research, retrieval, file operations, or any MCP operation
other than the required local get_access_status calls. Output the readiness
block, choices, and closing question." \
    --permission-mode bypassPermissions < /dev/null > "$file" 2>&1
}

check_readiness() {
  local label="$1"
  shift
  local file="$OUT/$label.txt"
  local missing=0
  local normalized
  local phrase
  normalized=$(tr -d '\140' < "$file")
  for phrase in "$@"; do
    if grep -Fqi "$phrase" <<<"$normalized"; then printf '    readiness found: %s\n' "$phrase"
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
  ask "$file" "$invocation"
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
  printf '=== %s (no menu by design, expect all modes offered)\n' "$label"
  ask "$file" "$invocation"
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

check_count market-research    "/market-research-agent:market-research-workflow"        6
check_count govcon-growth      "/govcon-growth-agent:govcon-growth-workflow"            9
check_count acquisition-policy "/acquisition-policy-agent:acquisition-policy-workflow" 10

check_terms pre-award "/pre-award-agent:pre-award-workflow" \
  'scope only' 'pricing only' 'end[ -]to[ -]end' 'revision'
check_terms other-transaction "/other-transaction-agent:other-transaction-workflow" \
  'project description only' 'cost analysis only' 'end[ -]to[ -]end' 'revision|recost'

check_readiness market-research 'Data access readiness' 'SAM_API_KEY is not configured'
check_readiness govcon-growth 'Data access readiness' 'SAM_API_KEY is not configured'
check_readiness pre-award 'Data access readiness' 'BLS_API_KEY is not configured' 'PERDIEM_API_KEY is not configured'
check_readiness other-transaction 'Data access readiness' 'BLS_API_KEY is not configured' 'PERDIEM_API_KEY is not configured'
check_readiness acquisition-policy 'Data access readiness' 'REGULATIONS_GOV_API_KEY is not configured'

printf '\n%s\n' "failures: $FAILED"
exit "$FAILED"
