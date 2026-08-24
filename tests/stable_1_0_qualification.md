# Stable 1.0 Qualification Summary

Decision date: August 23, 2026

Stable agents: five packages at `1.0.0`

Marketplace: `1.2.0`

## Decision

The qualified RC15 package line and the approved Pre-Award source-link correction support stable promotion. No unresolved P0 or P1 defect remained at the release decision.

The maintained distribution is `1102tools.com` to the GitHub-hosted 1102tools marketplace. The release does not claim listing in an official OpenAI, Codex, Anthropic, or Claude storefront.

## RC15 exit qualification

Attempt of record: `exit-attempt-20260824T003055.562927Z`

Executed: `2026-08-24T00:34:54Z`

Result: pass, with zero failed or blocked events

The sanitized evidence established:

- Clean remote installation in isolated Codex and Claude configurations, with package trees matching the frozen repository trees.
- Ten of ten explicit cross-client scenario turns passed with prompt-hash equality and no prohibited read boundary.
- Nine of nine federal MCP canaries passed with discovered versions equal to the pinned versions, actual tool calls and timestamps, pacing checks, and an empty error list.
- Four required credential names were observed as present without retaining values; the redaction sweep was clean.
- Real-profile sentinels were byte-identical before and after testing.
- The evidence attempt contained 126 hashed artifacts.

The raw run ledger, transcripts, and private evidence remain outside Git under the protected validation directory. This repository retains only sanitized conclusions and replay references.

## Stable-promotion allowed differences

Stable promotion changes versions, manifests, marketplace metadata, current documentation, and evidence summaries. One shipped workflow file changes only its obsolete repository URL from `github.com/1102tools/...` to `github.com/1102tools-dev/...`; its executable workflow contract is unchanged. A routing-test matcher also changes to distinguish a prohibited copy directive from compliant negated wording.

No MCP command, pin, pacing value, credential contract, builder, validator, or other packaged runtime behavior changes during stable promotion. The exact allowed categories are recorded in `stable_1_0_allowed_diff.json` and checked before publication.

## Targeted Pre-Award requalification

After the canonical and vendored source-link correction:

- Canonical skill validation and 52 deterministic skill tests passed.
- The vendored Pre-Award skill matched the canonical source lock and SHA-256 record.
- Seven no-network Pre-Award routes passed in Claude.
- Six routes passed immediately in Codex; the seventh exposed a grader false positive caused by the compliant phrase “no need to ... copy the handoffs.” The matcher was narrowed to actual copy directives, a deterministic regression was added, and the affected Codex route passed on replay.
- The preserved Codex and Claude PWS DOCX artifacts passed the current document validator.
- The preserved Codex and Claude FFP workbooks passed the current workbook validator after LibreOffice recalculation and independent recomputation.

## Stable support contract

Two client families and four surfaces are maintained:

| Surface | Stable qualification boundary |
|---|---|
| Codex Desktop | Guided chat, federal research, DOCX, and XLSX when required artifact tools are available |
| Codex CLI | Chat, research, routing, and DOCX; early stop plus JSON/Markdown/CSV or Desktop handoff when the spreadsheet runtime is unavailable |
| Claude Code in Claude Desktop | Supported Code surface with full artifacts when required tools are available |
| Claude Code CLI | Supported command-line surface with full artifacts when required tools are available |

Explicitly selecting or invoking the intended installed agent is the stable routing contract. Ambient natural-language activation remains host-controlled and best effort. Claude Desktop chat/Cowork, Copilot, and DeepSeek are not maintained release-blocking surfaces.

## Continuing limitations

- Agent outputs support professional work but do not replace authorized acquisition, contracting, agreements, pricing, policy, or legal determinations.
- Keyed federal sources require user credentials and remain subject to upstream availability and rate limits.
- Tavily is optional, third party, and used only after explicit selection and approval.
- Full workbook generation depends on an available supported spreadsheet runtime; the agent must fail early instead of fabricating a workbook path.
