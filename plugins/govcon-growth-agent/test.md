# GovCon Growth Agent test record

Version: `1.0.1`

## Stable 1.0 qualification

The stable package preserves the qualified `rc.10` workflow bytes and current
MCP pins. RC15 exit qualification passed clean remote installation in both
maintained client families, exact package-tree checks, explicit menu routing,
approval boundaries, credential redaction, and the nine-server live-canary
gate. The validated Codex and Claude brief artifacts, retrieval-timestamp
checks, and lifecycle evidence remain applicable. No unresolved P0 or P1
defect remained at promotion.

Explicit agent selection or invocation is the stable routing contract. Ambient
activation is host-controlled and best effort. Native web only remains the
recommended public-web choice; Tavily remains an explicitly selected optional
provider and is never a silent fallback.
Evidence date: August 22, 2026

## Canonical skill evidence

The bundled `govcon-growth-workflow` runtime is synchronized from `federal-contracting-skills` commit `658108e2c59b591f617c89b4c38e1822a6429bd7`. Its canonical test record includes:

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

## Historical RC5 stabilization evidence — before RC6 remediation

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

## RC6 remediation — 2026-08-22

`1.0.0-rc.5` pins SAM.gov `1.0.9`. The server redacts the active credential
from upstream bodies, payloads, URLs, and network exceptions and no longer
echoes a malformed key prefix. The Codex host-profile and authenticated
opportunity lanes must replay before this candidate closes.

## RC5 lifecycle hardening replay — 2026-08-23

Current `1.0.0-rc.5` Codex and Claude lanes each produced a GovCon Growth
brief. Source-call timestamp linkage, record, evidence, structure, links,
extraction, LibreOffice, ZIP-integrity, and visual checks passed. The Claude
resume checkpoint preserved prior retrieval IDs and limitations without a
duplicate call, bid decision, or premature artifact. The Codex long-session
artifact passed, while its separately controlled resume checkpoint remains an
advisory evidence gap. No GovCon Growth P0 or P1 remains; the broader
authenticated opportunity matrix still gates final `1.0.0`. Evidence:
[`../../tests/manual/rc5_lifecycle_ledger.json`](../../tests/manual/rc5_lifecycle_ledger.json).

## RC6 native-first provider correction — 2026-08-23

`1.0.0-rc.6` vendors canonical skill commit
`1fece54e03ac7465b82314150d2d9ffffd895452`. The provider menu is now Native
web only (Recommended), Native web with Tavily fallback, Tavily only, and No
public web. Deterministic validation enforces native-first combined mode,
native-to-Tavily fallback direction, explicit provider order, and read-only
migration of retired Tavily-first records. Tavily remains bundled. Installed
Codex and Claude behavioral qualification is recorded separately after the
package release gate.

## RC7 provider and menu hardening — 2026-08-23

`1.0.0-rc.7` vendors canonical skills commit `d49ad2051cc7053794b5f5c5a986b4824ff315bf`. The provider gate rejects ambiguous replies, preserves federal MCP and supplied-document research in No public web mode, and excludes account creation or payment as a Tavily recovery path. A specific opportunity or attached bid-screen request is also explicitly prohibited from bypassing the complete nine-choice first-turn menu.

## RC8 exact provider-language remediation — 2026-08-23

`1.0.0-rc.8` vendors canonical skills commit `84f35851c6294fcf584d0bbb22f3fb8172ad5eb5`. A Sonnet installed-package replay correctly rejected an ambiguous selection but paraphrased combined fallback as available for “insufficient” native results. The current gate requires the complete policy choice block without paraphrasing and preserves the rule that zero, thin, or inconclusive results never trigger Tavily. The 14-case matrix and both-client research lanes must replay against exact RC8 bytes.

## RC9 calculation-evidence correction — 2026-08-23

`1.0.0-rc.9` vendors canonical skills commit `6f8911f0b6110e139408c0d6766513847b9ead14`. Stable qualification found that consequential decision-weight calculations could use the generic marker `[calculation]` despite a stable calculation evidence item in the record. The builder now requires exactly one linked calculation evidence item and cites its stable ID. The DOCX validator verifies that ID on the same paragraph as each total, and deterministic negative coverage removes only the paragraph citation while leaving the evidence register intact.

## RC10 LibreOffice evidence-table pagination correction — 2026-08-23

`1.0.0-rc.10` vendors canonical skills commit `3cfca7adffd6f45ae84f9f60d8530e740b363de1`. A long qualification brief reproduced a clipped repeated Evidence Register header on a later LibreOffice-rendered page. The builder now keeps that long table's header on its first page only while preserving repeating headers for the other tables. Deterministic OOXML coverage rejects reintroducing the repeated header, and the preserved nine-page brief passed record validation, brief validation, LibreOffice PDF conversion, citation checks, and page-by-page visual review without clipping.
