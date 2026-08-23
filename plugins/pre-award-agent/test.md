# Pre-Award Agent Release-Candidate Test Record

Date: August 21, 2026

Package: `pre-award-agent` `1.0.0-rc.7`

Status: release candidate; not approved for a `1.0.0` tag

## Locked components

- Agent Plugins specification: 1.0.0
- Canonical skills commit: `d49ad2051cc7053794b5f5c5a986b4824ff315bf`
- Canonical MCP commit: `1d286d2015b8cca628f35d7b19c995b9cb5fb906`
- `bls-oews-mcp==1.0.6`, explicit 3-second safeguard
- `gsa-calc-mcp==1.0.4`, explicit 3-second safeguard
- `gsa-perdiem-mcp==1.0.6`, explicit 4-second safeguard

Every vendored runtime file matched its SHA-256 lock. Development-only `test.md` and `testing.md` files were not copied into installed skill folders.

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

- This orchestrator defines no launch menu by design; it infers the mode from the request. Explicit invocation offered all four modes (scope only, pricing only, end to end, revision and repricing) and asked which to use, with no research, retrieval, or MCP call.
- The bundled `pre-award-workflow` skill declared `license: Apache-2.0` through `1.0.0-rc.3` while every manifest and LICENSE in the package declared MIT. Corrected to MIT in this release, and `scripts/validate_packages.py` now fails when a skill, package, and repository license disagree.

## Test environment

- Codex CLI 0.149.0-alpha.4, GPT-5.6 Sol, xhigh reasoning
- Claude Code CLI 2.1.238
- GitHub Copilot CLI 1.0.80
- `uv` 0.11.5
- LibreOffice 26.2.4.2
- macOS on Apple silicon

## Package, skill, and offline MCP checks

- Agent Plugins 1.0 `plugin.json` and `mcp.json` schema validation: pass
- Portable frontmatter, internal references, no-escape paths, no symlinks, no embedded credentials, exact PyPI pins, wrapper locations, and manifest-version parity: pass
- Codex plugin validator: pass
- Claude Code strict plugin and marketplace validation: pass
- All five bundled skills passed the skill validator
- Six deterministic orchestrator contract tests passed repository-wide
- All seven bundled Python validators or recomputation scripts compiled in a temporary directory and returned command-line help
- MCP process startup and tool discovery, without invoking any tool or upstream API: BLS OEWS 7 tools, GSA CALC+ 8 tools, GSA Per Diem 6 tools

The source MCP `v1.0.9` release passed 3,464 offline tests across all eight packages, with 1,614 live-network tests skipped. Shared pacing tests covered fake-clock intervals, coroutine and process serialization, shared `api.data.gov` buckets, distinct keys, keyless services, override validation, and numeric, HTTP-date, and absent `Retry-After` behavior. All eight Trusted Publisher jobs completed, and the three agent dependencies initialized from their published wheels and exposed their tool catalogs without credentials or upstream calls.

## Codex orchestration controls

The no-network routing suite used native `$pre-award-workflow` invocation for explicit cases and allowed read-only access to installed skill instructions. It prohibited MCP calls, web access, file creation, and file modification.

Seven Pre-Award scenarios passed:

1. Missing contract type stopped at the user or Contracting Officer decision.
2. Natural-language PWS-to-FFP routing selected end-to-end mode and began with the SOW/PWS gate.
3. Hybrid FFP and T&M CLINs required an approved routing table and separate workbooks.
4. An approved handoff remained approved and did not trigger repeated decomposition.
5. A natural-language fair-and-reasonable request produced the controlled Option A/Option B boundary.
6. Explicit fair-and-reasonable invocation produced the exact component boundary. This release-blocking case passed three additional consecutive repeat runs.
7. Missing BLS capability produced a specific hard stop, preserved approved work, and did not continue with CALC+ alone.

An early harness version verbally requested skill invocation and prohibited the read-only shell access Codex uses to load a skill body. That setup exercised only skill metadata and produced invalid boundary behavior. The harness was corrected to use a native leading `$skill` mention and allow read-only skill-file inspection. Only the corrected runs count as release evidence.

## Locked component evidence

The byte-identical canonical component packages carry their own August 21 records. Those records include:

- A validated eight-page PWS fixture, six rejected document fault injections, LibreOffice rendering, and Codex and Claude authority-boundary behavior
- FFP, LH/T&M, and CR workbook fixtures that passed formula-structure audit, independent recomputation, and LibreOffice formula execution
- Pricing fault injections for `DATEDIF`, incorrect cross-sheet wage rows, coverage-hours errors, materials treatment, fee treatment, and formula structure
- A prior FFP pacing observation of nine keyed calls with a shortest observed gap of 5.883 seconds

Those component records are evidence for the locked skill implementations, not proof that every multi-skill agent path has been rerun.

## Historical client installation and blockers (before RC5 stabilization)

The compatibility entries below are historical checkpoint evidence. Copilot
CLI and VS Code/Copilot are not maintained public-preview support gates; current
maintained support is Codex and Claude Code as stated in the RC5 section below.

| Surface | Result |
|---|---|
| Codex CLI | Clean removal and marketplace installation of `1.0.0-rc.3` passed; package inventory reported five installed skills, and the three pinned MCPs exposed 7, 8, and 6 tools without invoking a tool |
| Codex Desktop | Plugin was installed locally, but a clean new-task end-to-end artifact run remains pending |
| Claude Code | Strict package and marketplace validation passed; clean removal and marketplace installation of `1.0.0-rc.3` passed with the plugin enabled |
| Copilot CLI | Clean removal and marketplace installation of `1.0.0-rc.3` passed; inventory reported five installed skills |
| VS Code/Copilot | Installation, discovery, and representative workflow remain pending |

The `rc.3` client checks cover installation, inventory, package validation, and key-free MCP discovery. They do not replace the earlier routing evidence, and they do not add a new authenticated model or end-to-end artifact result.

When both 1102tools plugins are installed, Codex 0.149.0-alpha.4 reports duplicate MCP-name warnings for the three shared servers and resolves one configuration for each name. Both package configurations are byte-for-byte equivalent at the semantic server level, and repository validation rejects drift. This warning is recorded as current client behavior.

## Unexecuted release gates

The full manual scenarios `PRE-01` through `PRE-16` in [`tests/manual_release_matrix.md`](../../tests/manual_release_matrix.md) have not all been rerun as multi-turn agent sessions. In particular, clean end-to-end PWS-to-IGCE artifact runs for FFP, LH, T&M, CR, hybrid, revision, rejected-key, and zero-travel paths remain open across the required client matrix.

No live federal API was called during package testing. This avoided shared-key risk, but means live keyed startup, authentication failure, provider rate-limit behavior, and call-timestamp evidence still require the serialized manual release run.

## Historical release decision (before RC5 stabilization)

Static packaging and the available Codex control tests pass. The authenticated cross-client and end-to-end artifact matrix is incomplete, so `1.0.0` is blocked. The public preview is `1.0.0-rc.4`.

## Historical RC5 stabilization evidence — before RC6 remediation

Current maintained public-preview support is Codex and Claude Code (in the
Claude Desktop app or standalone CLI). Copilot CLI and VS Code/Copilot entries
in the historical checkpoint above are compatibility observations, not current
support gates.

The current public preview is `1.0.0-rc.5`, pinned to BLS OEWS `1.0.5`, GSA
CALC+ `1.0.4`, and GSA Per Diem `1.0.5`. The repaired shared pacing runtime
passed simultaneous nonzero-interval coroutine and cross-process serialization
tests without deadlock.

Codex and Claude Code release-blocking routes passed, including contract-type
authority, hybrid separate-workbook routing, approved handoff preservation,
the explicit fair-and-reasonable boundary, and missing-capability hard stops.
Claude Desktop's embedded Code binary independently passed the explicit
contract-type boundary. The representative 16-page PWS and seven-sheet FFP
IGCE passed separation, structure, formula, independent recomputation,
LibreOffice recalculation, extraction, and visual review; the independently
recomputed workbook total was `$598,481.5713107554`.

The remaining manual modes continue to gate final `1.0.0`. The replayable RC5
inventory is [`../../tests/manual/rc5_closure_ledger.json`](../../tests/manual/rc5_closure_ledger.json).

## RC6 remediation — 2026-08-22

`1.0.0-rc.6` pins BLS OEWS `1.0.6` and GSA Per Diem `1.0.6`. Both MCPs now
redact active credentials from upstream response bodies, parsed payloads, and
network exceptions before any error or tool result can reach a client. The
credential and representative artifact lanes must replay against the published
patches before this candidate closes.

## RC5 lifecycle hardening replay — 2026-08-23

The current `1.0.0-rc.6` Codex lane produced and validated a PWS plus FFP IGCE.
The Claude retry used a protected valid BLS v2 credential and produced the
approved PWS plus a seven-sheet CPFF Term IGCE for 14,920 hours and a
`$3,446,455.87` independently recomputed total estimated price. The workbook
passed canonical validation, independent recomputation, serialized LibreOffice
recalculation, a workbook-wide cached-error audit, ZIP integrity, fault
injection, and inspection of all 13 rendered pages. The existing CR validator
caught a double-counted labor subtotal before delivery; the corrected workbook
passed every layer. No credential value was displayed or retained. No P0 or P1
Pre-Award defect remains; complete Codex resume proof and remaining manual modes
still gate final `1.0.0`. Evidence:
[`../../tests/manual/rc5_lifecycle_ledger.json`](../../tests/manual/rc5_lifecycle_ledger.json).

## RC7 boundary and host-artifact hardening — 2026-08-23

`1.0.0-rc.7` vendors canonical skills commit `d49ad2051cc7053794b5f5c5a986b4824ff315bf`. The orchestrator makes the fixed FFP Option A/Option B response an explicit release invariant and rejects a shorter refusal or a later promise to write the determination. Spreadsheet runtime adaptation now follows a governing host artifact workflow and fails early into a structured specification when the supported workbook path is absent; it never guesses dependency paths or calls the fallback a workbook. Cross-client routing and host-degradation replay remain required.
