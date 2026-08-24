# Pre-Award Agent

Stable release `1.0.1`.

Every new invocation first performs local, presence-only readiness checks for BLS OEWS and GSA Per Diem. With no `BLS_API_KEY`, BLS remains available through its limited v1 fallback: 25 requests per day and 10 years per query. With no `PERDIEM_API_KEY`, Per Diem uses the shared `DEMO_KEY`, limited to approximately 10 requests per hour. The agent discloses those limits before its workflow choices, never requests a key in chat, and links to [credential setup](https://1102tools.com/setup#credentials). Scope-only work and keyless GSA CALC+ remain available.

The Pre-Award Agent creates a SOW or PWS and carries its approved scope into the correct IGCE workflow without manual handoff copying.

## Included capabilities

- `pre-award-workflow`, the portable orchestrator
- `sow-pws-builder`
- `igce-builder-ffp`
- `igce-builder-lh-tm`, with distinct LH and T&M modes
- `igce-builder-cr`
- BLS OEWS, GSA CALC+, and GSA Per Diem MCP configuration

Every skill is a complete multi-file runtime package with its references, deterministic validators, scripts, and OpenAI metadata. The installed package does not reach outside this directory.

## Modes

1. Scope-only SOW/PWS creation
2. Pricing-only FFP, LH, T&M, or CR IGCE creation
3. End-to-end SOW/PWS to IGCE creation
4. User-directed scope revision and repricing

End-to-end mode preserves the validated staffing and Section B handoffs in the active conversation, asks for transition approval, and routes only to the user-confirmed pricing method. Hybrid CLINs are split into separate workbooks.

## Outputs

- A validated SOW or PWS `.docx`
- A separate validated IGCE `.xlsx` for each pricing method
- A completion record listing the approved handoff version, validators, and any unavailable validation layer

The staffing and Section B handoffs are internal chat workpapers. They never enter either artifact.

## Boundaries

The agent does not select contract type, approve scope on the user’s behalf, originate fair-and-reasonable determinations, or recommend negotiation positions. Missing required pricing capabilities stop pricing; the agent does not improvise a public API substitute.

Labor pricing requires both BLS OEWS and GSA CALC+. GSA Per Diem is used only when travel is in scope. Missing optional keys limit the affected source; they do not silently disable the agent.

## Invocation

- Codex: `$pre-award-workflow`
- Claude Code: `/pre-award-agent:pre-award-workflow`

Codex Desktop/CLI and Claude Code in Claude Desktop/CLI are the maintained stable paths. Other compatible clients are self-supported.

See the repository [README](../../README.md) for installation, optional-key setup, architecture, and supported-surface differences. See [`test.md`](test.md) for the stable qualification record and historical RC evidence.
