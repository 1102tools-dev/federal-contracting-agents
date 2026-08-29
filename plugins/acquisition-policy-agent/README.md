# Acquisition Policy Agent

Stable release `1.0.9`.

The Acquisition Policy Agent combines one host-neutral workflow with four source-specific federal MCP servers:

- eCFR `1.0.5` for the codified baseline and version comparisons;
- Federal Register `1.0.4` for proposed and final rules, effective dates, notices, and rulemaking history;
- Regulations.gov `1.0.8` for docket confirmation and public-comment evidence;
- Acquisition.gov `1.0.1` for RFO model text, approved guidance, and agency deviations posted to the official index.

Use `$acquisition-policy-workflow` in Codex or `/acquisition-policy-agent:acquisition-policy-workflow` in Claude Code. Codex Desktop/CLI and Claude Code in Claude Desktop/CLI are the maintained stable paths; other compatible clients are self-supported. A vague request produces the complete ten-choice workflow menu; a clear request routes directly and asks only for missing framing.

The agent produces sourced chat findings and, when requested and approved, a validated Acquisition Policy Impact Brief `.docx`. It supports government, industry, and neutral lenses without changing the underlying facts.

## Credentials and pacing

Every new invocation first performs a local, presence-only Regulations.gov readiness check. If `REGULATIONS_GOV_API_KEY` is absent, the agent says so before its menu or routed answer and explains that the shared `DEMO_KEY` fallback is limited to approximately 10 requests per hour. It links to [credential setup](https://1102tools.com/setup#credentials), never asks for a key in chat, and does not describe the fallback limit as an outage.

The plugin never stores `REGULATIONS_GOV_API_KEY`. Configure the key in the environment that launches the client or in the client credential surface, restart the client, and rerun the readiness check.

The package sets three-second pacing for eCFR, Federal Register, and Acquisition.gov, and four seconds for Regulations.gov.

## Boundary

This agent reports what published sources document. It does not provide legal advice, decide procurement-specific applicability, select clauses, perform market research, analyze opportunities, build IGCEs, or perform grants or cooperative-agreement work. RFO model text is not labeled operative without an agency deviation.

See [test.md](test.md) for the stable qualification record and historical RC evidence.
