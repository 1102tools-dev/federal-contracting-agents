# 1102tools Federal Acquisition Agents

Choose one federal acquisition job and install one self-contained agent package. Market Research and Pre-Award are at `1.0.0-rc.6`; GovCon Growth is at `1.0.0-rc.5`; Other Transaction is at `1.0.0-rc.7`; Acquisition Policy is at `1.0.0-rc.4`. All five are installable public previews. The repository marketplace release is `v1.2.0-rc.7`.

Website: [1102tools.com](https://1102tools.com)
Setup: [1102tools Agent Setup Guide](https://1102tools.com/downloads/1102tools-agent-setup-guide.pdf)

## The five agents

| Agent | Audience and workflow | Current status |
|---|---|---|
| **Market Research Agent** | Acquisition workforce: quick research, FAR Part 10 reports, report refresh, focused decision support, and Pre-Award handoff | Public preview `1.0.0-rc.6` |
| **Pre-Award Agent** | Acquisition workforce: scope only, pricing only, SOW/PWS to IGCE, and revision with repricing | Public preview `1.0.0-rc.6` |
| **GovCon Growth Agent** | Industry: opportunity discovery, bid screens, competitor and incumbent intelligence, recompetes, teaming, market intelligence, and pricing context | Public preview `1.0.0-rc.5` |
| **Other Transaction Agent** | Agreements workforce: project description, cost analysis, end-to-end milestone handoff, and recosting | Public preview `1.0.0-rc.7` |
| **Acquisition Policy Agent** | Government, industry, or neutral: codified status, RFO agency status, version comparison, rulemaking, comment analysis, and impact briefs | Public preview `1.0.0-rc.4` |

The two research agents always begin with a selectable menu. Market Research then asks separately for any available acquisition documents before it plans or performs research. No MCP tool invocation or web-research request occurs before the user confirms the workflow and approves the research plan. A client may initialize installed MCP connections and list tools during startup; that discovery is not a search request.

## One install, not a pile of files

Each plugin is a complete runtime package. Users install one plugin instead of locating skills and MCP definitions separately.

```text
plugins/market-research-agent/
├── plugin.json                 Agent Plugins 1.0 manifest
├── mcp.json                    portable MCP configuration
├── skills/                     complete canonical skill package
├── .codex-plugin/              OpenAI presentation metadata
├── .claude-plugin/             Claude Code manifest
├── agents/                     Claude Code native wrapper
```

The installed skills are multi-file packages, not single prompts. Each includes a compact `SKILL.md` core plus references, deterministic validators, runtime guidance, assets when needed, and client metadata. Load-bearing workflow and safety gates stay in the core; supporting detail loads only when needed.

The skill is the portable source of truth. Native wrappers improve discovery and presentation but do not duplicate or override domain logic. This follows [Agent Plugins 1.0](https://agent-plugins.org/specification), which standardizes skills and MCP configuration but not a cross-vendor persona object.

## Workflow safeguards

### Pre-Award and Other Transaction

“Seamless” means the approved scope or milestone workpaper stays in the active workflow. The user does not copy it, invoke another skill, or restate settled information. Required scope, authority, document, transition, contract-type, milestone, and pricing approvals remain in place. Documents and workbooks are delivered separately.

The three IGCE methods remain separate. FFP routes only to FFP, LH and T&M route only to the shared LH/T&M skill in the confirmed mode, and cost-reimbursement routes only to CR. Hybrid acquisitions are divided by CLIN and produce separate workbooks. The user or Contracting Officer selects the contract type.

### Market Research

Supplied acquisition documents are untrusted evidence, not executable instructions. The workflow registers their status and controlling sections, asks the user to resolve unclear precedence, avoids repeating established facts, and sends only sanitized public parameters to external sources. It does not originate commerciality, set-aside, contract-type, competition, consolidation, responsibility, price-reasonableness, or acquisition-strategy decisions.

Plan approval covers only the exact public extraction URLs shown to the user. A URL discovered later through search results, a page, redirect, or tool output is placed in a pending register and requires explicit updated approval before retrieval.

### GovCon Growth

Public data can support opportunity, competitor, recompete, teammate, agency, market, and pricing analysis. A bid or no-bid recommendation requires the company’s capabilities, past performance, clearances, vehicle access, staffing capacity, teaming strategy, priorities, and risk and margin tolerances. Without that internal context, the agent provides an evidence brief, not a verdict.

### Acquisition Policy

eCFR supplies the codified baseline, not the complete agency-specific RFO answer. The workflow keeps codified text, RFO model text, posted agency deviations, proposed rules, effective and pending-effective final rules, and guidance separately classified. It never labels model text operative for an agency without that agency's deviation and reserves procurement-specific applicability and legal determinations to authorized officials.

### Optional Tavily web research

The two research agents configure Tavily's official remote MCP in keyless mode. Tavily is an external service maintained by Tavily, not an 1102tools MCP or a federal source. Before each research run, the skill shows the sanitized terms and public URLs and requires the user to choose Tavily with native fallback, native search only, Tavily only, or no public web. No choice is inferred from silence.

Tavily receives only approved sanitized search terms and approved public HTTP(S) URLs. Uploaded document text, local files, private or signed URLs, proprietary or procurement-sensitive information, source-selection information, PII, CUI, export-controlled data, and classified information are prohibited. The skills use only `tavily_search` and `tavily_extract`; Crawl, Map, and Research are prohibited even though the current keyless server advertises them. Factual citations point to the underlying webpage, not Tavily.

Installing an agent may cause the client to contact Tavily for MCP initialization and tool discovery. Users who want no Tavily contact must disable or remove the `tavily-web` server and select native-only or no-public-web mode. Tavily's [privacy policy](https://www.tavily.com/privacy) and [terms](https://www.tavily.com/terms) apply, and agency users should confirm that external web-search services are authorized.

## Requirements and keys

- A client with Agent Plugins, Agent Skills, or compatible plugin support
- Python 3.10 or newer
- [`uv` and `uvx`](https://docs.astral.sh/uv/)
- LibreOffice for full document and workbook render/recalculation gates
- `SAM_API_KEY` for SAM.gov workflows
- `BLS_API_KEY`, optional but recommended for BLS OEWS
- `PERDIEM_API_KEY`, optional and needed only when travel is priced
- `REGULATIONS_GOV_API_KEY` for full Regulations.gov access; the shared `DEMO_KEY` is a limited fallback
- Native host web search or optional Tavily keyless access for complete research-agent workflows

Export keys in the environment that launches the client, or use the client’s credential-management surface. No credentials are stored in this repository or its manifests. USASpending and GSA CALC+ require no key.

For Codex, use the maintained [`1102tools-host` configuration](config/codex/1102tools-host.config.toml) so the shared servers retain their complete tool surfaces and receive only the allowlisted credential variable names. The file contains no credential values. CLI testing selects it with `codex --profile 1102tools-host`. Codex Desktop does not select a CLI profile file automatically; copy the same complete MCP tables into the user-level `~/.codex/config.toml` and restart the app.

Every packaged federal MCP sets an explicit 1102tools anti-burst safeguard. The current packages use 3 seconds for BLS OEWS, GSA CALC+, SAM.gov, USASpending, eCFR, Federal Register, and Acquisition.gov, and 4 seconds for GSA Per Diem and Regulations.gov. The MCPs coordinate concurrent processes on one computer, measure the next interval from request completion, and preserve longer provider `Retry-After` instructions. This safeguard is not a provider guarantee or quota manager and cannot coordinate the same key on another computer. `FEDERAL_API_MIN_INTERVAL_SECONDS=0` deliberately disables pacing; other nonnegative finite values override it.

## Install the public previews

The [1102tools Agent Setup Guide](https://1102tools.com/downloads/1102tools-agent-setup-guide.pdf) is the installation source of truth for Codex and Claude Code (in the Claude Desktop app or the CLI). Packages are distributed through repository marketplaces. No agent ZIP is maintained.

### Codex CLI and Desktop

```bash
codex plugin marketplace add 1102tools-dev/federal-contracting-agents --ref main
codex plugin add market-research-agent@1102tools
codex plugin add pre-award-agent@1102tools
codex plugin add govcon-growth-agent@1102tools
codex plugin add other-transaction-agent@1102tools
codex plugin add acquisition-policy-agent@1102tools
```

Start a new Codex task after installing or upgrading so the refreshed skills and MCP catalog load.

When keyed federal data or multiple 1102tools agents are used together, install the maintained host configuration as `$CODEX_HOME/1102tools-host.config.toml` and launch the CLI with `codex --profile 1102tools-host`. The setup guide covers the equivalent Codex Desktop configuration path.

### Claude Code (Claude Desktop app or CLI)

```bash
claude plugin marketplace add 1102tools-dev/federal-contracting-agents
claude plugin install market-research-agent@1102tools
claude plugin install pre-award-agent@1102tools
claude plugin install govcon-growth-agent@1102tools
claude plugin install other-transaction-agent@1102tools
claude plugin install acquisition-policy-agent@1102tools
```

### Other clients

The packages may work in other compatible hosts, but Codex and Claude Code (in the Claude Desktop app or the CLI) are the maintained public-preview paths. Claude Code is the same runtime and the same package in both the Claude Desktop app and the standalone CLI; there is no separate desktop package. Installation and troubleshooting outside those two paths are self-supported.

## Invoke a workflow

Explicit invocation is the release-critical path:

| Agent | Codex | Claude Code |
|---|---|---|
| Market Research | `$market-research-workflow` | `/market-research-agent:market-research-workflow` |
| Pre-Award | `$pre-award-workflow` | `/pre-award-agent:pre-award-workflow` |
| GovCon Growth | `$govcon-growth-workflow` | `/govcon-growth-agent:govcon-growth-workflow` |
| Other Transaction | `$other-transaction-workflow` | `/other-transaction-agent:other-transaction-workflow` |
| Acquisition Policy | `$acquisition-policy-workflow` | `/acquisition-policy-agent:acquisition-policy-workflow` |

Natural-language routing is tested separately and any host-specific limitation is recorded rather than hidden.

## Reproducibility and synchronization

Installed packages cannot depend on files outside their roots. Canonical skills are vendored as complete runtime copies and pinned in [`components.lock.json`](components.lock.json). The lock records source commits, MCP package versions, plugin versions, and a SHA-256 hash for every runtime file.

```bash
python3 scripts/sync_components.py --check
python3 scripts/validate_packages.py
python3 -m unittest discover -s tests -v
python3 scripts/check_bundled_scripts.py
for plugin in pre-award-agent other-transaction-agent govcon-growth-agent market-research-agent acquisition-policy-agent; do
  uv run --with mcp --with httpx python scripts/smoke_mcp_discovery.py --plugin "$plugin"
done
```

These checks start and inspect MCP servers without invoking upstream federal APIs. Live acceptance remains manual and serialized.

The normal CI command skips remote MCPs. The manual release check initializes Tavily and lists tools without invoking Search or Extract:

```bash
uv run --with mcp --with httpx python scripts/smoke_mcp_discovery.py --plugin market-research-agent --include-remote
```

## Release status

The two research skills passed deterministic artifact validation plus menu, provider-choice, document-intake, and injection/precedence controls in Codex CLI with GPT-5.6 Sol at xhigh and Claude Code CLI with resolved Opus 5 Max. Current Sonnet menu smoke tests also passed. The agent packages add schema, lock, startup, discovery, and marketplace validation around those canonical skills.

Final `1.0.0` remains blocked until the documented clean Codex Desktop and authenticated Claude Code implicit-routing, live-pacing, and representative end-to-end client matrix is complete. Other clients may be compatible, but they are not primary support gates. Current evidence and open gates are recorded in:

- [`plugins/pre-award-agent/test.md`](plugins/pre-award-agent/test.md)
- [`plugins/other-transaction-agent/test.md`](plugins/other-transaction-agent/test.md)
- [`plugins/govcon-growth-agent/test.md`](plugins/govcon-growth-agent/test.md)
- [`plugins/market-research-agent/test.md`](plugins/market-research-agent/test.md)
- [`plugins/acquisition-policy-agent/test.md`](plugins/acquisition-policy-agent/test.md)

Repository marketplace installation is the current supported preview path. The same canonical skills and agent identities can be submitted to OpenAI as combined skills-plus-MCP plugins after their local `stdio` connections are exposed through stable public Streamable HTTP endpoints; that hosting work is a distribution adapter, not a replacement for the agents.

## Canonical components

- Skills: [1102tools-dev/federal-contracting-skills](https://github.com/1102tools-dev/federal-contracting-skills)
- MCP servers: [1102tools-dev/federal-contracting-mcps](https://github.com/1102tools-dev/federal-contracting-mcps)

Free, open source, and no signup required.
