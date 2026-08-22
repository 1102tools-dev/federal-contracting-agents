#!/usr/bin/env bash
# Multi-agent coexistence, install-order, plugin-only reachability, and
# winner-promotion checks for Claude Code.
#
# Why this exists
# ---------------
# All five packages declare shared MCP server names (sam-gov, usaspending,
# gsa-calc, gsa-perdiem, bls-oews, tavily-web). Claude Code deduplicates by
# server name and the first declarer wins, so 17 declarations resolve to 10
# registrations and which plugin owns a shared name depends on install order.
#
# That is namespace attribution, not capability loss: the surviving instance is
# byte-identical, and every skill is written to match tools by server and
# semantic operation rather than by generated prefix. This harness proves that
# claim rather than assuming it, in both install orders.
#
# Contamination control
# ---------------------
# A developer machine's own user-level MCP servers can silently satisfy a call
# and make the test pass for the wrong reason. Two environment-level fixes were
# tried and rejected: a separate CLAUDE_CONFIG_DIR reports "Not logged in"
# because the OAuth credential resolves from the system keychain scoped to the
# default config directory, and --strict-mcp-config drops plugin-provided
# servers along with user ones, removing the thing under test.
#
# Control is therefore enforced by the assertion instead of the environment.
# A pass REQUIRES the invoked tool name to begin with mcp__plugin_, so a call
# satisfied by a user-level server yields mcp__<server>__ and fails. The test
# cannot pass for the wrong reason, which is the property that matters.
#
# Usage: bash tests/manual/coexistence.sh
# Requires: the marketplace under test added as "1102tools".

set -uo pipefail
MARKETPLACE=1102tools
FAILED=0

ORDER_A="market-research-agent pre-award-agent govcon-growth-agent other-transaction-agent acquisition-policy-agent"
ORDER_B="acquisition-policy-agent other-transaction-agent govcon-growth-agent pre-award-agent market-research-agent"

install_in_order() {
  local order="$1"
  local plugin
  for plugin in $ORDER_A; do claude plugin uninstall "$plugin@$MARKETPLACE" >/dev/null 2>&1; done
  rm -rf "$HOME/.claude/plugins/cache/$MARKETPLACE"
  for plugin in $order; do claude plugin install "$plugin@$MARKETPLACE" >/dev/null 2>&1; done
}

registered_count() {
  claude mcp list 2>/dev/null | grep -c '^plugin:'
}

owners() {
  claude mcp list 2>/dev/null | grep '^plugin:' | sed 's/^plugin:\([^:]*\):\([^:]*\):.*/\2 -> \1/' | sort
}

check_order() {
  local name="$1"
  local order="$2"
  printf '=== install order %s\n' "$name"
  install_in_order "$order"
  local count
  count=$(registered_count)
  printf '    registered plugin MCP servers: %s (17 declared)\n' "$count"
  if [ "$count" -eq 10 ]; then printf '    RESULT: PASS (expected 10 unique names)\n'
  else printf '    RESULT: FAIL\n'; FAILED=$((FAILED+1)); fi
  printf '    ownership:\n'; owners | sed 's/^/      /'
}

check_plugin_only_call() {
  # Contamination-proof by assertion rather than by environment.
  #
  # A separate CLAUDE_CONFIG_DIR cannot be used here: Claude Code resolves its
  # OAuth credential from the system keychain scoped to the default config
  # directory, so an isolated directory reports "Not logged in". And
  # --strict-mcp-config drops plugin-provided servers along with user ones,
  # which removes the thing under test.
  #
  # Instead the assertion itself rejects contamination. A pass REQUIRES the
  # invoked tool name to begin with mcp__plugin_. If a developer machine's own
  # user-level server satisfied the call, the tool name would be
  # mcp__<server>__ and this check fails. The test therefore cannot pass for
  # the wrong reason, which is the property that matters.
  printf '=== plugin-only reachability (assertion-enforced, not environment-enforced)\n'
  local owner
  owner=$(claude mcp list 2>/dev/null | grep -E '^plugin:[a-z-]+:gsa-calc:' | sed 's/^plugin:\([^:]*\):.*/\1/')
  printf '    gsa-calc is owned by: %s\n' "${owner:-<none>}"
  local out=/tmp/coexist-plugin-only.txt
  claude -p "CONSTRAINT: you may only call MCP tools whose name begins with mcp__plugin_.
Do not call mcp__gsa-calc__ or any other non-plugin MCP tool; those simulate a
personal configuration a new user would not have.

Under that constraint, call the GSA CALC+ semantic operation keyword_search
with query 'program manager'. Print the exact MCP tool name you invoked and
whether it returned rate data. End with one line: TOOLNAME=<exact tool name>" \
    --permission-mode bypassPermissions < /dev/null > "$out" 2>&1
  local tool
  tool=$(grep -oE 'mcp__[A-Za-z0-9_-]+__keyword_search' "$out" | head -1)
  printf '    tool invoked: %s\n' "${tool:-<none>}"
  case "$tool" in
    mcp__plugin_*) printf '    RESULT: PASS (losing agent reached the capability via a plugin-provided server)\n' ;;
    "")            printf '    RESULT: FAIL (no CALC tool reachable)\n'; FAILED=$((FAILED+1)) ;;
    *)             printf '    RESULT: FAIL (satisfied by a non-plugin server: %s)\n' "$tool"; FAILED=$((FAILED+1)) ;;
  esac
  printf '    transcript: %s\n' "$out"
}

check_promotion() {
  printf '=== winner promotion after uninstalling the owning plugin\n'
  local before
  before=$(claude mcp list 2>/dev/null | grep -E '^plugin:[a-z-]+:sam-gov:' | sed 's/^plugin:\([^:]*\):.*/\1/')
  printf '    sam-gov owner before: %s\n' "${before:-<none>}"
  claude plugin uninstall "$before@$MARKETPLACE" >/dev/null 2>&1
  local after
  after=$(claude mcp list 2>/dev/null | grep -E '^plugin:[a-z-]+:sam-gov:' | sed 's/^plugin:\([^:]*\):.*/\1/')
  printf '    sam-gov owner after:  %s\n' "${after:-<none>}"
  if [ -n "$after" ] && [ "$after" != "$before" ]; then
    printf '    RESULT: PASS (promoted, capability retained)\n'
  else
    printf '    RESULT: FAIL (server lost on winner removal)\n'; FAILED=$((FAILED+1))
  fi
  claude plugin install "$before@$MARKETPLACE" >/dev/null 2>&1
}

check_order A "$ORDER_A"
check_order B "$ORDER_B"
check_plugin_only_call
check_promotion
install_in_order "$ORDER_A"

printf '\n%s\n' "failures: $FAILED"
exit "$FAILED"
