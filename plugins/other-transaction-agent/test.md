# Other Transaction Agent Release-Candidate Test Record

Date: August 21, 2026

Package: `other-transaction-agent` `1.0.0-rc.2`

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
- All three bundled skills passed the skill validator
- Six deterministic orchestrator contract tests passed repository-wide
- All three bundled Python validators or recomputation scripts compiled in a temporary directory and returned command-line help
- MCP process startup and tool discovery, without invoking any tool or upstream API: BLS OEWS 7 tools, GSA CALC+ 8 tools, GSA Per Diem 6 tools

The source MCP releases also passed their pacing regression suites before publication: BLS OEWS had 85 passing tests with 164 network tests skipped, and GSA Per Diem had 186 passing tests with 255 network tests skipped. The plugin sets the three-second pacing floor for both credentialed servers.

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

## Client installation and blockers

| Surface | Result |
|---|---|
| Codex CLI | Clean `1.0.0-rc.2` marketplace installation, package inventory, skill discovery, and MCP discovery passed; the `rc.1` explicit routing, natural-language routing, and post-install missing-capability evidence remains applicable because the runtime components are unchanged |
| Codex Desktop | Plugin was installed locally, but a clean new-task end-to-end artifact run remains pending |
| Claude Code | Clean marketplace installation of `1.0.0-rc.2`, strict validation, and package inventory passed; model runs remain blocked because the OAuth session is expired and cannot refresh |
| Copilot CLI | Clean marketplace installation of `1.0.0-rc.2` and plugin inventory passed; model runs remain blocked because no supported OAuth or fine-grained token is configured |
| VS Code/Copilot | Installation, discovery, and representative workflow remain pending |

When both 1102tools plugins are installed, Codex 0.149.0-alpha.4 reports duplicate MCP-name warnings for the three shared servers and resolves one configuration for each name. Both package configurations are byte-for-byte equivalent at the semantic server level, and repository validation rejects drift. This warning is recorded as current client behavior.

## Unexecuted release gates

The full manual scenarios `OT-01` through `OT-15` in [`tests/manual_release_matrix.md`](../../tests/manual_release_matrix.md) have not all been rerun as multi-turn agent sessions. Research OT, Prototype OT, 4022(f), project-only, cost-only, end-to-end, fixed, cost-type, mixed, contribution, pending-decision, revision, and rejected-key paths remain open across the required client matrix.

No live federal API was called during package testing. This avoided shared-key risk, but means live keyed startup, authentication failure, provider rate-limit behavior, and call-timestamp evidence still require the serialized manual release run.

## Release decision

Static packaging and the available Codex control tests pass. The authenticated cross-client and end-to-end artifact matrix is incomplete, so `1.0.0` is blocked. The public preview is `1.0.0-rc.2`.
