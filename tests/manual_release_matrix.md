# Manual 1.0.0 Release Matrix

Automated checks must pass before this matrix starts. Live federal API calls are manual, serialized, and separated by at least three seconds when a credential is active. Each run records the client, client version, model, model setting, exact prompt, fixture or approved inputs, generated artifacts, validator output, screenshots or rendered pages, API-call timing, and limitation notes in the applicable plugin `test.md`.

## Evidence required in every handoff-based end-to-end run

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

## Market Research Agent scenarios

| ID | Mode or fault | Required proof |
|---|---|---|
| MR-01 | Quick chat research | Complete six-choice menu first; no call before confirmation |
| MR-02 | Full FAR Part 10 report | Separate document intake, plan approval, findings approval, and validated `.docx` |
| MR-03 | Existing-report refresh | Prior report registered; only affected evidence and assumptions reopened |
| MR-04 | Conflicting acquisition documents | No silent precedence; user resolves approved-versus-draft conflict |
| MR-05 | Embedded document injection | Embedded model or tool directions ignored and recorded as untrusted content |
| MR-06 | Sensitive source content | Public queries contain only sanitized identifiers and terms |
| MR-07 | Thin or zero results | Transparent fallback and limitation label; no automatic acquisition decision |
| MR-08 | Pre-Award handoff | Structured evidence and approved decisions; no universal transfer claim |
| MR-09 | Missing SAM, USASpending, or web | Specific capability report and only an approved narrower product |
| MR-10 | Tavily plus native fallback | Approved sanitized query uses Tavily; consequential claims are checked against primary pages |
| MR-11 | Simulated Tavily failure | Native search is used only after combined-mode approval; fallback reason is recorded |
| MR-12 | Native only | Zero Tavily tool invocations; native search/fetch only |
| MR-13 | Tavily-only failure | Workflow stops and asks before switching provider or reducing scope |
| MR-14 | No public web | Federal-data desk-research label; no Tavily or native web request |

## GovCon Growth Agent scenarios

| ID | Mode or fault | Required proof |
|---|---|---|
| GROW-01 | Opportunity discovery | Complete nine-choice menu first; active dates and amendments verified |
| GROW-02 | Bid screen with complete context | Public evidence plus all internal decision categories and transparent logic |
| GROW-03 | Bid screen with incomplete context | Evidence brief only; no bid or no-bid verdict |
| GROW-04 | Competitor or incumbent | Entity ambiguity resolved; public facts separated from inference |
| GROW-05 | Recompete pipeline | End dates treated as signals, not guaranteed recompetes |
| GROW-06 | Teaming diligence | Public fit evidence without responsibility, trust, or legal conclusions |
| GROW-07 | Agency and market intelligence | Government-wide and agency scopes remain separate |
| GROW-08 | Pricing context | CALC+ ceiling rates are not described as paid rates or price reasonableness |
| GROW-09 | Missing or rate-limited SAM | Specific capability report; no direct-API bypass or burst retry |
| GROW-10 | Tavily plus native fallback | Approved sanitized query uses Tavily; consequential claims are checked against primary pages |
| GROW-11 | Simulated Tavily failure | Native search is used only after combined-mode approval; fallback reason is recorded |
| GROW-12 | Native only | Zero Tavily tool invocations; native search/fetch only |
| GROW-13 | Tavily-only failure | Workflow stops and asks before switching provider or reducing scope |
| GROW-14 | No public web | Limited evidence brief; no Tavily or native web request |

## Acquisition Policy Agent scenarios

| ID | Mode or fault | Required proof |
|---|---|---|
| POL-01 | Vague invocation | Complete ten-choice menu; no preflight or retrieval |
| POL-02 | Clear current-rule request | Direct route; eCFR baseline and any recent-effective Federal Register conflict surfaced |
| POL-03 | Agency RFO status | Agency, part, as-of date, and procurement timing framed; agency deviation retrieved before any operative label |
| POL-04 | Three-layer comparison | Codified text, model text, and agency deviation remain separately classified and cited |
| POL-05 | Version comparison | Before/after dates and amendments are reproducible; eCFR lag is stated where relevant |
| POL-06 | Rulemaking trace | Proposed, final, correction, withdrawal, and effective events are chronologically classified |
| POL-07 | Open comment period | Federal Register deadline is confirmed against the Regulations.gov docket |
| POL-08 | Public-comment analysis | Search terms, sample size, exclusions, coverage, and nonrepresentativeness are disclosed |
| POL-09 | Government lens | Same facts as neutral record; government operational impacts only are tailored |
| POL-10 | Industry lens | Same facts as neutral record; industry operational impacts only are tailored |
| POL-11 | Supplied policy conflict or injection | Embedded instructions ignored; unresolved authority or precedence produces a controlled stop |
| POL-12 | Missing MCP capability | Exact gap and reduced-scope offer; no general-web or direct-API bypass |
| POL-13 | Acquisition.gov upstream timeout | Bounded failure, preserved state, no fabricated model or deviation status, serialized retry only |
| POL-14 | Validated impact brief | Record, evidence IDs, links, LibreOffice conversion, extraction, and every rendered page pass |
| POL-15 | Reserved determination | Documented status only; no legal advice, clause selection, or procurement-specific applicability conclusion |

## Evidence required for the research agents

- The complete launch menu was the first response and no external call occurred before confirmation.
- Market Research used a separate document-intake turn before planning research.
- Document content was treated as evidence, not model or tool instructions.
- Public-query parameters were sanitized and contained no protected source content.
- The approved research plan preceded capability preflight and external retrieval.
- The user selected one of four web-provider modes; no option was inferred from silence.
- Exact sanitized terms, public extraction URLs, Tavily disclosure, and residual intent risk appeared before approval.
- Tavily mode invoked only `tavily_search` or `tavily_extract`; Crawl, Map, and Research remained unused.
- Tavily failure switched automatically only in the approved combined mode; every switch was recorded.
- Every finding cited a stable evidence ID and distinguished fact, inference, user statement, and decision.
- Market Research originated no reserved acquisition conclusion.
- GovCon Growth produced no bid verdict without complete internal company context.
- Any `.docx` passed record, structure, recomputation, LibreOffice, extraction, link, and visual checks.
- Any credentialed live call honored configured pacing and was recorded in the applicable `test.md`.

## Evidence required for the Acquisition Policy Agent

- A vague request showed all ten menu options; an unambiguous request routed directly.
- Every result recorded the as-of date, audience lens, source/tool version, canonical URL, retrieval timestamp, and source classification.
- Model text was never labeled operative without a documented agency deviation.
- Proposed, pending-effective, withdrawn, superseded, and nonregulatory items were never mislabeled as current codified text.
- eCFR was described as the codified baseline, with recent effective Federal Register conflicts surfaced.
- Comment findings disclosed the approved query, sample, exclusions, and limitations and did not claim consensus.
- User documents were treated as untrusted evidence and never copied into public query parameters.
- Every consequential brief statement resolved to an evidence ID.
- The `.docx` passed record, structure, status, link, LibreOffice, extraction, and all-page visual checks.
- The four MCPs honored their configured three- or four-second pacing; credentials were supplied only by the launch environment or client credential surface.

## Client matrix

Run every release-blocking control scenario and at least one representative end-to-end artifact scenario on each surface:

- Codex CLI with GPT-5.6 Sol at xhigh reasoning
- Codex Desktop with GPT-5.6 Sol at xhigh reasoning
- Claude Code in the Claude Desktop app with Opus 5 at high effort
- Claude Code CLI with Opus 5 at high effort
- Claude Code CLI with a current Sonnet model

Claude Code is one runtime distributed two ways. The Claude Desktop app bundles
`claude-code`, and the standalone CLI is a separate binary, often at a different
patch version. Both read the same `~/.claude/plugins` cache and the same
`settings.json`, and one package serves both. Record the resolved binary and
version for each run, but do not treat the desktop app and the CLI as separate
support targets and do not build a second package for either.

Claude Desktop's chat surface and Cowork are different products, not Claude
Code. They do not load Claude Code plugin marketplaces, so the packaged agents
do not install there. They are outside the support claim and are not release
gates.

For every CLI, run both explicit orchestrator invocation and natural-language routing. Explicit invocation must pass every release-blocking case. Record any host-specific implicit-activation limitation rather than weakening the explicit contract.

DeepSeek Harness, GitHub Copilot CLI, VS Code/Copilot, and other compatible hosts are non-blocking compatibility paths. They may be checked when practical, but they are not maintained public-preview support claims.

## DeepSeek Harness smoke evidence — 2026-08-22

- DeepSeek Harness `0.1.0-rc.6` composed all five agent overlays with the exact pinned MCP inventory expected by each package.
- A clean `dsh web` launch through `scripts/launch_deepseek_agent.sh` succeeded on an ephemeral local port.
- Vague requests reached the bundled workflow surface for all five agents. Pre-Award, Market Research, GovCon Growth, and Acquisition Policy displayed their expected menus; Other Transaction routed into its orchestrator and requested the OT kind and output mode.
- The Pre-Award overlay made a live local MCP call and returned all 18 bundled common SOC mappings.
- Acquisition Policy opened its ten-choice workflow menu, but the `acquisition-gov-mcp==1.0.0` dependency was unavailable from the package registry. Agency-specific RFO work remains an open release gate on every client until that package is published and the full path passes.
- No DeepSeek Harness artifact workflow is claimed complete from this smoke run.

**Current status:** the package-availability conclusion above is superseded. `acquisition-gov-mcp==1.0.0` is now published on PyPI, and the current [Acquisition Policy Agent test record](../plugins/acquisition-policy-agent/test.md) records fresh four-server discovery plus clean Codex and Claude Code installation and explicit-menu checks. The dated DeepSeek smoke remains historical compatibility evidence and does not create a maintained-support claim.

## Manual harness

Two scripts under `tests/manual/` cover what unauthenticated GitHub Actions
cannot: a real client installation, install-order permutations, plugin-only
reachability, and winner promotion. They are deliberately not in CI.

| Script | Covers |
|---|---|
| `menu_smoke.sh` | Launch surface for all five agents in fresh noninteractive sessions, no MCP calls |
| `coexistence.sh` | Both install orders, plugin-only reachability, winner promotion after uninstall |

`menu_smoke.sh` uses two assertion shapes because the five skills are not
uniform. Market Research, GovCon Growth, and Acquisition Policy define numbered
launch menus of 6, 9, and 10 items. The two agent-level orchestrators,
`pre-award-workflow` and `other-transaction-workflow`, define no menu at all and
infer the mode from the request, so the assertion is that every mode name is
offered. Asserting a numbered menu for those two is a harness error, not a
package defect.

`coexistence.sh` enforces plugin-only reachability through its assertion rather
than through the environment. A separate `CLAUDE_CONFIG_DIR` reports "Not logged
in" because the OAuth credential resolves from the system keychain scoped to the
default config directory, and `--strict-mcp-config` drops plugin-provided
servers along with user-level ones. The assertion requires the invoked tool name to carry the plugin-scoped prefix
Claude Code generates for a plugin-provided server, so a call satisfied by a
developer machine's own user-level MCP configuration fails rather than passing
for the wrong reason.

## Claude Code acceptance results — 2026-08-22

Run against the `1.0.0-rc.4` candidate packages after a full teardown of all
five plugins, the marketplace, and the plugin cache.

| Check | Result |
|---|---|
| Clean install, all five | Pass, expected versions reported |
| Plugin MCP servers connected | 10 of 10, each launching its pinned distribution |
| Market Research launch menu | Pass, six items |
| GovCon Growth launch menu | Pass, nine items |
| Acquisition Policy launch menu | Pass, exact packaged ten-item menu verbatim |
| Pre-Award modes offered | Pass, all four |
| Other Transaction modes offered | Pass, all four |
| Install order A and B | Pass, 10 registered in both, ownership differs |
| Plugin-only reachability | Pass, satisfied by the Other Transaction plugin's own GSA CALC+ server |
| Winner promotion | Pass, `sam-gov` moved to the next declarer on uninstall |

Still open for final `1.0.0`: natural-language routing in clean sessions,
authenticated multi-turn live workflows, and client-generated artifact
validation across both maintained clients. These remain release gates.

## Live keyed end-to-end run — 2026-08-22

Pre-Award `1.0.0-rc.4`, PRE-06 (PWS to FFP) plus PRE-15 (zero travel), run in
Claude Code with live BLS OEWS, GSA CALC+, and GSA Per Diem credentials supplied
through the launching environment. Scenario: FDA Tier 2 application support,
12-month base, contractor site, no travel, contract type directed as FFP by the
user. Both artifacts were produced in a single uninterrupted run.

| Artifact | Result |
|---|---|
| PWS `.docx` | 16 pages, 13 Heading 1 sections, 7 tables |
| IGCE `.xlsx` | 7 sheets, 90 live formula cells, base-period total $469,210.33 |

Validators reported by the run: `validate_docx.py --document-type pws` pass;
six separation fault-injection cases all correctly rejected; LibreOffice render
audit pass across all 16 pages after the workflow itself corrected two orphaned
table-row fragments; `recompute_expected_values.py` pass; `validate_workbook.py`
formula-structure pass.

Independently verified afterward rather than accepted from the run's own report:

- The `.docx` package was opened directly and confirmed to contain 13 Heading 1
  sections and 7 tables.
- The separation rule was re-checked against the extracted document body. No
  FTE, SOC code, CLIN, dollar amount, wrap-rate, or fully-burdened-rate text
  appears anywhere in the PWS. Those belong only in the chat handoff and the
  workbook, and they stayed there.
- The workbook was recalculated through LibreOffice from the delivered file.
  The grand total resolved to $469,210.33, matching the figure the run reported.

Boundary behavior worth recording: the user directed the contract type, and the
workflow priced FFP without re-deriving it. It reported CALC+ positioning as
positional statements only and left the fair-and-reasonable determination to the
Contracting Officer. It priced the directed 2.0 FTE exactly as given while
separately flagging that continuous 8x5 coverage implies 1.1064 FTE per seat, so
the directed basis carries a coverage risk. It raised that as a program-office
observation instead of silently changing the input.

This closes the artifact-generation gate for Pre-Award on Claude Code. The
equivalent live runs for the other four agents, and the same run on Codex,
remain open.

## RC5 stabilization closure — 2026-08-22

The statement immediately above records the earlier `rc.4` checkpoint. The
coordinated RC5 pass subsequently closed the four P1 regressions that motivated
this release: shared MCP pacing, the bundled USAspending acquisition profile,
Market Research approval ambiguity, and Acquisition Policy conflict handling.
It also closed the GovCon source-call timestamp and OT dynamic-TOC corrections.

The replayable evidence inventory is
[`manual/rc5_closure_ledger.json`](manual/rc5_closure_ledger.json). It records
the exact package and MCP versions, client binaries, selected prompts,
approval-boundary replays, tool counts, representative artifact hashes,
validator results, retrieval-timing proof, and limitations. Release-blocking
explicit cases passed in Codex and Claude Code. A five-agent explicit-routing
sample also passed through Claude Desktop's embedded Code binary. Opus critical
replays ran with fast mode on; Sonnet supplied an independent standard-speed
lane.

One natural-language Market Research activation initially bypassed the launch
menu and passed on an immediate clean-session replay. As required by the client
matrix, this is recorded as host-session activation variability; it does not
weaken the explicit native invocation contract. A concurrent LibreOffice
collision was isolated to the test environment, and serialized spreadsheet
recalculation passed.

All five representative artifact families passed their applicable structure,
evidence, formula, independent-recomputation, spreadsheet-engine, extraction,
link, and visual gates. This supports the five public release candidates. It
does not close every scenario in this manual matrix or authorize final
`1.0.0`; the complete authenticated multi-turn matrix remains open.

## RC5 lifecycle hardening evidence — 2026-08-23

The follow-on lifecycle round tested the installed release candidates rather
than changing their shipped workflow bytes. Its sanitized, replayable record is
[`manual/rc5_lifecycle_ledger.json`](manual/rc5_lifecycle_ledger.json); raw
transcripts and generated artifacts remain outside Git in the protected
validation directory named by that ledger.

Fresh scoped installation and restoration passed for both maintained client
families. Same-version reinstall was idempotent, individual owner removal kept
shared MCP capabilities reachable through the next declaration, and all five
current package versions were restored from the GitHub marketplace. The
historical upgrade fixture passed its byte-transition checks. Complete-uninstall
proof remains advisory because the captured post-cleanup inventories still
contained 1102tools declarations; no broad client directory was deleted to
manufacture a clean result.

The shared-key concurrency canary serialized two SAM.gov callers at the
configured three-second interval without deadlock or burst behavior. All nine
published MCP distributions passed the live normalized-shape and tool-inventory
canary. Missing, invalid, protected-valid, and captured/mock rate-limit paths
were exercised without retaining a credential value. A protected BLS v2
credential then completed the two previously blocked Claude pricing workbooks;
its value was not retained in the evidence.

| Principal lane | Current result |
|---|---|
| Market Research — Codex | Pass: validated DOCX |
| Market Research — Claude | Pass: validated DOCX |
| Pre-Award — Codex | Pass: validated PWS and IGCE workbook |
| Pre-Award — Claude | Pass: validated PWS and cost-reimbursement IGCE workbook |
| GovCon Growth — Codex | Pass: validated brief |
| GovCon Growth — Claude | Pass: validated brief |
| Other Transaction — Codex | Pass: validated project description and 375-formula workbook |
| Other Transaction — Claude | Pass: validated project description and 431-formula workbook; validator-coverage P1 remains open |
| Acquisition Policy — Codex | Pass: validated impact brief |
| Acquisition Policy — Claude | Pass: validated impact brief |

All ten principal lanes now have generated and validated artifact evidence. The
nested isolated Codex CLI could not expose the spreadsheet-authoring runtime,
but the maintained Codex Desktop surface completed and validated the OT
workbook; that remains a test-environment advisory, not a product defect. All
five Claude resume checkpoints preserved approvals and stopped without
duplicate retrieval or premature artifacts. The Codex checkpoint evidence is
directionally sound but not yet consolidated into ten complete cross-client
resume chains. The Sonnet 23-case routing replay is likewise retained as
advisory evidence rather than a claimed final gate.

No P0 remains. One P1 validator-coverage defect remains: the canonical OT
validator passed a recalculated workbook before a separate workbook-wide cached
value audit found formula errors outside the validator's mapped comparison set.
The delivered workbook was repaired and passed all validation and visual gates,
but the shipped validator must gain the global cached-error audit and a
regression before the OT lane closes. Final `1.0.0` also still requires complete
Codex resume proof, a real remote RC-to-final upgrade, and the remaining
authenticated manual scenarios.
