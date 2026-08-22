#!/usr/bin/env bash
# Launch-surface smoke for all five packaged agents in fresh Claude Code sessions.
#
# Menus and mode lists make no MCP calls, so user-level MCP configuration cannot
# contaminate this check. Each agent is invoked explicitly in its own
# noninteractive session.
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

set -uo pipefail
OUT="${1:-/tmp/menu-smoke}"
mkdir -p "$OUT"
FAILED=0

ask() {
  local file="$1"
  local invocation="$2"
  claude -p "$invocation

State the complete set of choices this workflow offers, exactly as the skill
defines them. Do not perform any research, retrieval, MCP call, file operation,
or preflight. Output only those choices and the closing question." \
    --permission-mode bypassPermissions < /dev/null > "$file" 2>&1
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

printf '\n%s\n' "failures: $FAILED"
exit "$FAILED"
