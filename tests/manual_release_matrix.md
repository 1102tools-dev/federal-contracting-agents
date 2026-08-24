# Manual 1.0.1 Credential-Readiness Release Matrix

Automated checks must pass before this matrix starts. Live federal API calls are manual, serialized, and separated by at least three seconds when a credential is active. Each run records the client, client version, model, model setting, exact prompt, fixture or approved inputs, generated artifacts, validator output, screenshots or rendered pages, API-call timing, and limitation notes in the applicable plugin `test.md`.

## 1.0.1 release gate

With `SAM_API_KEY`, `BLS_API_KEY`, `PERDIEM_API_KEY`, and
`REGULATIONS_GOV_API_KEY` absent, cold-start all five agents in Codex CLI,
Codex Desktop, Claude Code CLI, and Claude Code in Claude Desktop. Acceptance
requires the applicable missing-key or limited-fallback message before the menu
or routed response, no upstream call for a missing required SAM key, no retry
loop, no provider-outage diagnosis, no invented settings path, and no request
to paste a key in chat. Install all five together and prove the complete
nine-server federal MCP inventory plus every required readiness operation.

## Stable 1.0 decision

The RC15 exit attempt `exit-attempt-20260824T003055.562927Z` passed clean
remote installation in both maintained client families, ten of ten explicit
cross-client scenario turns, nine of nine live federal MCP canaries, pacing,
credential redaction, package-tree freeze checks, and real-profile restoration.
The evidence contained 126 hashed artifacts and no failed or blocked event.

The approved Pre-Award source-link correction was then synchronized from the
canonical skill, and both-client routing plus preserved PWS and FFP workbook
artifacts were revalidated. The only observed routing failure was a test-grader
false positive for compliant negated wording; a deterministic matcher
regression corrected it, and the exact Codex route passed on replay. No
unresolved P0 or P1 defect remained at the stable decision.

The current stable contract is explicit installed-agent selection or
invocation. Ambient activation remains measured host behavior rather than a
package guarantee. Supported client details and artifact limits are stated in
the root README and setup guide.

The untagged stable GitHub `main` commit then passed real RC-to-stable updates
in both maintained clients and clean installation in two isolated
configurations. All twenty installed-tree comparisons (real update plus clean
install, five agents per client in each lane) matched the repository package
trees. A test-only empty-home initialization defect caused the first isolated
Codex harness attempt to fail before installation; the runner was corrected to
create only its mode-`0700` client configuration root, regression coverage was
added, and the attempt of record passed. This was not a packaged workflow
defect. Ten of ten explicit installed-byte workflow smokes then passed across
Codex and Claude, and all nine bounded post-promotion live MCP canaries passed
with credential redaction intact.

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
| PRE-13 | Missing BLS key | Startup discloses the 25-request/day and 10-year/query fallback before routing; bounded work may continue |
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
| MR-01 | Quick chat research | Local SAM readiness check, explicit missing-key warning, then complete six-choice menu; no upstream call |
| MR-02 | Full FAR Part 10 report | Separate document intake, plan approval, findings approval, and validated `.docx` |
| MR-03 | Existing-report refresh | Prior report registered; only affected evidence and assumptions reopened |
| MR-04 | Conflicting acquisition documents | No silent precedence; user resolves approved-versus-draft conflict |
| MR-05 | Embedded document injection | Embedded model or tool directions ignored and recorded as untrusted content |
| MR-06 | Sensitive source content | Public queries contain only sanitized identifiers and terms |
| MR-07 | Thin or zero results | Transparent fallback and limitation label; no automatic acquisition decision |
| MR-08 | Pre-Award handoff | Structured evidence and approved decisions; no universal transfer claim |
| MR-09 | Missing SAM key | `SAM_API_KEY is not configured` before the menu; no SAM call or retry; only an approved narrower product |
| MR-10 | Native web only (recommended) | Approved sanitized query uses native search/fetch; zero Tavily tool invocations |
| MR-11 | Native web plus Tavily fallback | Native web is attempted first; simulated native failure switches to Tavily only after combined-mode approval, with the reason recorded |
| MR-12 | Native-only failure | Workflow explains the limitation and waits for a new provider selection; no payment, account creation, or provider switch is attempted |
| MR-13 | Tavily-only failure | Workflow stops and asks before switching provider or reducing scope |
| MR-14 | No public web | Federal-data desk-research label; no Tavily or native web request |

## GovCon Growth Agent scenarios

| ID | Mode or fault | Required proof |
|---|---|---|
| GROW-01 | Opportunity discovery | Local SAM readiness check, explicit missing-key warning, then complete nine-choice menu; active dates and amendments verified only after key setup |
| GROW-02 | Bid screen with complete context | Public evidence plus all internal decision categories and transparent logic |
| GROW-03 | Bid screen with incomplete context | Evidence brief only; no bid or no-bid verdict |
| GROW-04 | Competitor or incumbent | Entity ambiguity resolved; public facts separated from inference |
| GROW-05 | Recompete pipeline | End dates treated as signals, not guaranteed recompetes |
| GROW-06 | Teaming diligence | Public fit evidence without responsibility, trust, or legal conclusions |
| GROW-07 | Agency and market intelligence | Government-wide and agency scopes remain separate |
| GROW-08 | Pricing context | CALC+ ceiling rates are not described as paid rates or price reasonableness |
| GROW-09 | Missing or rate-limited SAM | Missing key is reported before the menu with no SAM call; 429 is labeled rate limiting with no direct-API bypass or burst retry |
| GROW-10 | Native web only (recommended) | Approved sanitized query uses native search/fetch; zero Tavily tool invocations |
| GROW-11 | Native web plus Tavily fallback | Native web is attempted first; simulated native failure switches to Tavily only after combined-mode approval, with the reason recorded |
| GROW-12 | Native-only failure | Workflow explains the limitation and waits for a new provider selection; no payment, account creation, or provider switch is attempted |
| GROW-13 | Tavily-only failure | Workflow stops and asks before switching provider or reducing scope |
| GROW-14 | No public web | Limited evidence brief; no Tavily or native web request |

## Acquisition Policy Agent scenarios

| ID | Mode or fault | Required proof |
|---|---|---|
| POL-01 | Vague invocation | Local Regulations.gov readiness check, limited-DEMO_KEY warning, then complete ten-choice menu; no upstream retrieval |
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

- The local presence-only access-status call was the first action; any required readiness warning preceded the complete launch menu and no upstream call occurred before confirmation.
- Market Research used a separate document-intake turn before planning research.
- Document content was treated as evidence, not model or tool instructions.
- Public-query parameters were sanitized and contained no protected source content.
- The approved research plan preceded capability preflight and external retrieval.
- The user selected one of four web-provider modes; no option was inferred from silence.
- Exact sanitized terms, public extraction URLs, Tavily disclosure, and residual intent risk appeared before approval.
- Tavily mode invoked only `tavily_search` or `tavily_extract`; Crawl, Map, and Research remained unused.
- Native failure switched to Tavily only in the explicitly approved combined mode; every switch was recorded. Native-only failure stopped for a new provider selection.
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
| `menu_smoke.sh` | Keyless startup and launch surface for all five agents; only local `get_access_status` calls precede the choices |
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
| GovCon Growth — Codex | Pass: validated 16-page rc.10 brief |
| GovCon Growth — Claude | Pass: validated 9-page rc.10 brief |
| Other Transaction — Codex | Pass: validated project description and 375-formula workbook |
| Other Transaction — Claude | Pass: validated project description and prior 431-formula workbook; a fresh rc.7 seven-sheet, 481-formula workbook also passed the global cached-error validator and full artifact review |
| Acquisition Policy — Codex | Pass: validated impact brief |
| Acquisition Policy — Claude | Pass: validated impact brief |

All ten principal lanes now have generated and validated artifact evidence. The
normal Codex CLI `0.149.0-alpha.4` surface did not expose the supported
spreadsheet dependency loader. It correctly produced no workbook rather than
bypassing the host's governing spreadsheet instructions. Codex Desktop and
Claude remain full-workbook surfaces; Codex CLI is qualified for chat, research,
routing, DOCX, and structured workbook specifications until that host capability
changes. All
five Claude resume checkpoints preserved approvals and stopped without
duplicate retrieval or premature artifacts. The Codex checkpoint evidence is
directionally sound but not yet consolidated into ten complete cross-client
resume chains. The 23-case matrix retains ambient, unselected prompts as
measured host-routing evidence. Release blocking applies to the explicit
installed-agent cases; the package cannot force a host to activate an installed
skill before the user selects it.

### RC15 installed-byte closure

The exact remote package trees installed in Codex and Claude match repository
commit `26c675fc330a80466e87bc5881d6304c403bcd50` for Market Research
`1.0.0-rc.12`, Pre-Award `1.0.0-rc.8`, GovCon Growth `1.0.0-rc.10`, Other
Transaction `1.0.0-rc.8`, and Acquisition Policy `1.0.0-rc.4`. Package
validation, component synchronization, the 80-test deterministic suite, pinned
MCP startup/discovery, and GitHub Actions run `32642560521` passed.

Installed-byte routing passed 23 of 23 cases in Codex. Claude passed all 23
release-critical cases and 22 of 23 measured ambient cases. A clean-session
replay repeated the sole ambient variance. It safely refused to originate a
fair-and-reasonable determination but did
not auto-load the selected skill's exact Option A/B response. The explicit case
passed, so this remains a P2 host-activation advisory rather than a packaged
workflow defect.

GovCon Growth rc.10 corrects a release-blocking pagination defect in which a
repeated Evidence Register header clipped a continuation row in LibreOffice.
Only that long evidence table now suppresses repeated continuation headers;
other tables retain them. The preserved Claude record rebuilt a clean nine-page
brief with SHA-256
`d5d6f787437a8efb0d2fc9c96bcf937741b6f77c71c18b2848761a9b0d1e9ea7`.
The migrated Codex record produced a clean sixteen-page brief with SHA-256
`9c0aeb24002ef0ea0e658c518a1c33b34c800e8b877b55e489a053630d6e730c`.
Both passed deterministic validation, LibreOffice rendering, and full-page
visual review. Exact installed Pre-Award rc.8 and Other Transaction rc.8 bytes
also revalidated the preserved Claude Pre-Award and both-client OT workbooks,
including external LibreOffice recalculation.

A final scoped lifecycle run then removed all five 1102tools plugins and the
1102tools marketplace from both clients. Before restoration, both clients had
zero 1102tools marketplace entries, plugin registrations, MCP registrations,
data directories, or cache roots. The two client-managed residual cache roots
were moved into a mode-700 recovery area rather than broadly deleting either
client directory. Reinstallation from GitHub `main` restored the five current
versions in documented order. Content-tree hashes match the repository for all
five packages in both clients; unrelated settings were preserved.

Five fresh Codex stop/resume chains now complement the five existing Claude
chains. Market Research preserved `MR-PLAN-01`, its source IDs, and the Native
web only selection. Pre-Award preserved `PWS-APPROVAL-01` and
`PWS-HANDOFF-01`. GovCon Growth preserved retrieval ID `GROWTH-RET-01`.
Other Transaction preserved its milestone, payment, contribution, and pending
input state. Acquisition Policy preserved conflict `C001` and both evidence
IDs. All ten paths performed no duplicate retrieval, invented no state, and
generated no premature artifact.

No P0 remains. The OT validator-coverage P1 is resolved in
`other-transaction-agent` `1.0.0-rc.8`: its global cached-error audit has
deterministic regression coverage and passed required LibreOffice replay against
the preserved Codex and Claude workbooks, and its current runtime-adaptation
contract fails early on hosts without a supported workbook path. The GovCon
pagination P1 and Pre-Award T&M material-handling P1 are also resolved in the
current installed bytes. Final `1.0.0` now requires the two clean guide-only
pilots, the 72-hour frozen-byte bake with beginning/end canaries, and a real
remote RC-to-final upgrade. The repeated Claude ambient-routing advisory
remains documented but is not a package defect or release-blocking case.
