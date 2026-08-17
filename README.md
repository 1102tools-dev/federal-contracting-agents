# 1102tools Agents

**Coming soon.** Pre-composed AI agents for federal contracting, packaged as installable plugin bundles. Each agent wires the orchestration skills from [federal-contracting-skills](https://github.com/1102tools-dev/federal-contracting-skills) to the MCP data servers from [federal-contracting-mcps](https://github.com/1102tools-dev/federal-contracting-mcps), so what you install is not a box of parts but a working unit: a cost analyst, a scope builder, an OT toolkit.

Website: [1102tools.com](https://1102tools.com)

[![Promo banner: Agents just got a standard. On August 6, OpenAI, AWS, Microsoft, GitHub, Cursor, and Vercel published Agent Plugins 1.0, an open standard that packs skills and MCP servers into one installable folder. The next 1102tools repo ships federal contracting agents in that format, pre-composed from the same free skills and servers, with Claude Code's plugin format alongside. Panel shows three IGCE skills plus three pricing MCP servers combining into an IGCE Cost Analyst agent, with SOW/PWS Builder and OT Toolkit queued behind it.](docs/agents-promo.png)](https://1102tools.com)

## The standard this builds on

On August 6, 2026, OpenAI, together with AWS, Microsoft, GitHub, Cursor, and Vercel, published **[Agent Plugins 1.0](https://agent-plugins.org)**: an open, vendor-neutral standard for packaging agent capabilities. One folder holds Agent Skills and MCP server configuration; compatible clients (ChatGPT, Codex, Cursor, GitHub Copilot, VS Code, Kiro) discover and install it directly.

That was the missing layer. Skills went portable. MCP became the universal data protocol. Agent Plugins is the composition standard on top: the piece that turns "install these six skills and eight servers" into "install this agent."

Every agent in this repo ships as an Agent Plugins 1.0 package first. If your platform reads the standard, one folder gets you the skills, the data servers, and the wiring between them.

## Claude gets its own build

Claude Code has its own plugin and marketplace format, and it carries a component the open standard does not: agent persona files with explicit routing logic. Each agent folder here will include the Claude Code manifest and persona alongside the standard package, same folder, no separate download. When the packages land, this repo becomes installable as a Claude Code marketplace:

```
/plugin marketplace add 1102tools-dev/federal-contracting-agents
```

## The planned lineup

| Agent | What it bundles |
|-------|-----------------|
| **IGCE Cost Analyst** | The three IGCE builder skills (FFP, LH/T&M, cost-reimbursement) with the BLS OEWS, GSA CALC+, and GSA Per Diem servers. Routes to the right pricing model by contract type and never blends them. |
| **SOW/PWS Builder** | The scope decision skill, producing a contract-file-ready SOW or PWS and the chat-only staffing handoff the cost analyst consumes. |
| **OT Toolkit** | OT project description and OT cost analysis skills with the pricing servers, for other transactions outside the FAR. |

The compositions follow the architecture diagram in the skills repo: these agents are those chains, packaged.

## The parts

- Skills: [federal-contracting-skills](https://github.com/1102tools-dev/federal-contracting-skills)
- Data servers: [federal-contracting-mcps](https://github.com/1102tools-dev/federal-contracting-mcps)

Same terms as everything else under 1102tools: free, open source, no signup. Watch the repo for the release.
