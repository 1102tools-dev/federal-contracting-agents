# GovCon Growth Agent

Public preview `1.0.0-rc.4`.

This self-contained Agent Plugins 1.0 package installs one authoritative multi-file skill, pinned SAM.gov, USASpending, and GSA CALC+ MCP definitions, plus Tavily's optional official keyless remote MCP. It supports opportunity discovery, bid screens, competitor and incumbent analysis, recompete radar, teaming research, agency and market intelligence, pricing context, and prior-research refreshes.

The first turn is always a nine-choice workflow menu. SAM is needed only for SAM-specific modes, and CALC+ only for pricing context. The workflow uses the minimum required tool surface.

Before public web research, the agent shows the sanitized search terms and public URLs and requires a provider choice: Tavily with native fallback, native only, Tavily only, or no public web. Tavily is a third-party service. The workflow uses only `tavily_search` and `tavily_extract`, cites underlying pages, and never sends internal company documents or sensitive data to a public search provider. Installing the plugin may contact Tavily for MCP startup discovery; users who want no Tavily contact must disable or remove `tavily-web`.

A bid recommendation requires internal company capabilities, past performance, clearances and certifications, vehicle access, staffing and geographic capacity, teaming strategy, strategic priorities, and risk and margin tolerances. Without that context, the agent produces an evidence brief and no verdict.

Install and update through the [1102tools Agent Setup Guide](https://1102tools.com/downloads/1102tools-agent-setup-guide.pdf). Codex and Claude Code (in the Claude Desktop app or the CLI) are the maintained public-preview paths. Other compatible clients are self-supported. No plugin ZIP is maintained.

Current test evidence and limitations are in [test.md](test.md).
