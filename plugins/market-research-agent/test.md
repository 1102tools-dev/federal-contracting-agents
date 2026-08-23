# Market Research Agent test record

Version: `1.0.0-rc.6`
Evidence date: August 22, 2026

## Canonical skill evidence

The bundled `market-research-workflow` runtime is synchronized from `federal-contracting-skills` commit `655800a929bfdcfef348ce19ecd941633a597b02`. The `rc.3` package renames the canonical skill from `market-research-builder` to `market-research-workflow`; archived research records carrying the old identifier remain valid during the RC transition, but new explicit invocations use `$market-research-workflow`. Its canonical `test.md` records:

- Sixteen deterministic repository tests, both artifact builders, LibreOffice conversion, extraction, citation, recomputation, and portable-skill validation.
- All four provider modes, approved fallback, prohibited provider and tool use, private and credential-bearing URL rejection, and prompt-injection/document-precedence controls.
- The complete menu, document-intake stop, four provider choices, sanitized terms and URLs, third-party disclosure, and no pre-approval research in Codex CLI `0.149.0-alpha.4` with GPT-5.6 Sol at xhigh and Claude Code `2.1.239` with `claude-opus-5` at max effort.
- A Sonnet packaged-plugin smoke initially exposed an omitted selection question. The exact question was moved into the front-loaded core; a fresh `claude-sonnet-5` max-effort run then returned the six choices and exact question with zero web-search and web-fetch requests.

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

### Historical package-specific checkpoint (rc.4)

The checkpoint below predates the RC5 stabilization section. It is retained as
dated evidence and is not the current package-preview declaration.

Installed and verified at `1.0.0-rc.4`.

- Explicit invocation returned the complete six-item workflow menu and its closing selection question, with no research, retrieval, or MCP call.
- `sam-gov` now pins `sam-gov-mcp==1.0.7`, whose missing-key guidance is host-neutral.

## `rc.3` rename and repackage evidence

- Component synchronization and SHA-256 locking resolve exactly one bundled skill named `market-research-workflow`; the retired skill folder is absent.
- All five agent packages passed schema, portability, reference, pinned-MCP, Tavily-policy, and credential-hygiene validation after the rename.
- The agent repository passed 15 tests plus 8 subtests, and every bundled deterministic script passed its `--help` discovery check.
- Local startup discovered 19 SAM.gov and 55 USASpending tools without invoking a tool. Remote Tavily discovery was intentionally not repeated for this naming-only package revision.
- The prior `rc.2` installed-client results below remain behavioral evidence. A clean `rc.3` install and explicit `$market-research-workflow` invocation remain open before final release.

## Package and remote-MCP evidence

Passed:

- Agent Plugins 1.0 schemas, all portable/native manifests, exact federal package pins, pacing values, references, component hashes, bundled scripts, and credential hygiene.
- Tavily is confined to the two research agents. Portable configuration uses the exact Streamable HTTP endpoint and keyless header; Claude-native configuration is equivalent with `type: http`.
- Live keyless initialization and `tools/list` completed without OAuth and without invoking a tool. The server advertised five operations and produced schema SHA-256 `f28255db8e816ce522e9bd20a89b6fcf2312af41e60c3846799e9c3195e60992`. The required `tavily_search` and `tavily_extract` operations were present.
- The current keyless endpoint also advertises `tavily_crawl`, `tavily_map`, and `tavily_research`. The skill and record validator prohibit all three; this upstream tool-surface mismatch is recorded in `components.lock.json`.
- One approved, non-sensitive Market Research Tavily search was sent for `official FAR Part 10 market research guidance`, restricted to `acquisition.gov`. Tavily returned a `CallToolResult`; the local evidence formatter then used the wrong Python attribute name and failed before retaining the response text. No repeat query was made. The equivalent native-only run independently verified the underlying Acquisition.gov pages.
- Clean isolated installation and `1.0.0-rc.2` inventory passed in Codex CLI, Claude Code, and GitHub Copilot CLI `1.0.80`. Claude resolved one skill, one native agent, and the expected SAM.gov, USASpending, and Tavily servers. This remains historical behavioral evidence; the naming-only `rc.3` package requires a fresh clean-install check before final release.

## Historical installed-client behavior (before RC5 stabilization)

- Codex session `01a0275a-09cc-7a70-b8a1-dbdefa9b8309` used the installed plugin, showed the menu, stopped for document intake, displayed the complete provider approval, and honored `Native search only`. It made exactly one approved Acquisition.gov search, fetched the approved official pages, cited the underlying FAR pages, and made zero Tavily and zero federal MCP calls.
- Claude Opus 5 Max loaded the packaged plugin and returned the complete recommended menu with zero web-search and web-fetch requests.
- Claude Sonnet 5 Max passed the corrected exact-question regression with zero web-search and web-fetch requests.
- When both research agents are installed, Codex `0.149.0-alpha.4` warns that their intentionally shared semantic MCP names collide and selects one identical definition. The workflows remained functional, but the warning is retained as a preview limitation.

## Historical open release-candidate gates (before RC5 stabilization)

- Codex Desktop has not been independently rerun after `rc.2`.
- The VS Code CLI is not installed on this machine, so VS Code/Copilot installation remains open.
- Copilot installation passed, but a representative authenticated workflow remains open.
- Tavily-only failure and combined-mode fallback are covered deterministically, not by manufacturing a live provider outage.
- The Market Tavily response content was not retained because of the local formatter error described above; direct content/citation capture remains an `rc` evidence gap.
- Full implicit-routing, upload-only-client, commercial-evidence, and client-generated report scenarios remain open.

These gaps block final `1.0.0`; they do not block this repository-marketplace release candidate.

## Historical RC5 stabilization evidence — before RC6 remediation

Current maintained public-preview support is Codex and Claude Code (in the
Claude Desktop app or standalone CLI). Copilot CLI and VS Code/Copilot entries
elsewhere in this record are historical compatibility observations, not current
support gates.

`1.0.0-rc.5` vendors Market Research record schema `1.2`. Formal generation now
requires timestamped approvals for findings, every stable `Dnnn` acquisition
decision, and every `Unnn` unresolved-item disposition. Legacy `1.1` records
remain readable but must migrate before a new formal artifact is generated.

Codex and Claude Code both replayed the ambiguous generic `Approved` scenario
and stopped for the missing `D001` selection and `U001` disposition. Claude
Sonnet passed the explicit menu, natural-language menu replay, and decision
boundary. Claude Opus 5 in fast mode independently passed the explicit menu and
decision boundary. The published SAM.gov `1.0.8` and USAspending `1.0.4`
acquisition profile exposed 19 and 20 tools, including the core award,
spending, agency, recipient, NAICS, and PSC operations.

The representative four-page report passed record, evidence, structure,
LibreOffice, extraction, and visual validation. Full authenticated coverage of
every market-research mode remains a final `1.0.0` gate. The machine-readable
run inventory is [`../../tests/manual/rc5_closure_ledger.json`](../../tests/manual/rc5_closure_ledger.json).

## RC6 remediation — 2026-08-22

`1.0.0-rc.6` pins SAM.gov `1.0.9` and vendors canonical skill commit
`655800a929bfdcfef348ce19ecd941633a597b02`. Plan approval now allowlists only
the exact public extraction URLs shown to the user. Newly discovered URLs are
registered and require explicit updated approval before fetch or extraction;
provider fallback cannot bypass the stop. The affected Claude and Codex live
research lanes must replay this gate before the candidate closes.
