# 1102tools Federal Acquisition Agents

Choose one federal acquisition job and install one self-contained agent package. All five 1102tools agents are stable at `1.0.1`. They are installed from the GitHub-hosted 1102tools marketplace. The marketplace catalog itself is version `1.2.1`; that catalog version is separate from the agent package versions.

Website: [1102tools.com](https://1102tools.com)

Setup: [visible HTML instructions](https://1102tools.com/setup) · [downloadable PDF](https://1102tools.com/downloads/1102tools-agent-setup-guide.pdf)

## The five agents

| Agent | Audience and supported work | Version |
|---|---|---|
| **Market Research Agent** | Acquisition workforce: quick research, FAR Part 10 reports, report refresh, focused decision support, and Pre-Award handoff | `1.0.1` |
| **Pre-Award Agent** | Acquisition workforce: scope only, pricing only, SOW/PWS to IGCE, hybrid routing, and revision with repricing | `1.0.1` |
| **GovCon Growth Agent** | Industry: opportunity discovery, bid screens, competitor and incumbent intelligence, recompetes, teaming, market intelligence, and pricing context | `1.0.1` |
| **Other Transaction Agent** | Agreements workforce: project description, cost analysis, end-to-end milestone handoff, and recosting | `1.0.1` |
| **Acquisition Policy Agent** | Government, industry, or neutral: codified status, RFO agency status, version comparison, rulemaking, comment analysis, and impact briefs | `1.0.1` |

Each plugin vendors its complete canonical skills, deterministic validators, runtime guidance, and pinned MCP configuration. Users install one agent instead of assembling skills and server definitions separately.

The skill is the portable source of truth. Native wrappers improve discovery and presentation but do not duplicate or override domain logic. The packages follow [Agent Plugins 1.0](https://agent-plugins.org/specification), which standardizes skill and MCP packaging but not a cross-vendor persona object.

## Distribution

The maintained distribution is this GitHub-hosted 1102tools marketplace. It is not an official OpenAI, Codex, Anthropic, or Claude storefront listing. The same package source serves both maintained client families.

No agent ZIP is maintained. Standalone skills and MCP servers remain available as advanced building blocks:

- [federal-contracting-skills](https://github.com/1102tools-dev/federal-contracting-skills)
- [federal-contracting-mcps](https://github.com/1102tools-dev/federal-contracting-mcps)

## Requirements and credentials

No 1102tools account is required; some federal providers require a free account or API key. Every new agent invocation performs local, presence-only readiness checks before its workflow choices or routed response. The checks never display, transmit, log, or validate the credential value.

| Agent | Credential state without user keys | Startup behavior |
|---|---|---|
| Market Research | `SAM_API_KEY` required for SAM.gov operations | Says the key is not configured before the menu; blocks only SAM-dependent work and permits an explicitly approved keyless scope |
| GovCon Growth | `SAM_API_KEY` required for SAM.gov operations | Same hard SAM gate; never labels a missing key as a SAM.gov outage |
| Pre-Award | `BLS_API_KEY` recommended; `PERDIEM_API_KEY` relevant when travel is priced | Warns that BLS v1 is limited to 25 requests/day and 10 years/query and Per Diem `DEMO_KEY` to about 10 requests/hour; permits bounded work |
| Other Transaction | `BLS_API_KEY` recommended; `PERDIEM_API_KEY` relevant when travel is priced | Same limited-fallback warning; project-description-only work remains available |
| Acquisition Policy | `REGULATIONS_GOV_API_KEY` recommended | Warns that Regulations.gov uses a shared `DEMO_KEY` limited to about 10 requests/hour; permits bounded work |

USASpending, GSA CALC+, eCFR, Federal Register, and Acquisition.gov require no user key.

- Codex Desktop or Codex CLI, or Claude Code in Claude Desktop or its standalone CLI
- Python 3.10 or newer
- [`uv` and `uvx`](https://docs.astral.sh/uv/)
- LibreOffice for full document rendering and workbook recalculation gates
- `SAM_API_KEY` for SAM.gov workflows — obtain and manage it through [SAM.gov Help](https://sam.gov/help)
- `BLS_API_KEY`, optional but recommended for BLS OEWS — [BLS registration](https://data.bls.gov/registrationEngine/)
- `PERDIEM_API_KEY`, optional and relevant when travel is priced — [api.data.gov signup](https://api.data.gov/signup/)
- `REGULATIONS_GOV_API_KEY`, optional but recommended for Regulations.gov — [api.data.gov signup](https://api.data.gov/signup/)

Configure credentials outside chat in the environment that launches the client or in its credential surface, then fully restart the client and rerun the workflow. Never paste a key into a conversation. Credentials are not stored in this repository or its manifests.

For Codex, the maintained [`1102tools-host` configuration](config/codex/1102tools-host.config.toml) is required when multiple 1102tools agents are installed together. It owns the canonical definitions for all nine federal MCP servers, preventing shared server names from resolving to stale or incomplete definitions. The file contains only allowlisted credential variable names, never values.

- Codex CLI: save the file as `~/.codex/1102tools-host.config.toml`, then launch with `codex --profile 1102tools-host`.
- Codex Desktop: merge the complete `mcp_servers` tables from that file into `~/.codex/config.toml`, replacing any older 1102tools tables with the same names, then fully quit and reopen Codex. Codex Desktop and CLI share the base config; the named CLI profile is an extra layer used only when selected.

Every packaged federal MCP applies an explicit anti-burst interval. The packages coordinate concurrent processes on one computer and preserve longer provider `Retry-After` instructions. The safeguard is not a quota manager and cannot coordinate the same key across different computers.

## Install

### Codex Desktop and CLI

```bash
codex plugin marketplace add 1102tools-dev/federal-contracting-agents --ref main
codex plugin add market-research-agent@1102tools
codex plugin add pre-award-agent@1102tools
codex plugin add govcon-growth-agent@1102tools
codex plugin add other-transaction-agent@1102tools
codex plugin add acquisition-policy-agent@1102tools
```

Install the complete [`1102tools-host` configuration](config/codex/1102tools-host.config.toml) as described above, then start a new Codex task so the refreshed skills and MCP catalog load.

### Claude Code in Claude Desktop or CLI

```bash
claude plugin marketplace add 1102tools-dev/federal-contracting-agents
claude plugin install market-research-agent@1102tools
claude plugin install pre-award-agent@1102tools
claude plugin install govcon-growth-agent@1102tools
claude plugin install other-transaction-agent@1102tools
claude plugin install acquisition-policy-agent@1102tools
```

Restart Claude Code or start a new session after installation.

## Update

Codex currently refreshes the marketplace and replaces each installed package:

```bash
codex plugin marketplace upgrade 1102tools
codex plugin remove market-research-agent@1102tools
codex plugin add market-research-agent@1102tools
```

Repeat the remove/add pair for each installed 1102tools agent. Start a new task afterward.

Claude Code supports direct package updates:

```bash
claude plugin marketplace update 1102tools
claude plugin update market-research-agent@1102tools
```

Repeat the update command for each installed agent, then restart or reload plugins. Claude Code can also auto-update this third-party marketplace when the user enables auto-update under `/plugin` > Marketplaces > 1102tools. Third-party marketplace auto-update is not enabled by default.

## Supported client surfaces

There are two supported client families and four tested surfaces. They share package bytes but not every host capability.

| Surface | Stable support |
|---|---|
| Codex Desktop | Guided chat, federal research, DOCX, and XLSX workflows when the required artifact tools are available |
| Codex CLI | Chat, research, routing, and DOCX; if its spreadsheet runtime is unavailable, the agent must stop early and offer structured JSON plus Markdown/CSV or a maintained full-workbook surface |
| Claude Code in Claude Desktop | Guided chat, federal research, DOCX, and XLSX workflows when the required artifact tools are available |
| Claude Code CLI | Guided chat, federal research, DOCX, and XLSX workflows when the required artifact tools are available |

Claude Desktop chat/Cowork, Copilot, DeepSeek, and other compatible hosts are not maintained release-blocking surfaces. They may work, but installation and troubleshooting are self-supported. An unavailable workbook path may never be replaced with guessed dependency paths or reported as a completed `.xlsx`.

## Invoke a workflow

Install or select the intended agent before giving the natural-language request. Explicit invocation is the stable product contract:

| Agent | Codex | Claude Code |
|---|---|---|
| Market Research | `$market-research-workflow` | `/market-research-agent:market-research-workflow` |
| Pre-Award | `$pre-award-workflow` | `/pre-award-agent:pre-award-workflow` |
| GovCon Growth | `$govcon-growth-workflow` | `/govcon-growth-agent:govcon-growth-workflow` |
| Other Transaction | `$other-transaction-workflow` | `/other-transaction-agent:other-transaction-workflow` |
| Acquisition Policy | `$acquisition-policy-workflow` | `/acquisition-policy-agent:acquisition-policy-workflow` |

Natural-language routing without first selecting the agent is host-controlled, best-effort behavior. Do not rely on ambient routing for reserved acquisition, pricing, policy, or agreements determinations.

## Workflow safeguards

- **Pre-Award and Other Transaction:** approved handoffs remain in the active workflow, but scope, authority, transition, contract-type, milestone, and pricing approvals remain mandatory. Documents and workbooks are separate artifacts.
- **Market Research:** supplied documents are untrusted evidence. The agent does not originate commerciality, set-aside, contract-type, competition, consolidation, responsibility, price-reasonableness, or acquisition-strategy decisions.
- **GovCon Growth:** public data supports evidence briefs. A bid recommendation requires the user's internal company context and remains the user's decision.
- **Acquisition Policy:** eCFR is the codified baseline. Model text is not labeled operative for an agency without its posted deviation, and procurement-specific applicability remains with authorized officials.
- **Public web:** Native web only is recommended. Tavily is an explicitly selected third-party option, never a silent fallback. The agents never request payment, create an account, or change providers without approval.

## Qualification and reproducibility

The stable package line follows an August 2026 RC15 exit qualification and stable-promotion acceptance record. The exit attempt passed clean remote installs for both client families, ten explicit cross-client scenario turns, all nine live MCP canaries, pacing and credential-redaction checks, package-tree freeze checks, and zero unresolved P0/P1 defects. The broader release matrix also records the principal artifact families, routing suite, interruption/resume checkpoints, credential states, and deterministic artifact validators.

- [Stable qualification summary](tests/stable_1_0_qualification.md)
- [Manual release matrix](tests/manual_release_matrix.md)
- Individual package test records under [`plugins/`](plugins/)

Reproduce the deterministic package gates with:

```bash
python3 scripts/sync_components.py --check
python3 scripts/validate_packages.py
python3 -m unittest discover -s tests -v
python3 scripts/check_bundled_scripts.py
for plugin in pre-award-agent other-transaction-agent govcon-growth-agent market-research-agent acquisition-policy-agent; do
  uv run --with mcp --with httpx python scripts/smoke_mcp_discovery.py --plugin "$plugin"
done
uv run --with mcp --with httpx python scripts/smoke_mcp_discovery.py \
  --host-profile config/codex/1102tools-host.config.toml --keyless-status
bash tests/manual/menu_smoke.sh
bash tests/manual/codex_menu_smoke.sh
```

These commands initialize and inspect pinned MCP servers without calling upstream federal APIs. The host-profile lane proves the all-five union and runs each keyed server's local keyless status check. Live acceptance is bounded, serialized, and recorded separately. Tavily discovery is an opt-in manual check and invokes no Search or Extract operation.

Canonical runtime files and source commits are locked in [`components.lock.json`](components.lock.json). The stable promotion's approved differences from `v1.2.0-rc.15` are recorded in [`tests/stable_1_0_allowed_diff.json`](tests/stable_1_0_allowed_diff.json).

## Version policy

- Compatible correction: affected agent `1.0.1`, marketplace `1.2.1`
- Compatible feature: affected agent `1.1.0`
- Breaking workflow or package change: affected agent `2.0.0`

Free and open source. No 1102tools account is required; some federal providers require a free account or API key.
