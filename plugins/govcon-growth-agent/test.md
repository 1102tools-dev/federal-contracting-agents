# GovCon Growth Agent test record

Version: `1.0.0-rc.4`
Evidence date: August 22, 2026

## Canonical skill evidence

The bundled `govcon-growth-workflow` runtime is synchronized from `federal-contracting-skills` commit `3e49d0617b50a6f2d9e942f45d4656d89385d442`. Its canonical `test.md` records:

- Sixteen deterministic repository tests, the evidence-brief artifact builder, LibreOffice conversion, extraction, citation, recomputation, bid-boundary checks, and portable-skill validation.
- All four provider modes, approved fallback, prohibited provider and tool use, private and credential-bearing URL rejection, and incomplete-company-context controls.
- The complete menu, four provider choices, sanitized terms and URLs, third-party disclosure, and no pre-approval research in Codex CLI `0.149.0-alpha.4` with GPT-5.6 Sol at xhigh and Claude Code `2.1.239` with `claude-opus-5` at max effort.
- A Sonnet packaged-plugin smoke initially exposed an omitted selection question. The exact question was moved into the front-loaded core; a fresh `claude-sonnet-5` max-effort run then returned the nine choices and exact question with zero web-search and web-fetch requests.

No live federal API call was made.

## Claude Code acceptance — August 22, 2026

Both Claude Code surfaces were exercised against this package. Claude Code is one
runtime distributed two ways: the Claude Desktop app bundles `claude-code`
`2.1.237`, and the standalone CLI is a separate binary at `2.1.240`. Both
read the same `~/.claude/plugins` cache and the same `settings.json`, and both resolved all
five plugins and the same ten plugin MCP servers with identical pins. The
packages this record covers were installed by the CLI binary and consumed by the
desktop runtime, so the cross-surface path is exercised rather than assumed.
There is no separate desktop package.

- Full teardown first: all five plugins uninstalled, the marketplace removed,
  and `~/.claude/plugins/cache/1102tools` deleted. A fresh marketplace add and
  install of all five reported the expected versions.
- All ten plugin MCP servers connected, each launching its pinned distribution.
- Launch surfaces verified in five fresh noninteractive sessions with no MCP
  calls, retrieval, or file operations. Harness: `tests/manual/menu_smoke.sh`.
- Coexistence, install-order, plugin-only reachability, and winner promotion
  verified. Harness: `tests/manual/coexistence.sh`, zero failures.

### Shared MCP server names

The five packages declare seventeen MCP servers across ten distinct names.
Claude Code deduplicates by name and the first declarer wins, so ten register
and ownership depends on install order. Order A (Market Research first) gave
`sam-gov`, `usaspending`, and `tavily-web` to Market Research; order B
(Acquisition Policy, Other Transaction, GovCon Growth first) gave them to GovCon
Growth. Ten registered in both orders.

This is namespace attribution, not capability loss. Under order B, with
`gsa-calc` owned by Other Transaction, a Pre-Award request restricted to
plugin-provided tools only was satisfied by the Other Transaction plugin's own
GSA CALC+ server and returned rate data. Uninstalling the owning plugin promoted the next declarer immediately:
`sam-gov` moved from GovCon Growth to Market Research with no loss of
capability. Every skill matches tools by server and semantic operation rather
than by generated prefix, which is what makes the surviving instance
interchangeable.

Duplicate-name warnings at startup are a packaging-polish item. Renaming the
shared servers would start duplicate identical processes and duplicate remote
initialization, so it is deliberately not done.

### Historical package-specific checkpoint (rc.3)

The checkpoint below predates the RC5 stabilization section. It is retained as
dated evidence and is not the current package-preview declaration.

Installed and verified at `1.0.0-rc.3`.

- Explicit invocation returned the complete nine-item workflow menu and its closing selection question, with no research, retrieval, or MCP call.
- `sam-gov` now pins `sam-gov-mcp==1.0.7`, whose missing-key guidance is host-neutral.
- The shipped source-commit citation above was corrected to the commit this package actually vendors. The prior citation named a commit whose later delta changed `references/evidence-contract.md` and `scripts/validate_research_record.py`, so the record attested to bytes the package no longer ships.

## Package and remote-MCP evidence

Passed:

- Agent Plugins 1.0 schemas, all portable/native manifests, exact federal package pins, pacing values, references, component hashes, bundled scripts, and credential hygiene.
- Tavily is confined to the two research agents. Portable configuration uses the exact Streamable HTTP endpoint and keyless header; Claude-native configuration is equivalent with `type: http`.
- Live keyless initialization and `tools/list` completed without OAuth and without invoking a tool. The server advertised five operations and produced schema SHA-256 `f28255db8e816ce522e9bd20a89b6fcf2312af41e60c3846799e9c3195e60992`. The required `tavily_search` and `tavily_extract` operations were present.
- The current keyless endpoint also advertises `tavily_crawl`, `tavily_map`, and `tavily_research`. The skill and record validator prohibit all three; this upstream tool-surface mismatch is recorded in `components.lock.json`.
- One approved, non-sensitive Tavily search for `official federal contracting opportunity guidance for small businesses`, restricted to `sba.gov` and `sam.gov`, completed in keyless mode without error. It returned three SBA pages. The equivalent native-only run verified the underlying SBA pages and cited those pages rather than Tavily.
- Clean isolated installation and `1.0.0-rc.2` inventory passed in Codex CLI, Claude Code, and GitHub Copilot CLI `1.0.80`. Claude resolved one skill, one native agent, and the expected SAM.gov, USASpending, GSA CALC+, and Tavily servers.

## Historical installed-client behavior (before RC5 stabilization)

- Codex session `01a0275d-84ae-73e0-b887-417cf93ba220` used the installed plugin, showed the complete menu, performed mode-specific intake, displayed the complete provider approval, and honored `Native search only`. It made exactly one approved SBA search, followed only approved SBA pages, cited the underlying pages, and made zero Tavily and zero federal MCP calls.
- Claude Opus 5 Max loaded the packaged plugin and returned the complete recommended menu with zero web-search and web-fetch requests.
- Claude Sonnet 5 Max passed the corrected exact-question regression with zero web-search and web-fetch requests.
- When both research agents are installed, Codex `0.149.0-alpha.4` warns that their intentionally shared semantic MCP names collide and selects one identical definition. The workflows remained functional, but the warning is retained as a preview limitation.

## Historical open release-candidate gates (before RC5 stabilization)

- Codex Desktop has not been independently rerun after `rc.2`.
- The VS Code CLI is not installed on this machine, so VS Code/Copilot installation remains open.
- Copilot installation passed, but a representative authenticated workflow remains open.
- Tavily-only failure and combined-mode fallback are covered deterministically, not by manufacturing a live provider outage.
- Complete live opportunity, implicit-routing, upload-only-client, and client-generated brief scenarios remain open.

These gaps block final `1.0.0`; they do not block this repository-marketplace release candidate.

## RC5 stabilization evidence — 2026-08-22

Current maintained public-preview support is Codex and Claude Code (in the
Claude Desktop app or standalone CLI). Copilot CLI and VS Code/Copilot entries
elsewhere in this record are historical compatibility observations, not current
support gates.

`1.0.0-rc.4` pins SAM.gov `1.0.8` and USAspending `1.0.4`, with the latter's
20-tool acquisition profile in every maintained manifest and dormant overlay.
Clean discovery retained the core award, spending, agency, recipient, NAICS,
PSC, transaction, and subaward operations. Source evidence timestamps are now
validated against the linked source-call ledger rather than report-build time.

Codex and Claude explicit menu and pricing-boundary routes passed. Claude
Desktop's embedded Code binary independently passed the explicit menu. One
implicit attached-opportunity prompt did not activate the package and is
recorded as non-blocking host-session routing evidence; the explicit native
contract remains green. The representative three-page brief passed source-call
timestamp linkage, record, structure, rendering, extraction, and visual review.

The full authenticated opportunity matrix remains a final `1.0.0` gate. The
replayable RC5 inventory is [`../../tests/manual/rc5_closure_ledger.json`](../../tests/manual/rc5_closure_ledger.json).
