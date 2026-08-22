# Acquisition Policy Agent test record

Version: `1.0.0-rc.1`

## Passed before packaging

- Canonical skill quick validation and repository validation.
- Policy-record fixture validation, controlled negative cases, and deterministic unit tests.
- Impact-brief generation, evidence-ID validation, link validation, LibreOffice conversion, text extraction, and all-page visual review.
- Acquisition.gov MCP offline parsing, PDF, cursor, SSRF, redirect, size, content-type, 429, pacing, strict-schema, and build tests.
- Local stdio startup and MCP discovery reported server `acquisition-gov` version `1.0.0` with exactly the five expected tools.
- Agent-level local-wheel startup and discovery loaded the exact four-server inventory without invoking an upstream tool: Acquisition.gov 5 tools, eCFR 13, Federal Register 8, and Regulations.gov 8.

## Upstream live gate

On 2026-08-21 the official RFO index was reachable and parsed, including the current Part 10 index entry and its posted-deviation links. At the same check, the linked model-part, agency-PDF, and FAQ routes timed out at the Acquisition.gov CDN before returning response headers. The MCP returned a bounded source failure and did not fabricate results. Repeat the serialized live gate before release.

## Open agent release gates

- Publish and independently install `acquisition-gov-mcp==1.0.0` from PyPI.
- Repeat exact startup and tool discovery from a clean install using the published Acquisition.gov package; the local-wheel preflight is green.
- Run explicit and implicit routing cases in clean Codex CLI/Desktop, Claude Code, Copilot CLI, and VS Code/Copilot.
- Complete an agency RFO status analysis, rulemaking/comment workflow, public-comment analysis, and validated impact brief with live sources.
- Record the complete client and artifact matrix below before removing `rc`.

The package remains a release candidate until every open gate passes.
