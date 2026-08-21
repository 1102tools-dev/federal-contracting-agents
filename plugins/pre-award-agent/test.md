# Pre-Award Agent Release-Candidate Test Record

Date: August 21, 2026

Package: `pre-award-agent` `1.0.0-rc.1`

Status: release candidate; not approved for a `1.0.0` tag

## Locked components

- Agent Plugins specification: 1.0.0
- Canonical skills commit: `f28404af67d454a1313d145962de79e7ba37a7b1`
- Canonical MCP commit: `4e46c06bb58aacce44a24d372200c4116adb4483`
- `bls-oews-mcp==1.0.3`
- `gsa-calc-mcp==1.0.2`
- `gsa-perdiem-mcp==1.0.3`

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

The source MCP releases also passed their pacing regression suites before publication: BLS OEWS had 85 passing tests with 164 network tests skipped, and GSA Per Diem had 186 passing tests with 255 network tests skipped. The plugin sets the three-second pacing floor for both credentialed servers.

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
| Codex CLI | Clean `1.0.0-rc.1` marketplace installation, skill discovery, MCP discovery, explicit routing, and natural-language routing passed; a post-install boundary smoke passed |
| Codex Desktop | Plugin was installed locally, but a clean new-task end-to-end artifact run remains pending |
| Claude Code | Marketplace update to `1.0.0-rc.1`, strict validation, three-MCP inventory, and local component inventory passed; restart is required to apply the update, and model runs are blocked because the OAuth session is expired and cannot refresh |
| Copilot CLI | Marketplace update to `1.0.0-rc.1` and plugin inventory passed; model runs are blocked because no supported OAuth or fine-grained token is configured |
| VS Code/Copilot | Installation, discovery, and representative workflow remain pending |

When both 1102tools plugins are installed, Codex 0.149.0-alpha.4 reports duplicate MCP-name warnings for the three shared servers and resolves one configuration for each name. Both package configurations are byte-for-byte equivalent at the semantic server level, and repository validation rejects drift. This warning is recorded as current client behavior.

## Unexecuted release gates

The full manual scenarios `PRE-01` through `PRE-16` in [`tests/manual_release_matrix.md`](../../tests/manual_release_matrix.md) have not all been rerun as multi-turn agent sessions. In particular, clean end-to-end PWS-to-IGCE artifact runs for FFP, LH, T&M, CR, hybrid, revision, rejected-key, and zero-travel paths remain open across the required client matrix.

No live federal API was called during package testing. This avoided shared-key risk, but means live keyed startup, authentication failure, provider rate-limit behavior, and call-timestamp evidence still require the serialized manual release run.

## Release decision

Static packaging and the available Codex control tests pass. The authenticated cross-client and end-to-end artifact matrix is incomplete, so `1.0.0` is blocked. The package remains `1.0.0-rc.1`.
