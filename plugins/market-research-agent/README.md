# Market Research Agent

Stable release `1.0.12`.

This self-contained Agent Plugins 1.0 package installs one authoritative multi-file skill, pinned SAM.gov and USASpending MCP definitions, plus Tavily's optional official keyless remote MCP. It supports quick research, a complete FAR Part 10 report, refreshes, one-question analysis, and a structured Pre-Award Agent handoff.

Every new invocation first performs a local, presence-only SAM.gov readiness check. If `SAM_API_KEY` is absent, the agent says so before the six-choice workflow menu, links to [credential setup](https://1102tools.com/setup#credentials), and makes no SAM.gov data call. SAM-specific work stops until the key is configured outside chat and the client is restarted; explicitly approved USASpending, supplied-document, and web routes remain available.

The second turn is always a separate question about existing acquisition documents. Research starts only after the user confirms the source register and approves the research plan. The agent never asks the user to paste a key into chat and never describes a missing key as a SAM.gov outage.

Before public web research, the agent shows the sanitized search terms and public URLs and requires a provider choice: Native web only (Recommended), Native web with Tavily fallback, Tavily only, or No public web. Tavily is a third-party service and is never an inferred fallback. The workflow uses only `tavily_search` and `tavily_extract`, cites underlying pages, and never sends acquisition-document text or sensitive data to a public search provider. Installing the plugin may contact Tavily for MCP startup discovery; users who want no Tavily contact must disable or remove `tavily-web`.

The skill may organize evidence and record an authorized user's acquisition decisions. It does not originate commerciality, set-aside, contract-type, competition, consolidation, responsibility, price-reasonableness, or acquisition-strategy determinations.

Install and update through the [1102tools Agent Setup Guide](https://1102tools.com/downloads/1102tools-agent-setup-guide.pdf). Codex Desktop/CLI and Claude Code in Claude Desktop/CLI are the maintained stable paths. Other compatible clients are self-supported. No plugin ZIP is maintained.

Current test evidence and limitations are in [test.md](test.md).
