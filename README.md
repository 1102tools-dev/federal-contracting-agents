# 1102tools Agent Plugins

Two self-contained Agent Plugins compose the six tested 1102tools skills with the three federal pricing MCP servers they actually use. Both packages are public previews at `1.0.0-rc.2`; final `1.0.0` remains blocked by the authenticated-client and end-to-end artifact matrix.

Website: [1102tools.com](https://1102tools.com)

## The two agents

| Plugin | Workflows | Bundled skills |
|---|---|---|
| **Pre-Award Agent** | Scope only, pricing only, SOW/PWS to IGCE, and revision with repricing | SOW/PWS Builder, FFP IGCE, LH/T&M IGCE, CR IGCE, and the `pre-award-workflow` orchestrator |
| **Other Transaction Agent** | Project description only, cost analysis only, project description to cost analysis, and milestone revision with recosting | OT Project Description Builder, OT Cost Analysis, and the `other-transaction-workflow` orchestrator |

Both packages include BLS OEWS, GSA CALC+, and GSA Per Diem MCP configuration. The other five 1102tools MCP servers are intentionally excluded because these workflows do not use them.

The Pre-Award Agent keeps the three pricing methods separate. FFP routes only to FFP, LH and T&M route only to the shared LH/T&M skill in the selected mode, and cost-reimbursement routes only to the CR skill. Hybrid acquisitions are divided by CLIN and produce separate workbooks. The user or Contracting Officer selects the contract type.

The Other Transaction Agent preserves Research OT, Prototype OT, and follow-on production distinctions. It does not originate authority, participant-status, successful-completion, contribution, price-reasonableness, or follow-on eligibility determinations.

## One install, not a pile of files

Each plugin is a complete runtime package. A user installs one plugin instead of locating four separate skill folders, adding three MCP definitions by hand, and copying a handoff between conversations.

```text
plugins/pre-award-agent/
├── plugin.json                 Agent Plugins 1.0 manifest
├── mcp.json                    portable MCP configuration
├── skills/                     orchestrator plus complete skill packages
├── .codex-plugin/              OpenAI presentation metadata
├── .claude-plugin/             Claude Code manifest
├── agents/                     Claude Code native agent wrapper
└── com.github.copilot/         Copilot custom-agent wrapper
```

The installed skills are also multi-file packages, not single prompt files. Each includes a compact `SKILL.md` core plus the references, deterministic validators, runtime guidance, assets, and client metadata needed by that capability. Detailed specifications load only when needed, while the load-bearing workflow and silent-wrong-answer gates remain in the core.

The orchestrator skill is the portable agent entry point. Native wrappers improve discovery and presentation but do not duplicate or override acquisition logic. This is necessary because [Agent Plugins 1.0](https://agent-plugins.org/specification) standardizes skills and MCP configuration, not a cross-vendor persona or agent object.

## Seamless handoffs

“Seamless” means the approved scope or milestone workpaper stays in the active workflow. The user does not copy it, invoke a second skill, or restate settled information.

The agent still stops at every required approval:

1. Build and validate the document.
2. Validate the internal chat-only handoff.
3. Ask permission to transition into pricing or cost analysis.
4. Route only to the user-confirmed method.
5. Ask only for missing downstream inputs.
6. Build and validate the workbook as a separate artifact.

The internal handoff never enters the `.docx`, and the workbook is never merged into the document.

## Requirements and optional keys

- A client with Agent Plugins, Agent Skills, or compatible plugin support
- Python 3.10 or newer
- [`uv` and `uvx`](https://docs.astral.sh/uv/)
- LibreOffice for the full real-engine workbook recalculation gate
- `BLS_API_KEY`, optional but recommended for BLS
- `PERDIEM_API_KEY`, optional and needed only when travel is priced

Export keys in the environment that launches the client, or set them through that client’s credential-management surface. No credentials are stored in this repository or either manifest. GSA CALC+ does not require a key.

Credentialed BLS and Per Diem releases enforce `FEDERAL_API_MIN_INTERVAL_SECONDS=3` inside the MCP process. Longer provider retry instructions still take precedence, and automated tests never call live federal APIs.

## Install the public preview

The [1102tools Universal Setup Guide](https://1102tools.com/downloads/1102tools-universal-setup.pdf) is the installation source of truth. The agents are distributed through the repository marketplaces below. No agent ZIP is maintained on the website or in GitHub Releases.

### Codex CLI and Desktop

```bash
codex plugin marketplace add 1102tools-dev/federal-contracting-agents --ref main
codex plugin add pre-award-agent@1102tools
codex plugin add other-transaction-agent@1102tools
```

Start a new Codex task after installing or upgrading so the new skills and MCP catalog load.

### Claude Code

```bash
claude plugin marketplace add 1102tools-dev/federal-contracting-agents
claude plugin install pre-award-agent@1102tools
claude plugin install other-transaction-agent@1102tools
```

### GitHub Copilot CLI

```bash
copilot plugin marketplace add 1102tools-dev/federal-contracting-agents
copilot plugin install pre-award-agent@1102tools
copilot plugin install other-transaction-agent@1102tools
```

## Invoke a workflow

Explicit invocation is the release-critical path:

- Codex: `$pre-award-workflow` or `$other-transaction-workflow`
- Claude Code: `/pre-award-agent:pre-award-workflow` or `/other-transaction-agent:other-transaction-workflow`
- Copilot: select the installed custom agent or explicitly request the named orchestrator skill

Natural-language routing is also tested, but client-specific implicit-activation limitations are recorded in each package’s `test.md`.

Both self-contained plugins intentionally declare the same three stable MCP server names. Current Codex builds emit duplicate-server warnings when both plugins are installed together, then resolve each identical configuration once. The validator rejects any configuration drift between the two packages.

## Reproducibility and synchronization

Installed packages cannot depend on files outside their own root. The canonical skills are therefore vendored as complete runtime copies and pinned in [`components.lock.json`](components.lock.json). The lock records the canonical skills commit, MCP source commit, exact PyPI versions, package version, and a SHA-256 hash for every copied runtime file.

```bash
python3 scripts/sync_components.py --check
python3 scripts/validate_packages.py
python3 -m unittest discover -s tests -v
python3 scripts/check_bundled_scripts.py
uv run --with mcp python scripts/smoke_mcp_discovery.py --plugin pre-award-agent
```

CI uses mocked or no-call checks. Live federal API testing remains manual and serialized.

## Release status

The package structure, schema validation, vendored-component lock, MCP startup and discovery, deterministic script checks, and Codex routing controls are implemented. `1.0.0` will not be tagged until the authenticated Claude Code, Copilot CLI, VS Code/Copilot, and clean Codex Desktop matrix is complete. Current results and blockers are in:

- [`plugins/pre-award-agent/test.md`](plugins/pre-award-agent/test.md)
- [`plugins/other-transaction-agent/test.md`](plugins/other-transaction-agent/test.md)

OpenAI public-directory submission is deferred because the current submission path does not accept a plugin whose MCP dependencies are only local `stdio` servers. Repository marketplace installation remains supported. See [OpenAI’s submission guidance](https://developers.openai.com/plugins/guides/submit-claude-plugin).

## Canonical components

- Skills: [1102tools-dev/federal-contracting-skills](https://github.com/1102tools-dev/federal-contracting-skills)
- MCP servers: [1102tools-dev/federal-contracting-mcps](https://github.com/1102tools-dev/federal-contracting-mcps)

Free, open source, and no signup required.
