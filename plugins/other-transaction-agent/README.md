# Other Transaction Agent

Stable release `1.0.12`.

Every new invocation first performs local, presence-only readiness checks for BLS OEWS and GSA Per Diem. With no `BLS_API_KEY`, BLS remains available through its limited v1 fallback: 25 requests per day and 10 years per query. With no `PERDIEM_API_KEY`, Per Diem uses the shared `DEMO_KEY`, limited to approximately 10 requests per hour. The agent discloses those limits before its workflow choices, never requests a key in chat, and links to [credential setup](https://1102tools.com/setup#credentials). Project-description-only work and keyless GSA CALC+ remain available.

The Other Transaction Agent creates an OT project description and carries its approved milestones into an auditable cost analysis without manual handoff copying.

## Included capabilities

- `other-transaction-workflow`, the portable orchestrator
- `ot-project-description-builder`
- `ot-cost-analysis`
- BLS OEWS, GSA CALC+, and GSA Per Diem MCP configuration

Every skill is a complete multi-file runtime package with its references, deterministic validators, scripts, and OpenAI metadata. The installed package does not reach outside this directory.

## Modes

1. Project-description-only creation
2. Cost-analysis-only creation
3. End-to-end project-description to cost-analysis creation
4. User-directed milestone revision and recosting

End-to-end mode preserves milestone IDs, durations, deliverables, completion evidence, payment types, locations, authority facts, contribution treatment, overrides, and pending decisions. It asks for transition approval before cost analysis and asks only for missing downstream inputs.

## Outputs

- A validated OT project-description `.docx`
- A separate validated cost-analysis `.xlsx`
- A completion record listing the approved handoff version, validators, and any unavailable validation layer

The milestone handoff is an internal chat workpaper and never enters either artifact.

## Boundaries

The agent does not originate Agreements Officer authority, participant-status, successful-completion, contribution, price-reasonableness, or follow-on eligibility determinations. Missing required pricing capabilities stop cost analysis; the agent does not improvise a public API substitute.

Labor pricing requires both BLS OEWS and GSA CALC+. GSA Per Diem is used only when travel is in scope. Missing optional keys limit the affected source; they do not silently disable the agent.

## Invocation

- Codex: `$other-transaction-workflow`
- Claude Code: `/other-transaction-agent:other-transaction-workflow`

Codex Desktop/CLI and Claude Code in Claude Desktop/CLI are the maintained stable paths. Other compatible clients are self-supported.

See the repository [README](../../README.md) for installation, optional-key setup, architecture, and supported-surface differences. See [`test.md`](test.md) for the stable qualification record and historical RC evidence.
