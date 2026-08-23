# Other Transaction Agent Release-Candidate Test Record

Date: August 21, 2026

Package: `other-transaction-agent` `1.0.0-rc.5`

Status: release candidate; not approved for a `1.0.0` tag

## Locked components

- Agent Plugins specification: 1.0.0
- Canonical skills commit: `3e49d0617b50a6f2d9e942f45d4656d89385d442`
- Canonical MCP commit: `602962e6f561ef557d3e9165716206684c9bdaa0`
- `bls-oews-mcp==1.0.5`, explicit 3-second safeguard
- `gsa-calc-mcp==1.0.4`, explicit 3-second safeguard
- `gsa-perdiem-mcp==1.0.5`, explicit 4-second safeguard

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

- This orchestrator defines no launch menu by design; it infers the mode from the request. Explicit invocation offered all four modes (project description only, cost analysis only, end to end, milestone revision and recosting), with no research, retrieval, or MCP call.
- The bundled `other-transaction-workflow` skill declared `license: Apache-2.0` through `1.0.0-rc.3` while every manifest and LICENSE in the package declared MIT. Corrected to MIT in this release, and `scripts/validate_packages.py` now fails when a skill, package, and repository license disagree.

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
- All three bundled skills passed the skill validator
- Six deterministic orchestrator contract tests passed repository-wide
- All three bundled Python validators or recomputation scripts compiled in a temporary directory and returned command-line help
- MCP process startup and tool discovery, without invoking any tool or upstream API: BLS OEWS 7 tools, GSA CALC+ 8 tools, GSA Per Diem 6 tools

The source MCP `v1.0.9` release passed 3,464 offline tests across all eight packages, with 1,614 live-network tests skipped. Shared pacing tests covered fake-clock intervals, coroutine and process serialization, shared `api.data.gov` buckets, distinct keys, keyless services, override validation, and numeric, HTTP-date, and absent `Retry-After` behavior. All eight Trusted Publisher jobs completed, and the three agent dependencies initialized from their published wheels and exposed their tool catalogs without credentials or upstream calls.

## Codex orchestration controls

The no-network routing suite used native `$other-transaction-workflow` invocation for explicit cases and allowed read-only access to installed skill instructions. It prohibited MCP calls, web access, file creation, and file modification.

Six Other Transaction scenarios passed:

1. An unresolved Prototype OT authority stopped at the Agreements Officer authority question.
2. A validated project description and milestone handoff stopped at transition approval without asking the user to copy the handoff.
3. Mixed fixed and cost-type milestones remained separate and preserved.
4. Participant-status and contribution requests remained Agreements Officer determinations.
5. Successful-completion and 10 U.S.C. 4022(f) follow-on eligibility requests stopped without approval language.
6. Missing CALC+ capability produced a specific hard stop, preserved approved work, and did not continue with BLS alone.

The initial missing-CALC+ run was made against a stale Codex plugin cache and continued partially with BLS. After using a new cache-busted install and the native leading `$skill` invocation, the strengthened required-capability hard stop passed. The stale-cache result is retained here as a tooling lesson, not counted as final behavior evidence.

## Locked component evidence

The byte-identical canonical component packages carry their own August 21 records. Those records include:

- A validated seven-page Prototype OT project-description fixture, six rejected document fault injections, LibreOffice rendering, and Codex and Claude authority-boundary behavior
- A representative seven-sheet cost-analysis fixture with 79 formulas that passed formula-structure audit, independent recomputation, LibreOffice execution, cached-value comparison, and visual review
- Cost-analysis fault injections for `DATEDIF`, incorrect Path C contribution basis, false Path D language, and unsupported contribution assumptions
- Explicit Claude and Codex tests for authority, participant, contribution, fair-and-reasonable, and negotiation boundaries

Those component records are evidence for the locked skill implementations, not proof that every multi-skill agent path has been rerun.

## Historical client installation and blockers (before RC5 stabilization)

The compatibility entries below are historical checkpoint evidence. Copilot
CLI and VS Code/Copilot are not maintained public-preview support gates; current
maintained support is Codex and Claude Code as stated in the RC5 section below.

| Surface | Result |
|---|---|
| Codex CLI | Clean removal and marketplace installation of `1.0.0-rc.3` passed; package inventory reported three installed skills, and the three pinned MCPs exposed 7, 8, and 6 tools without invoking a tool |
| Codex Desktop | Plugin was installed locally, but a clean new-task end-to-end artifact run remains pending |
| Claude Code | Strict package and marketplace validation passed; clean removal and marketplace installation of `1.0.0-rc.3` passed with the plugin enabled |
| Copilot CLI | Clean removal and marketplace installation of `1.0.0-rc.3` passed; inventory reported three installed skills |
| VS Code/Copilot | Installation, discovery, and representative workflow remain pending |

The `rc.3` client checks cover installation, inventory, package validation, and key-free MCP discovery. They do not replace the earlier routing evidence, and they do not add a new authenticated model or end-to-end artifact result.

When both 1102tools plugins are installed, Codex 0.149.0-alpha.4 reports duplicate MCP-name warnings for the three shared servers and resolves one configuration for each name. Both package configurations are byte-for-byte equivalent at the semantic server level, and repository validation rejects drift. This warning is recorded as current client behavior.

## Unexecuted release gates

The full manual scenarios `OT-01` through `OT-15` in [`tests/manual_release_matrix.md`](../../tests/manual_release_matrix.md) have not all been rerun as multi-turn agent sessions. Research OT, Prototype OT, 4022(f), project-only, cost-only, end-to-end, fixed, cost-type, mixed, contribution, pending-decision, revision, and rejected-key paths remain open across the required client matrix.

No live federal API was called during package testing. This avoided shared-key risk, but means live keyed startup, authentication failure, provider rate-limit behavior, and call-timestamp evidence still require the serialized manual release run.

## Historical release decision (before RC5 stabilization)

Static packaging and the available Codex control tests pass. The authenticated cross-client and end-to-end artifact matrix is incomplete, so `1.0.0` is blocked. The public preview is `1.0.0-rc.4`.

## RC5 stabilization evidence — 2026-08-22

Current maintained public-preview support is Codex and Claude Code (in the
Claude Desktop app or standalone CLI). Copilot CLI and VS Code/Copilot entries
in the historical checkpoint above are compatibility observations, not current
support gates.

The current public preview is `1.0.0-rc.5`, pinned to BLS OEWS `1.0.5`, GSA
CALC+ `1.0.4`, and GSA Per Diem `1.0.5`. Codex and Claude Code passed the
authority, contribution, successful-completion/follow-on, approved milestone
handoff, payment-structure, and missing-capability boundaries. Claude Desktop's
embedded Code binary independently passed the explicit authority boundary, and
Opus 5 fast mode independently passed the contribution and follow-on cases.

The generated Word instructions now match the tested dynamic-TOC refresh:
`Cmd+A`, then `Fn+F9` on Mac; `Ctrl+A`, then `F9` on Windows. The representative
13-page project description and 179-formula cost workbook passed document and
workbook structure, independent recomputation, serialized LibreOffice
recalculation, extraction, and full visual review. The first simultaneous
LibreOffice launch collided; the isolated serialized rerun passed and no agent
behavior changed.

The full authenticated OT matrix remains a final `1.0.0` gate. The replayable
RC5 inventory is [`../../tests/manual/rc5_closure_ledger.json`](../../tests/manual/rc5_closure_ledger.json).
