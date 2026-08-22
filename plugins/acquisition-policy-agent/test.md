# Acquisition Policy Agent test record

Version: `1.0.0-rc.2`

## Passed before packaging

- Canonical skill quick validation and repository validation.
- Policy-record fixture validation, controlled negative cases, and deterministic unit tests.
- Impact-brief generation, evidence-ID validation, link validation, LibreOffice conversion, text extraction, and all-page visual review.
- Acquisition.gov MCP offline parsing, PDF, cursor, SSRF, redirect, size, content-type, 429, pacing, strict-schema, and build tests.
- Local stdio startup and MCP discovery reported server `acquisition-gov` version `1.0.0` with exactly the five expected tools.
- Agent-level local-wheel startup and discovery loaded the exact four-server inventory without invoking an upstream tool: Acquisition.gov 5 tools, eCFR 13, Federal Register 8, and Regulations.gov 8.

## Upstream live gate

On 2026-08-22 the serialized release gate passed twice. The official RFO index, Part 10 model page, an indexed four-page NSF deviation PDF, and the FAQ each returned HTTP 200 with complete extraction. The MCP recorded source hashes and retained the rule that future hash changes require review rather than silent acceptance.

## Published-package and clean-install gate

The immutable MCP source commit `3f9376a406a2af17e5810d81f319d81efe34417e` installed into an isolated `uvx` environment directly from GitHub and exposed exactly five tools without invoking an upstream tool. Release workflow `32561799836` then passed shared safety checks, all nine package test-and-build jobs, trusted publication, and release creation. A fresh `uvx` environment installed `acquisition-gov-mcp==1.0.0` from PyPI and discovered all four policy-agent servers without invoking an upstream tool: Acquisition.gov 5 tools, eCFR 13, Federal Register 8, and Regulations.gov 8.

## Open agent release gates

- Run explicit and implicit routing cases in clean Codex CLI/Desktop and Claude Code.
- Complete an agency RFO status analysis, rulemaking/comment workflow, public-comment analysis, and validated impact brief with live sources.
- Record the complete client and artifact matrix below before removing `rc`.

The package remains a release candidate until every open gate passes.
