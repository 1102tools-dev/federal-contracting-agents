# Changelog

## v1.2.9 - Deliverable defects closed from the 1.0.8 output review

All five agents advance to `1.0.9`. Each change closes a defect found by reading the rendered 1.0.8 deliverables as a paying customer would.

- Acquisition Policy validation maps every focused route to its own required structure, so a correct route-native product no longer fails a gate written for the impact brief.
- Market Research complete reports drop a stray blank page, render the execution plan as timing plus a cross-reference rather than a second copy of the action table, and reject any citation naming evidence the register does not contain.
- Labor-Hour and Time-and-Materials workbooks must tie current-assumption scenario figures to the summary per-period totals, which catches a scenario table silently disconnected by a stale range.
- Other Transaction cost workbooks must ship the canonical sheet set with print areas and fit-to-page scaling, so a bespoke layout or an unprintable workbook is not deliverable.
- GovCon Growth briefs must state an evidence basis matching the research record and must record real retrieval times instead of placeholders.

## v1.2.8 - Rendered-deliverable correction from the paid-output review

All five agents advance to `1.0.8`. Every change in this release corrects a defect a paying reader can see in the delivered file.

- Market Research reports render reader-facing source labels instead of internal class tokens, deduplicate repeated action tables, renumber evidence IDs without gaps, share one document design across routes, and reject session narration and named-firm incoherence at validation.
- GovCon Growth briefs carry the customer identity verbatim from intake, ban internal harness vocabulary in reader-visible text, require a checkable locator and retrieval date on every federal evidence row, stop restating page-one lists, and must answer each route's management question or lead with an explicit shortfall statement.
- Acquisition Policy products render one decision-gate table with readable column widths, carry the customer organization and decision date into every scope header, constrain status cells to a fixed vocabulary, and identify the prior analysis on refresh.
- Cost-reimbursement IGCEs must price as cost plus fee wherever a label says price, keep scenario fee bases consistent with the summary, and show per-period exposure for multi-period requirements. LH and T&M IGCEs must cover every stated period, keep escalation inputs live, and trace summary constants to the refresh register.
- OT project descriptions must carry one product identity across cover, title, and header with no instructional residue. OT cost models require per-category benchmarks or named proxies, hours reconciled to milestone durations, and readable narrative columns. Recost workbooks reject orphan benchmarks, lump-sum deltas, and silently dropped register-directed elements.

## v1.2.7 — Paid-output differentiation and print correction

All five agents advance to `1.0.7`. This release corrects the last material presentation defects found in a full paid-output review.

- Current Rule, Agency Status, Three-Layer, and Rulemaking routes now deliver distinct route-native analyses instead of reusing the Acquisition Policy Impact Brief body.
- Agency-specific Policy conclusions are derived from the named scope and matched deviation evidence instead of a hardcoded comparator agency.
- FFP, LH/T&M, cost-reimbursement, and OT cost workbooks now require a populated print area, one-page-wide scaling, and an unsplit first-view decision summary.

## v1.2.6 — Focused decision-product correction

All five agents advance to `1.0.6`. This release replaces seven generic-looking focused reports with route-native paid work products.

- Market Research refreshes now compare the prior baseline to current evidence and state the acquisition consequence of each change.
- Small-business analyses now identify candidate concerns, test supporting and contrary evidence, bound the Rule of Two conclusion, and assign outreach actions.
- Pre-Award handoffs now translate market evidence into scope, packaging, performance, competition, pricing-input, and risk decisions.
- Regulatory change, rulemaking watchlist, public-comment, and policy-refresh products now use their own decision tables, management actions, source notes, and route-specific running headers.
- Focused products are not generated when the approved evidence does not earn the selected title; the workflow returns an evidence-acquisition note instead.

## v1.2.5 — Customer-facing fallback and formatting correction

All five agents advance to `1.0.5`. This small follow-up release keeps incomplete records readable and actionable in the delivered report.

- Market Research incomplete records now show an explicit evidence-request plan instead of repeated “Not recorded” rows.
- Growth, Market Research, and Acquisition Policy scope metadata now uses reader-facing labels and list values.
- Money-like calculated totals render as currency in the customer-facing report.

## v1.2.4 — Consulting-grade output correction

All five agents advance to `1.0.4`. This release makes the customer-visible work product the controlling quality standard across the suite.

- GovCon Growth routes now produce distinct executive decision products instead of thin shared briefs.
- Market Research refresh, focused-analysis, and Pre-Award handoff routes now answer their specific management question and assign executable next actions.
- Acquisition Policy products lead with route-specific planning postures, implications, owners, and decision gates.
- Pre-Award work statements and IGCEs require useful first-view briefs or dashboards, populated analysis, visible ranges, cost drivers, and source limitations.
- Other Transaction products require executable milestone evidence, controlled change visibility, readable funding summaries, and clear next actions.
- Rendered usefulness is the release standard; structural validity alone is not treated as a successful work product.

## v1.2.3 — Human-readable work-product correction

All five agents advance to `1.0.3`. This release ships route-specific, decision-first work-product presentation and fixes the package-validation source lock so the published CI gate validates the same canonical skills that are vendored in the agents.

## v1.2.2 — Outcome-guidance correction

All five agents advance to `1.0.2`.

- Every productive menu selection names the recommended product, its major contents, the default or reserved decision boundary, and the next gate before intake or artifact preflight.
- Market Research, GovCon Growth, and Acquisition Policy Help routes diagnose the user's objective and recommend exactly one route instead of repeating the menu.
- Pre-Award and Other Transaction map every mode to a concrete `.docx`, `.xlsx`, combined package, or revision package while preserving every Contracting Officer and Agreements Officer decision boundary.
- Six component skills permit useful intake in read-only or artifact-limited sessions and stop only before dependent provider work or artifact generation.
- Static qualification covers all 33 top-level selections and preserves startup readiness, provider choice, document injection, URL approval, handoff, hybrid pricing, cost-sharing, and reserved-determination controls.

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

Future compatible corrections use the affected agent's next patch version and the marketplace's next patch version; compatible features use `1.1.0`; breaking changes use `2.0.0`.
