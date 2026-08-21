# Other Transaction Agent

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

Labor pricing requires both BLS OEWS and GSA CALC+. GSA Per Diem is required only when travel is in scope.

## Invocation

- Codex: `$other-transaction-workflow`
- Claude Code: `/other-transaction-agent:other-transaction-workflow`
- Copilot: select `other-transaction-agent` or explicitly request `other-transaction-workflow`

See the repository [README](../../README.md) for installation, optional-key setup, architecture, and release status. See [`test.md`](test.md) for exact evidence and open gates.
