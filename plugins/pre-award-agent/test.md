# Pre-Award Agent Release-Candidate Test Record

Date: August 21, 2026

Package: `pre-award-agent` `1.0.0-rc.3`

Status: release candidate; not approved for a `1.0.0` tag

## Locked components

- Agent Plugins specification: 1.0.0
- Canonical skills commit: `8b46d1b4b53965efc62bac18aeffdbdc32e7ecf6`
- Canonical MCP commit: `8c0fb8a7aa09abc4c59f03570b183e31ff83cef6`
- `bls-oews-mcp==1.0.4`, explicit 3-second safeguard
- `gsa-calc-mcp==1.0.3`, explicit 3-second safeguard
- `gsa-perdiem-mcp==1.0.4`, explicit 4-second safeguard

Every vendored runtime file matched its SHA-256 lock. Development-only `test.md` and `testing.md` files were not copied into installed skill folders.

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

## Client installation and blockers

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

## Release decision

Static packaging and the available Codex control tests pass. The authenticated cross-client and end-to-end artifact matrix is incomplete, so `1.0.0` is blocked. The public preview is `1.0.0-rc.3`.
