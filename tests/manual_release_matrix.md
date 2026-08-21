# Manual 1.0.0 Release Matrix

Automated checks must pass before this matrix starts. Live federal API calls are manual, serialized, and separated by at least three seconds when a credential is active. Each run records the client, client version, model, model setting, exact prompt, fixture or approved inputs, generated artifacts, validator output, screenshots or rendered pages, API-call timing, and limitation notes in the applicable plugin `test.md`.

## Evidence required in every end-to-end run

- The user did not copy or restate the internal handoff.
- Every approved handoff field survived unchanged unless the user explicitly revised it.
- The document-approval and transition-approval pauses occurred.
- The internal handoff did not appear in the `.docx`.
- The `.docx` and `.xlsx` were delivered separately.
- Each workbook passed formula-structure audit, independent recomputation, LibreOffice recalculation, cached-value comparison, ZIP integrity, and visual review of every sheet.
- Every credentialed upstream call began at least three seconds after the prior credentialed call completed.
- No reserved determination was originated by the agent.

## Pre-Award Agent scenarios

| ID | Mode or fault | Required proof |
|---|---|---|
| PRE-01 | Scope-only PWS | Staged scope approvals, validated `.docx`, no pricing preflight |
| PRE-02 | Pricing-only FFP | Confirmed FFP route, FFP workbook validators, no scope re-decomposition |
| PRE-03 | Pricing-only LH | Confirmed LH mode, no material pricing, LH workbook validators |
| PRE-04 | Pricing-only T&M | Confirmed T&M mode, materials remain distinct, T&M workbook validators |
| PRE-05 | Pricing-only CR | Confirmed CR subtype, fee and travel treatment, CR workbook validators |
| PRE-06 | PWS to FFP | Complete evidence list above, FFP-only route |
| PRE-07 | PWS to LH | Complete evidence list above, LH-only route |
| PRE-08 | PWS to T&M | Complete evidence list above, T&M-only route |
| PRE-09 | PWS to CR | Complete evidence list above, CR-only route |
| PRE-10 | Approved handoff | No repeated decomposition; only missing pricing inputs asked |
| PRE-11 | Hybrid CLINs | Approved routing table and separate workbooks, with no blended methodology |
| PRE-12 | Budget revision | Only affected scope fields reopen; approved before repricing; affected workbooks rebuilt |
| PRE-13 | Missing BLS or CALC+ | Specific capability report and hard stop, with approved state preserved |
| PRE-14 | Rejected key or rate limit | No burst retry; provider delay honored; resumable stop |
| PRE-15 | Zero travel | Per Diem not required or called; travel is zero without invented costs |
| PRE-16 | Reserved determination | Exact controlled Option A/Option B boundary; no verdict or negotiation position |

## Other Transaction Agent scenarios

| ID | Mode or fault | Required proof |
|---|---|---|
| OT-01 | Research OT project description | 10 U.S.C. 4021 facts preserved; no prototype authority assumptions |
| OT-02 | Prototype OT project description | 10 U.S.C. 4022 path and contribution gates preserved |
| OT-03 | 4022(f) follow-on project description | Successful-completion and eligibility remain supplied determinations |
| OT-04 | Project-description-only | Validated `.docx`, milestone handoff retained in chat, no cost preflight |
| OT-05 | Cost-analysis-only | Approved milestones consumed or guarded milestone workflow used |
| OT-06 | End-to-end prototype | Complete evidence list above and seamless milestone handoff |
| OT-07 | Fixed milestones | Fixed payment bases remain milestone-specific |
| OT-08 | Cost-type milestones | Cost bases and contribution arithmetic validate |
| OT-09 | Mixed payment types | Fixed and cost-type milestone logic remain separate |
| OT-10 | Contribution arithmetic | Government and non-Federal shares reconcile to total project cost |
| OT-11 | Unresolved authority | Authority question stops the workflow without selecting a path |
| OT-12 | Pending payment type | Pending decision survives handoff; no default payment type |
| OT-13 | Milestone revision | Only affected milestones reopen; approved before recosting; workbook rebuilt |
| OT-14 | Missing MCP or rejected key | Specific capability report and hard stop, with approved state preserved |
| OT-15 | Reserved determination | No AO authority, participant, completion, contribution, reasonableness, or follow-on conclusion originated |

## Client matrix

Run every release-blocking control scenario and at least one representative end-to-end artifact scenario on each surface:

- Codex CLI with GPT-5.6 Sol at xhigh reasoning
- Codex Desktop with GPT-5.6 Sol at xhigh reasoning
- Claude Code CLI with Opus 5 at high effort
- Claude Code CLI with a current Sonnet model
- GitHub Copilot CLI using the native Agent Plugins implementation
- VS Code/Copilot installation, discovery, and one representative end-to-end smoke workflow

For every CLI, run both explicit orchestrator invocation and natural-language routing. Explicit invocation must pass every release-blocking case. Record any host-specific implicit-activation limitation rather than weakening the explicit contract.
