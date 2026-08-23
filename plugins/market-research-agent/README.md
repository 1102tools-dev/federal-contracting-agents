# Market Research Agent

Public preview `1.0.0-rc.7`.

This self-contained Agent Plugins 1.0 package installs one authoritative multi-file skill, pinned SAM.gov and USASpending MCP definitions, plus Tavily's optional official keyless remote MCP. It supports quick research, a complete FAR Part 10 report, refreshes, one-question analysis, and a structured Pre-Award Agent handoff.

The first turn is always a six-choice workflow menu. The second turn is always a separate question about existing acquisition documents. Research starts only after the user confirms the source register and approves the research plan.

Before public web research, the agent shows the sanitized search terms and public URLs and requires a provider choice: Tavily with native fallback, native only, Tavily only, or no public web. Tavily is a third-party service. The workflow uses only `tavily_search` and `tavily_extract`, cites underlying pages, and never sends acquisition-document text or sensitive data to a public search provider. Installing the plugin may contact Tavily for MCP startup discovery; users who want no Tavily contact must disable or remove `tavily-web`.

The skill may organize evidence and record an authorized user's acquisition decisions. It does not originate commerciality, set-aside, contract-type, competition, consolidation, responsibility, price-reasonableness, or acquisition-strategy determinations.

Install and update through the [1102tools Agent Setup Guide](https://1102tools.com/downloads/1102tools-agent-setup-guide.pdf). Codex and Claude Code (in the Claude Desktop app or the CLI) are the maintained public-preview paths. Other compatible clients are self-supported. No plugin ZIP is maintained.

Current test evidence and limitations are in [test.md](test.md).
