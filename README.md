# 1102tools Federal Contracting Agents

Choose one federal contracting job and install one self-contained agent package. The current 1102tools catalog contains three stable agents at `1.0.12`. The marketplace catalog is version `2.0.0`; that catalog version is separate from the package versions.

Website: [1102tools.com](https://1102tools.com)

Setup: [visible HTML instructions](https://1102tools.com/setup) · [downloadable PDF](https://1102tools.com/downloads/1102tools-agent-setup-guide.pdf)

## The three agents

| Agent | Audience and supported work | Version |
|---|---|---|
| **GovCon Growth Agent** | Industry: opportunity discovery, bid screens, competitor and incumbent intelligence, recompetes, teaming, market intelligence, and pricing context | `1.0.12` |
| **Pre-Award Agent** | Acquisition workforce: scope only, pricing only, SOW/PWS to IGCE, hybrid routing, and revision with repricing | `1.0.12` |
| **Other Transaction Agent** | Agreements workforce: project description, cost analysis, end-to-end milestone handoff, and recosting | `1.0.12` |

Each plugin vendors its complete canonical skills, deterministic validators, runtime guidance, and pinned MCP configuration. The skill is the portable source of truth. Native wrappers improve discovery and presentation without duplicating domain logic. The packages follow [Agent Plugins 1.0](https://agent-plugins.org/specification).

Market Research and Acquisition Policy are no longer distributed in this marketplace. Their stewardship is moving to [AcqAgent](https://github.com/acqagent).

## Distribution

The maintained distribution is this GitHub-hosted 1102tools marketplace. It is not an official OpenAI, Codex, Anthropic, or Claude storefront listing. No agent ZIP is maintained.

Standalone source components for the three retained agents remain available as advanced building blocks:

- [federal-contracting-skills](https://github.com/1102tools-dev/federal-contracting-skills)
- [federal-contracting-mcps](https://github.com/1102tools-dev/federal-contracting-mcps)

## Requirements and credentials

No 1102tools account is required. Some federal providers require a free account or API key. Every new agent invocation performs local, presence-only readiness checks before its workflow choices or routed response. The checks never display, transmit, log, or validate the credential value.

| Agent | Credential state without user keys | Startup behavior |
|---|---|---|
| GovCon Growth | `SAM_API_KEY` required for SAM.gov operations | Reports the missing key before the menu, blocks only SAM-dependent work, and permits an explicitly approved keyless scope |
| Pre-Award | `BLS_API_KEY` recommended; `PERDIEM_API_KEY` relevant when travel is priced | Warns about limited keyless fallbacks and permits bounded work |
| Other Transaction | `BLS_API_KEY` recommended; `PERDIEM_API_KEY` relevant when travel is priced | Uses the same limited-fallback warning; project-description-only work remains available |

USASpending and GSA CALC+ require no user key.

- Codex Desktop or Codex CLI, or Claude Code in Claude Desktop or its standalone CLI
- Python 3.10 or newer
- [`uv` and `uvx`](https://docs.astral.sh/uv/)
- LibreOffice for full document rendering and workbook recalculation gates
- `SAM_API_KEY` for SAM.gov workflows: [SAM.gov Help](https://sam.gov/help)
- `BLS_API_KEY`, optional but recommended: [BLS registration](https://data.bls.gov/registrationEngine/)
- `PERDIEM_API_KEY`, optional when travel is priced: [api.data.gov signup](https://api.data.gov/signup/)

Configure credentials outside chat in the environment that launches the client, then fully restart the client and rerun the workflow. Never paste a key into a conversation. Credentials are not stored in this repository or its manifests.

For Codex, the maintained [`1102tools-host` configuration](config/codex/1102tools-host.config.toml) is required when multiple 1102tools agents are installed together. It owns the complete definitions for the five federal MCP servers used by the three-agent catalog and contains credential variable names only, never values.

## Install

### Codex Desktop and CLI

```bash
codex plugin marketplace add 1102tools-dev/federal-contracting-agents --ref main
codex plugin add govcon-growth-agent@1102tools
codex plugin add pre-award-agent@1102tools
codex plugin add other-transaction-agent@1102tools
```

Install the complete [`1102tools-host` configuration](config/codex/1102tools-host.config.toml), then start a new Codex task.

### Claude Code in Claude Desktop or CLI

```bash
claude plugin marketplace add 1102tools-dev/federal-contracting-agents
claude plugin install govcon-growth-agent@1102tools
claude plugin install pre-award-agent@1102tools
claude plugin install other-transaction-agent@1102tools
```

Restart Claude Code or start a new session after installation.

## Update

Codex refreshes the marketplace and replaces each installed package:

```bash
codex plugin marketplace upgrade 1102tools
codex plugin remove govcon-growth-agent@1102tools
codex plugin add govcon-growth-agent@1102tools
```

Repeat the remove/add pair for each installed 1102tools agent. Claude Code supports direct updates:

```bash
claude plugin marketplace update 1102tools
claude plugin update govcon-growth-agent@1102tools
```

## Start an installed agent

Start a fresh task or session after installation.

- **Codex Desktop or CLI:** type `@`, begin typing the agent name, and select the matching agent.
- **Claude Code in Desktop or CLI:** type `/`, begin typing the agent name, and select its workflow.
- Press Enter once to load autocomplete, then press Enter again to send it. You may add an ordinary-language request before sending.

| Agent | Codex | Claude Code |
|---|---|---|
| GovCon Growth | `$govcon-growth-workflow` | `/govcon-growth-agent:govcon-growth-workflow` |
| Pre-Award | `$pre-award-workflow` | `/pre-award-agent:pre-award-workflow` |
| Other Transaction | `$other-transaction-workflow` | `/other-transaction-agent:other-transaction-workflow` |

## Workflow safeguards

- **Pre-Award and Other Transaction:** approved handoffs remain in the active workflow, but scope, authority, transition, contract-type, milestone, and pricing approvals remain mandatory. Documents and workbooks stay separate.
- **GovCon Growth:** public data supports evidence briefs. A bid recommendation requires the user's internal company context and remains the user's decision.
- **Public web:** Native web is recommended. Tavily is an explicitly selected third-party option, never a silent fallback.

## Qualification and reproducibility

Historical five-agent qualification records remain in this repository as dated evidence. Current catalog validation covers only the three retained packages and their 17 supported routes.

```bash
python3 scripts/sync_components.py --check
python3 scripts/validate_packages.py
python3 -m unittest discover -s tests -v
python3 scripts/check_bundled_scripts.py
for plugin in pre-award-agent other-transaction-agent govcon-growth-agent; do
  uv run --with mcp --with httpx python scripts/smoke_mcp_discovery.py --plugin "$plugin"
done
uv run --with mcp --with httpx python scripts/smoke_mcp_discovery.py \
  --host-profile config/codex/1102tools-host.config.toml --keyless-status
```

Canonical runtime files and source commits are locked in [`components.lock.json`](components.lock.json).

## Version policy

- Compatible correction: affected agent patch version; marketplace patch version
- Compatible feature: affected agent minor version
- Breaking workflow or catalog change: major version

Free and open source. No 1102tools account is required.
