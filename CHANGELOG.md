# Changelog

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
