# GovCon Growth Agent

Stable release `1.0.4`.

This self-contained Agent Plugins 1.0 package installs one authoritative multi-file skill, pinned SAM.gov, USASpending, and GSA CALC+ MCP definitions, plus Tavily's optional official keyless remote MCP. It supports opportunity discovery, bid screens, competitor and incumbent analysis, recompete radar, teaming research, agency and market intelligence, pricing context, and prior-research refreshes.

Every new invocation first performs a local, presence-only SAM.gov readiness check. If `SAM_API_KEY` is absent, the agent says so before the nine-choice workflow menu, links to [credential setup](https://1102tools.com/setup#credentials), and makes no SAM.gov data call. SAM-specific work stops until the key is configured outside chat and the client is restarted; keyless USASpending, CALC+, and explicitly approved web routes remain available.

The agent never asks the user to paste a key into chat and never describes a missing key as a SAM.gov outage. SAM is needed only for SAM-specific modes, and CALC+ only for pricing context. The workflow uses the minimum required tool surface.

Before public web research, the agent shows the sanitized search terms and public URLs and requires a provider choice: Native web only (Recommended), Native web with Tavily fallback, Tavily only, or No public web. Tavily is a third-party service and is never an inferred fallback. The workflow uses only `tavily_search` and `tavily_extract`, cites underlying pages, and never sends internal company documents or sensitive data to a public search provider. Installing the plugin may contact Tavily for MCP startup discovery; users who want no Tavily contact must disable or remove `tavily-web`.

A bid recommendation requires internal company capabilities, past performance, clearances and certifications, vehicle access, staffing and geographic capacity, teaming strategy, strategic priorities, and risk and margin tolerances. Without that context, the agent produces an evidence brief and no verdict.

Install and update through the [1102tools Agent Setup Guide](https://1102tools.com/downloads/1102tools-agent-setup-guide.pdf). Codex Desktop/CLI and Claude Code in Claude Desktop/CLI are the maintained stable paths. Other compatible clients are self-supported. No plugin ZIP is maintained.

Current test evidence and limitations are in [test.md](test.md).
