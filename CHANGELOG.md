# Changelog

## v1.2.1 — Credential-readiness correction

All five agents advance to `1.0.1`.

Agent `1.0.0` has a known missing-key diagnostic limitation: its MCP host can
collapse a credential failure into a generic tool-execution error, which a
client may then mischaracterize as a provider or server outage. Upgrade every
installed agent and the complete shared Codex host profile before relying on
credential diagnostics.

- Every new workflow invocation performs a local, presence-only access check before its menu or routed response.
- Market Research and GovCon Growth state that `SAM_API_KEY` is not configured and block only SAM-dependent work.
- Pre-Award and Other Transaction disclose the bounded BLS and GSA Per Diem keyless fallbacks.
- Acquisition Policy discloses the bounded Regulations.gov `DEMO_KEY` fallback.
- Missing keys are never retried, attributed to a provider outage, or requested in chat.
- The complete Codex `1102tools-host` profile now owns all nine federal MCP definitions used by the five-agent installation, with credential names allowlisted through `env_vars` and no credential values stored.
- SAM.gov `1.0.11`, BLS OEWS `1.0.8`, GSA Per Diem `1.0.8`, and Regulations.gov `1.0.7` expose `get_access_status` and actionable sanitized MCP errors.

## v1.2.0 — Stable release

The repository marketplace promotes all five agent packages to stable `1.0.0`:

- Market Research Agent `1.0.0`
- Pre-Award Agent `1.0.0`
- GovCon Growth Agent `1.0.0`
- Other Transaction Agent `1.0.0`
- Acquisition Policy Agent `1.0.0`

### Qualification

- Passed clean remote installation and explicit workflow checks in both maintained client families.
- Passed all nine pinned federal MCP startup, discovery, pacing, and bounded live-canary gates.
- Passed the deterministic routing, approval-boundary, component-lock, validator, and representative artifact gates recorded in the stable qualification summary.
- Passed real RC-to-stable updates and clean stable installation from GitHub `main` in Codex and Claude, with installed package trees matching the repository bytes.
- Preserved zero unresolved P0 or P1 defects at the release decision.

### Stable-promotion correction

- Corrected the remaining obsolete source link in the vendored Pre-Award FFP skill after the canonical skills repository correction.
- Revalidated the affected Codex and Claude routes and representative PWS/IGCE artifacts.
- Corrected one test-grader false positive for compliant language that said a user did not need to copy a handoff. This changed test-only matching, not workflow behavior.

### Distribution and support

- Distribution is the GitHub-hosted 1102tools marketplace linked from [1102tools.com](https://1102tools.com).
- Supported client families are Codex and Claude Code. Supported surfaces and artifact limitations are documented in the README and setup guide.
- This release is not an official OpenAI, Codex, Anthropic, or Claude storefront listing.
- Tavily remains an explicitly approved optional third-party provider and is never a silent fallback.

### Upgrade path

- Claude Code: refresh the marketplace and run `claude plugin update` for each installed agent.
- Codex: upgrade the marketplace, remove each installed package, and add it again.
- Start a new task or reload plugins after updating.

Future compatible corrections use the affected agent's `1.0.1` and marketplace `1.2.1`; compatible features use `1.1.0`; breaking changes use `2.0.0`.
