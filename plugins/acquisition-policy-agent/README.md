# Acquisition Policy Agent

Version `1.0.0-rc.2`

The Acquisition Policy Agent combines one host-neutral workflow with four source-specific federal MCP servers:

- eCFR `1.0.4` for the codified baseline and version comparisons;
- Federal Register `1.0.3` for proposed and final rules, effective dates, notices, and rulemaking history;
- Regulations.gov `1.0.3` for docket confirmation and public-comment evidence;
- Acquisition.gov `1.0.0` for RFO model text, approved guidance, and agency deviations posted to the official index.

Use `$acquisition-policy-workflow` in Codex, `/acquisition-policy-agent:acquisition-policy-workflow` in Claude Code, or select the installed custom agent in Copilot. A vague request produces the complete ten-choice workflow menu; a clear request routes directly and asks only for missing framing.

The agent produces sourced chat findings and, when requested and approved, a validated Acquisition Policy Impact Brief `.docx`. It supports government, industry, and neutral lenses without changing the underlying facts.

## Credentials and pacing

The plugin never stores `REGULATIONS_GOV_API_KEY`. Export the key in the environment that launches the client or use the client credential surface. The Regulations.gov MCP retains its clearly labeled, limited `DEMO_KEY` fallback.

The package sets three-second pacing for eCFR, Federal Register, and Acquisition.gov, and four seconds for Regulations.gov.

## Boundary

This agent reports what published sources document. It does not provide legal advice, decide procurement-specific applicability, select clauses, perform market research, analyze opportunities, build IGCEs, or perform grants or cooperative-agreement work. RFO model text is not labeled operative without an agency deviation.

See [test.md](test.md) for passed deterministic checks and open release gates.
