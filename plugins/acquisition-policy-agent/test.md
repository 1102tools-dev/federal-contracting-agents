# Acquisition Policy Agent test record

Version: `1.0.2`

## Stable 1.0 qualification

The stable package preserves the qualified `rc.4` workflow bytes and pinned
Acquisition.gov, eCFR, Federal Register, and Regulations.gov servers. RC15 exit
qualification passed clean remote installation in both maintained client
families, exact package-tree checks, explicit menu routing, conflict and
authority boundaries, credential redaction, and the nine-server live-canary
gate. The validated Codex and Claude impact briefs remain applicable. No
unresolved P0 or P1 defect remained at promotion.

## Passed before packaging

- The bundled `acquisition-policy-workflow` runtime is synchronized from
  `federal-contracting-skills` commit
  `6a0bd06dae4d100bde9f03f619ed509e548eebe7`.
- Canonical skill quick validation and repository validation.
- Policy-record fixture validation, controlled negative cases, and deterministic unit tests.
- Impact-brief generation, evidence-ID validation, link validation, LibreOffice conversion, text extraction, and all-page visual review.
- Acquisition.gov MCP offline parsing, PDF, cursor, SSRF, redirect, size, content-type, 429, pacing, strict-schema, and build tests.
- Local stdio startup and MCP discovery reported server `acquisition-gov` version `1.0.1` with exactly the five expected tools.
- Agent-level local-wheel startup and discovery loaded the exact four-server inventory without invoking an upstream tool: Acquisition.gov 5 tools, eCFR 13, Federal Register 8, and Regulations.gov 8.

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

### Historical package-specific checkpoint (rc.2)

The checkpoint below predates the RC5 stabilization section. It is retained as
dated evidence and is not the current package-preview declaration.

Installed and verified at `1.0.0-rc.2`.

- Explicit invocation returned the exact packaged ten-item launch menu verbatim, in order, with no retrieval or MCP call.
- All four pinned servers connected and discovered their tools: Acquisition.gov 5, eCFR 13, Federal Register 8, Regulations.gov 8.

## Historical upstream live gate

On 2026-08-22 the serialized release gate passed twice. The official RFO index, Part 10 model page, an indexed four-page NSF deviation PDF, and the FAQ each returned HTTP 200 with complete extraction. The MCP recorded source hashes and retained the rule that future hash changes require review rather than silent acceptance.

## Historical published-package and clean-install gate

The immutable MCP source commit `3f9376a406a2af17e5810d81f319d81efe34417e` installed into an isolated `uvx` environment directly from GitHub and exposed exactly five tools without invoking an upstream tool. Release workflow `32561799836` then passed shared safety checks, all nine package test-and-build jobs, trusted publication, and release creation. A fresh `uvx` environment installed `acquisition-gov-mcp==1.0.0` from PyPI and discovered all four policy-agent servers without invoking an upstream tool: Acquisition.gov 5 tools, eCFR 13, Federal Register 8, and Regulations.gov 8.

## Historical client installation and explicit routing (before RC5 stabilization)

On 2026-08-22 the repository marketplace installed `acquisition-policy-agent==1.0.0-rc.2` successfully in Codex CLI and Claude Code. Fresh noninteractive sessions invoked the workflow explicitly and returned the exact ten-item launch menu without external retrieval or MCP calls. The Codex check read the packaged launch-menu reference as required; forbidding all local file operations prevents progressive-disclosure references from loading and is not a valid workflow invocation.

## Historical open agent release gates (before RC5 stabilization)

- Run implicit routing cases in clean Codex CLI/Desktop and Claude Code.
- Complete an agency RFO status analysis, rulemaking/comment workflow, public-comment analysis, and validated impact brief with live sources.
- Record the complete client and artifact matrix below before removing `rc`.

The package remains a release candidate until every open gate passes.

## Historical RC5 stabilization evidence — before RC6 remediation

Current maintained public-preview support is Codex and Claude Code (in the
Claude Desktop app or standalone CLI). Copilot CLI and VS Code/Copilot entries
in the historical checkpoint above are compatibility observations, not current
support gates.

The current installable preview is `1.0.0-rc.3`, pinned to Acquisition.gov
`1.0.1`, eCFR `1.0.5`, Federal Register `1.0.4`, and Regulations.gov `1.0.4`.
Clean discovery exposed 5, 13, 8, and 8 tools respectively.

Policy record schema `1.1` structures every conflict with evidence IDs, status,
resolution source, and timestamps. Codex and Claude Code replayed the
conflicting-threshold scenario and both returned `documented_conflict`; neither
source was described as controlling, governing, applicable, or operative.
Claude Sonnet passed the exact ten-item menu, direct agency-status route, model
text boundary, and pending-rule boundary. Claude Opus 5 fast mode independently
passed the menu and both policy-state boundaries, and its fresh conflict run
recorded fast mode on. Claude Desktop's embedded Code binary independently
passed the exact ten-item menu.

The representative four-page impact brief passed record, evidence/status,
structure, five-link, LibreOffice, extraction, and visual validation. The full
live rulemaking/comment and procurement-specific status matrix remains a final
`1.0.0` gate. The replayable RC5 inventory is [`../../tests/manual/rc5_closure_ledger.json`](../../tests/manual/rc5_closure_ledger.json).

## RC6 remediation — 2026-08-22

`1.0.0-rc.4` pins Regulations.gov `1.0.5`, which redacts the active credential
from upstream response bodies, parsed payloads, request URLs, and network
exceptions. The keyed Regulations.gov and representative impact-brief lanes
must replay before this candidate closes.

## RC5 lifecycle hardening replay — 2026-08-23

Current `1.0.0-rc.4` Codex and Claude lanes each produced a validated
Acquisition Policy impact brief. Both preserved the unresolved-conflict boundary
without naming a disputed source as controlling, governing, applicable, or
operative. Record, status, evidence, structure, links, extraction,
LibreOffice, ZIP-integrity, and visual checks passed. The Claude resume
checkpoint also preserved the unresolved conflict without inventing a finding
or artifact; the complete Codex resume chain remains advisory. No Acquisition
Policy P0 or P1 remains. The broader live rulemaking/comment matrix still gates
final `1.0.0`. Evidence:
[`../../tests/manual/rc5_lifecycle_ledger.json`](../../tests/manual/rc5_lifecycle_ledger.json).

## 1.0.1 credential-readiness qualification — 2026-08-24

Fresh installed-package sessions in Claude Code and Codex CLI, with every
credential variable absent, called only the local Regulations.gov
`get_access_status` operation before output. Both displayed
`REGULATIONS_GOV_API_KEY is not configured` and the shared DEMO-key limit before
the exact ten-choice menu, while preserving the keyless eCFR, Federal Register,
and Acquisition.gov routes. Neither client blamed Regulations.gov or described
the limited fallback as an outage.

## 1.0.2 outcome-guidance candidate — 2026-08-26

The vendored canonical workflow now names the selected chat product or Impact
Brief, its contents, documented-status boundary, and next gate before framing
or capability preflight. Help diagnoses with at most three questions and then
recommends exactly one route without repeating the menu. Canonical and package
static tests cover all ten selections, the fixed status-boundary precedence,
and the preview ordering. Installed CLI and Desktop qualification remains a
promotion gate and is recorded separately when complete.
