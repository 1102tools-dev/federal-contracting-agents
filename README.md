# 1102tools Agents

**Coming soon.** Two pre-composed agents for federal pre-award work. Each one connects the orchestration packages from [federal-contracting-skills](https://github.com/1102tools-dev/federal-contracting-skills) to the MCP data servers from [federal-contracting-mcps](https://github.com/1102tools-dev/federal-contracting-mcps), then adds the routing needed to carry one workflow into the next.

Website: [1102tools.com](https://1102tools.com)

## The two agents

| Agent | What it bundles |
|-------|-----------------|
| **Pre-Award Agent** | SOW/PWS Builder plus the separate FFP, LH/T&M, and cost-reimbursement IGCE skills, connected to BLS OEWS, GSA CALC+, and GSA Per Diem. Supports scope-only, pricing-only, and end-to-end SOW/PWS-to-IGCE workflows. |
| **Other Transaction Agent** | OT Project Description Builder plus OT Cost Analysis, connected to the same pricing data servers. Supports project-description-only, cost-only, and end-to-end OT planning workflows. |

The Pre-Award Agent consolidates the workflow, not the pricing methods. Firm-fixed-price work routes only to the FFP skill, labor-hour and time-and-materials work routes only to the LH/T&M skill, and cost-reimbursement work routes only to the CR skill. Hybrid acquisitions are separated by CLIN and remain visibly separate. Contract type stays a user or Contracting Officer decision.

The Other Transaction Agent applies the same principle. Research, prototype, and follow-on production authorities remain distinct, and authority, participant status, contribution treatment, and agreement determinations stay with the user or Agreements Officer. The agent composes the approved project-description and cost-analysis workflows without inventing those decisions.

## Why the skills came first

An agent is only as reliable as the capabilities underneath it. The six skills were originally released in April 2026 as dense, single-file instructions, with some pricing skills reaching roughly 10,000 to 18,000 tokens. Packaging those files immediately would have wrapped the original technical debt instead of fixing it.

Before agent development began, all six skills were modernized into portable, progressive-disclosure packages. Each capability now includes:

- A compact `SKILL.md` orchestration core with its load-bearing gates front-loaded
- One-level `references/` for detailed rules, specifications, and runtime adaptation
- Deterministic validators for workbook or document artifacts
- OpenAI client metadata without forking the shared skill body
- A current `test.md` recording models, clients, fixtures, injected faults, results, and open coverage

OpenAI Codex using GPT-5.6 Sol completed the modernization and testing pass. Behavioral gates were exercised in Codex CLI with GPT-5.6 Sol at xhigh reasoning and Claude Code CLI with Opus 5. FFP also received claude.ai Opus 5 Max and Codex Desktop coverage. Pricing fixtures passed formula-structure audits, independent recomputation, and LibreOffice formula execution; document fixtures passed deterministic validation and all-page rendering review.

That foundation is now in place. The agents will compose the tested skill packages rather than duplicate their instructions or maintain separate Claude and Codex versions. The skills remain independently installable for users who want only one capability.

## The packaging standard

**[Agent Plugins 1.0](https://agent-plugins.org)** defines an open, vendor-neutral package format for Agent Skills and MCP server configuration. A portable plugin uses one manifest, a `skills/` directory, and an optional `mcp.json`; compatible clients can discover the component types they support.

Each 1102tools agent will ship as an Agent Plugins package first. Client-specific behavior will remain a thin overlay around the same shared skills rather than a fork of the acquisition logic.

## Claude gets an overlay

Claude Code has its own plugin and marketplace format, including agent persona files with explicit routing logic. Each agent folder will include the Claude Code manifest and persona alongside the portable package, with no separate skill implementation. When the packages land, this repo will become installable as a Claude Code marketplace:

```
/plugin marketplace add 1102tools-dev/federal-contracting-agents
```

## The parts

- Skills: [federal-contracting-skills](https://github.com/1102tools-dev/federal-contracting-skills)
- Data servers: [federal-contracting-mcps](https://github.com/1102tools-dev/federal-contracting-mcps)

Same terms as everything else under 1102tools: free, open source, no signup. The skills foundation is complete; agent composition and cross-client packaging are next. Watch the repo for the release.
