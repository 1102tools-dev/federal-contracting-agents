# Market Research Agent test record

Version: `1.0.0-rc.2`
Evidence date: August 21, 2026

## Canonical skill evidence

The bundled `market-research-builder` runtime is synchronized from `federal-contracting-skills` commit `6337508992730f9d670c7e69eebf4174f287eb31`. Its canonical `test.md` records:

- Sixteen deterministic repository tests, both artifact builders, LibreOffice conversion, extraction, citation, recomputation, and portable-skill validation.
- All four provider modes, approved fallback, prohibited provider and tool use, private and credential-bearing URL rejection, and prompt-injection/document-precedence controls.
- The complete menu, document-intake stop, four provider choices, sanitized terms and URLs, third-party disclosure, and no pre-approval research in Codex CLI `0.149.0-alpha.4` with GPT-5.6 Sol at xhigh and Claude Code `2.1.239` with `claude-opus-5` at max effort.
- A Sonnet packaged-plugin smoke initially exposed an omitted selection question. The exact question was moved into the front-loaded core; a fresh `claude-sonnet-5` max-effort run then returned the six choices and exact question with zero web-search and web-fetch requests.

No live federal API call was made.

## Package and remote-MCP evidence

Passed:

- Agent Plugins 1.0 schemas, all portable/native manifests, exact federal package pins, pacing values, references, component hashes, bundled scripts, and credential hygiene.
- Tavily is confined to the two research agents. Portable configuration uses the exact Streamable HTTP endpoint and keyless header; Claude-native configuration is equivalent with `type: http`.
- Live keyless initialization and `tools/list` completed without OAuth and without invoking a tool. The server advertised five operations and produced schema SHA-256 `f28255db8e816ce522e9bd20a89b6fcf2312af41e60c3846799e9c3195e60992`. The required `tavily_search` and `tavily_extract` operations were present.
- The current keyless endpoint also advertises `tavily_crawl`, `tavily_map`, and `tavily_research`. The skill and record validator prohibit all three; this upstream tool-surface mismatch is recorded in `components.lock.json`.
- One approved, non-sensitive Market Research Tavily search was sent for `official FAR Part 10 market research guidance`, restricted to `acquisition.gov`. Tavily returned a `CallToolResult`; the local evidence formatter then used the wrong Python attribute name and failed before retaining the response text. No repeat query was made. The equivalent native-only run independently verified the underlying Acquisition.gov pages.
- Clean isolated installation and `1.0.0-rc.2` inventory passed in Codex CLI, Claude Code, and GitHub Copilot CLI `1.0.80`. Claude resolved one skill, one native agent, and the expected SAM.gov, USASpending, and Tavily servers.

## Installed-client behavior

- Codex session `01a0275a-09cc-7a70-b8a1-dbdefa9b8309` used the installed plugin, showed the menu, stopped for document intake, displayed the complete provider approval, and honored `Native search only`. It made exactly one approved Acquisition.gov search, fetched the approved official pages, cited the underlying FAR pages, and made zero Tavily and zero federal MCP calls.
- Claude Opus 5 Max loaded the packaged plugin and returned the complete recommended menu with zero web-search and web-fetch requests.
- Claude Sonnet 5 Max passed the corrected exact-question regression with zero web-search and web-fetch requests.
- When both research agents are installed, Codex `0.149.0-alpha.4` warns that their intentionally shared semantic MCP names collide and selects one identical definition. The workflows remained functional, but the warning is retained as a preview limitation.

## Open release-candidate gates

- Codex Desktop has not been independently rerun after `rc.2`.
- The VS Code CLI is not installed on this machine, so VS Code/Copilot installation remains open.
- Copilot installation passed, but a representative authenticated workflow remains open.
- Tavily-only failure and combined-mode fallback are covered deterministically, not by manufacturing a live provider outage.
- The Market Tavily response content was not retained because of the local formatter error described above; direct content/citation capture remains an `rc` evidence gap.
- Full implicit-routing, upload-only-client, commercial-evidence, and client-generated report scenarios remain open.

These gaps block final `1.0.0`; they do not block this repository-marketplace release candidate.
