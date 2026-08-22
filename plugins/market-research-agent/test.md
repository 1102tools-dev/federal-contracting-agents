# Market Research Agent test record

Version: `1.0.0-rc.1`  
Evidence date: August 21, 2026

## Canonical skill evidence

The bundled `market-research-builder` is an exact runtime copy from `federal-contracting-skills` commit `9075e967c6cb0c0e8bdabf1f5879bbc4805c0aeb`. Its canonical test record documents:

- Offline schema, evidence-record, numeric, DOCX, LibreOffice, extraction, link, and visual validation.
- Menu-only first-turn and document-intake-only second-turn passes in Codex CLI `0.149.0-alpha.4` with GPT-5.6 Sol at xhigh.
- Menu-only first-turn and document-intake-only second-turn passes in Claude Code CLI `2.1.239` with resolved `claude-opus-5` at max effort.
- A current Sonnet menu smoke pass.
- A conflicting-document test that preserved approved-versus-draft status, ignored embedded prompt injection, made no external call, and asked the user to resolve precedence.

No live federal call was made for those tests.

## Package evidence

Passed:

- Agent Plugins 1.0 plugin and MCP schemas.
- Portable, Codex, and Claude manifest identity and version agreement.
- Exact vendored-file hashes and component-lock verification.
- One-skill package surface with SAM.gov `1.0.6` and USASpending `1.0.3` only.
- Explicit three-second pacing in both packaged MCP definitions.
- Secret, escaping-reference, symlink, unpinned-package, and host-token hygiene checks.
- Compilation and `--help` execution for all three bundled Python scripts.
- Startup and discovery of 19 SAM.gov tools and 55 USASpending tools without invoking any tool.
- New installation and inventory from the local repository marketplace in Codex CLI, Claude Code CLI, and GitHub Copilot CLI `1.0.80`.
- Claude inventory resolution of one skill, one native agent, and the two expected MCP servers.

## Open release-candidate gates

- A fresh Codex Desktop session has not yet proved installed-plugin discovery.
- VS Code/Copilot installation and a representative workflow remain open.
- Complete implicit-routing coverage is advisory and remains open.
- Full live-source and commercial-market evidence scenarios remain open.
- A representative client-generated report has not yet been compared with the deterministic validated fixture.

These gaps block final `1.0.0`; they do not block this repository-marketplace preview.
