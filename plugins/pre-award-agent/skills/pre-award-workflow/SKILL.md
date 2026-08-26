---
name: pre-award-workflow
description: Coordinate scope-only, pricing-only, end-to-end SOW/PWS-to-IGCE, and revision or repricing workflows using the bundled 1102tools skills. Trigger when work spans a work statement and IGCE, needs FFP, LH/T&M, CR, or hybrid routing, carries an approved handoff into pricing, encounters a missing pricing MCP, or requests a reserved fair-and-reasonable or negotiation determination.
license: MIT
---

# Pre-Award Workflow

Coordinate the bundled skills. Do not replace their acquisition logic, artifact specifications, approval gates, or validators.

Runtime requirements: the bundled SOW/PWS and IGCE skills, Python 3.10+, `uvx`, and document and spreadsheet artifact support. Pricing requires the bundled BLS OEWS and GSA CALC+ MCP servers; travel also requires GSA Per Diem.

## Startup data-access readiness

On every new invocation, before mode selection, reserved-determination routing,
or any other user-visible response, call `bls-oews.get_access_status` and
`gsa-perdiem.get_access_status`. These are local, presence-only checks. Never
display, request, or transmit credential values.

Show a `Data access readiness` block before continuing whenever either status
is limited or unavailable:

- BLS `limited_fallback`: `BLS_API_KEY is not configured. BLS v1 remains
  available at 25 requests per day and 10 years per query.`
- Per Diem `limited_fallback`: `PERDIEM_API_KEY is not configured. Travel
  pricing will use the shared DEMO_KEY fallback, limited to approximately 10
  requests per hour.`
- missing status operation: identify the exact server and say its MCP package
  or the shared `1102tools-host` profile is outdated or incomplete. Scope-only
  work remains available, but pricing readiness is not verified.

End the block with `Setup: https://1102tools.com/setup#credentials`. For
`configured_unverified`, remain quiet and never claim the key is valid. The two
status calls are the only tools permitted before a fixed reserved-determination
boundary. A later 401/403 is a rejected credential; 429 is rate limiting.
Neither is an upstream outage. Do not retry automatically.

## Permanent release gates

1. **Reserved determination:** Any request to decide, write, draft, or conclude that a proposed FFP price or rate is fair and reasonable routes immediately to the fixed Option A/Option B block below. A shorter refusal, generic request for proposal data, alternate option labels, or promise to write the conclusion later is invalid.
2. **Artifact mode preflight:** Show the selected route's outcome preview and complete useful intake before testing artifact dependencies. Before the first artifact-specific approval, follow the active host's authoritative document and spreadsheet instructions and state whether full artifact mode is available. Do not bypass a host hard stop by guessing dependency paths or changing authoring libraries. If workbook generation is unavailable, preserve the approved inputs, offer the component skill's structured JSON plus Markdown or CSV fallback, or ask the user to continue in a maintained client surface that supports `.xlsx`; never call that fallback a completed workbook.

## Reserved-determination hard stop

Apply this after the mandatory startup readiness calls and before mode selection,
analysis, any other tool use, or drafting whenever the user asks the agent to
decide, conclude, or write that a proposed price or rate is fair and reasonable,
acceptable, or suitable for negotiation. This rule also applies when the user
asks only for a draft, example, recommendation, template, or sentence.

For an FFP labor-rate request, enter `igce-builder-ffp` Workflow B. The first response is fixed. Output the following block verbatim and nothing else, then wait. Do not replace it with a general refusal, a request for rates or comparison data, or different choices:

> I can pull positioning data that shows where each proposed rate sits against CALC+ ceiling rates and BLS market wages. I cannot draft a price reasonableness memo, write a "fair and reasonable" determination, or recommend negotiation positions. Those are Contracting Officer decisions under FAR 15.404-1, not skill outputs.
>
> Tell me which you want:
>
> **Option A: Positioning data only.** I produce a table with each proposed rate, CALC+ P25/P50/P75/P90 and sample size, plus a BLS metro burdened equivalent. I provide no verdict or recommendation.
>
> **Option B: Memo template fill.** You provide your rationale and determination. I reproduce your text verbatim in a DRAFT memo and place the benchmark tables underneath it. I do not originate conclusions or negotiation positions.
>
> Which option?

For another pricing method, use its component skill's equivalent controlled boundary. Never output determination language that the user did not already supply verbatim, even when it is labeled draft, example, conditional, or unsupported.

## Post-selection outcome contract

After a productive selection or an unambiguous direct route, the first response must begin with these exact labels in this order, before intake, routing preflight, or artifact preflight:

**First-visible-text hard gate:** In the post-selection turn, the first non-whitespace characters must be `Recommended outcome:`. Do not add a heading, acknowledgement, selection recap, routing narration, or code fence. Render all four preview lines as assistant text before invoking a component skill. Do not narrate component routing.

```text
Recommended outcome: <named product>
Includes: <major contents>
Boundary/default: <recommended default and reserved decisions>
Next: <first required fact, document, authority choice, or approval>
```

Then ask one bounded question or one batched set of related questions. Reuse all supplied facts, never ask the user to invent or name a report, and offer an alternative only when it materially changes the product or effort. The startup readiness calls and a directly triggered reserved-determination hard stop take precedence over this preview. Preserve every component research, generation, transition, and authority gate.

| Mode | Recommended outcome | Includes | Boundary/default | Next |
|---|---|---|---|---|
| 1 | Validated SOW/PWS `.docx` plus two chat-only handoffs | an executable work statement, measurable standards, staffing handoff, and Section B handoff | recommend PWS for performance-based services when the requirement supports it; the user or Contracting Officer retains contract type, commerciality, and other reserved decisions | collect the current requirement or source material and missing acquisition-strategy facts |
| 2 | Routed IGCE `.xlsx`, separated by confirmed pricing method or hybrid CLIN | auditable labor, indirect, escalation, travel and other-cost build-up, benchmarks, assumptions, formulas, and validation | no contract type is inferred; the user or Contracting Officer must confirm FFP, LH, T&M, a CR subtype, or hybrid routing | collect the approved handoff or requirements and the confirmed pricing method |
| 3 | SOW/PWS, approved chat-only handoffs, and routed IGCE workbook or workbooks | the complete validated scope-to-price package with the approved handoff carried forward | component approval and transition gates remain mandatory; contract type and reserved acquisition decisions stay with the user or Contracting Officer | collect the current requirement or source material and missing acquisition-strategy facts |
| 4 | Affected artifact rebuild plus before/after change register | changed scope or pricing fields, dependent artifacts, preserved approvals, revised handoffs, and rebuilt validated outputs | preserve every unaffected decision and never patch calculated totals in place | collect the existing artifacts or handoffs and the exact changed facts |

## Operating rules

1. Preserve user and Contracting Officer authority. Never select a contract type, approve a decomposition, or originate a fair-and-reasonable or negotiation determination. If asked to write or decide the conclusion, do not provide sample, suggested, bracketed, or template determination text. Only the component skill's controlled memo-fill path may carry exact determination text that the user already supplied.
2. Preserve every existing component-skill pause. Carry an approved answer forward, but never answer a gate on the user's behalf.
3. Keep the SOW/PWS `.docx`, staffing and Section B handoffs, and IGCE `.xlsx` distinct. The handoffs remain internal chat workpapers and never enter either artifact.
4. Reuse approved information exactly. Ask only for required fields that remain missing or that the user explicitly reopens.
5. For hybrid acquisitions, separate CLINs by user-confirmed contract type and produce a separate workbook for each pricing method. Never blend methodologies.
6. Do not bypass a missing MCP capability by calling an improvised public API.

## Select the mode

For a vague invocation with no defined task, show this complete mode menu after
the readiness block and stop at its question:

```text
What would you like to do?

1. Scope only — develop or revise a SOW/PWS and its chat-only handoffs
2. Pricing only — build or revise an IGCE using the user-confirmed contract type
3. End to end — develop the SOW/PWS, approve the handoff, then build the IGCE
4. Revision and repricing — reopen only affected scope decisions and recost them

Which option would you like? You can reply with the number, label, or your own wording.
```

Infer the mode from the request. If more than one mode is plausible and the difference changes the workflow, ask one concise question and wait.

After selection or direct routing, render the matching row from the post-selection outcome contract before applying the mode rule below.

- **Scope only:** invoke `sow-pws-builder`. Complete and validate the `.docx` and chat-only handoffs, then stop.
- **Pricing only:** require the user-confirmed contract type and route directly to the matching IGCE skill.
- **End to end:** invoke `sow-pws-builder`, preserve its approvals and validated handoffs, obtain transition approval, then route to pricing.
- **Revision and repricing:** reopen only the affected scope decision, rerun the relevant document gate, identify every changed handoff field, obtain approval, and rerun only affected pricing workbooks.

## Pricing router

Route only on an explicit user or Contracting Officer decision:

| Confirmed type | Pricing skill |
|---|---|
| Firm-fixed-price or FFP | `igce-builder-ffp` |
| Labor-hour or LH | `igce-builder-lh-tm` in LH mode |
| Time-and-materials or T&M | `igce-builder-lh-tm` in T&M mode |
| Cost-reimbursement or a confirmed CR subtype | `igce-builder-cr` |

If the user has not selected a type, stop at that decision. State that the decision belongs to the user or Contracting Officer and ask: `What contract type has the user or Contracting Officer selected: FFP, LH, T&M, a CR subtype, or a hybrid by CLIN?` Do not infer the type from risk, uncertainty, source material, or a preferred workbook.

For a hybrid, build this routing table before pricing:

`CLIN or line | User-confirmed contract type | Pricing skill | Included staffing rows | Open decisions`

Ask the user to approve the routing table, end at the question, and wait. Each pricing skill consumes only its rows.

## End-to-end sequence

1. Invoke `sow-pws-builder` and follow its staged questioning, approvals, document build, validation, and delivery requirements.
2. Capture the validated chat-only outputs headed `STAFFING HANDOFF TABLE: FOR IGCE BUILDER` and `SECTION B HANDOFF TABLE` in the active conversation. Do not ask the user to copy, upload, or restate them.
3. Before transition, verify:
   - the staffing table contains `Labor Category | SOC Code | FTE | Phase | Hours/Yr | Notes`;
   - every approved labor category appears exactly once unless the approved phase structure requires separate rows;
   - user overrides, derivation bases, hybrid routing, and pending decisions remain visible;
   - the Section B table contains `Line | Description | Contract Type | Pricing Unit or Basis | Period | Notes`;
   - CLIN or line mapping and user-confirmed contract type agree across both handoffs;
   - no rate, burden, fee, price, or fair-and-reasonable conclusion entered the staffing handoff;
   - the `.docx` passed the SOW/PWS skill's separation audit.
4. If a required handoff field is absent or inconsistent, return to the specific producer step and obtain approval for the correction. Do not silently repair it.
5. Ask: `The SOW/PWS and internal handoffs are validated. Do you approve moving the approved handoff into the user-confirmed pricing workflow?` This transition approval is always the next action after handoff validation. Do not ask for pricing inputs before it. End at the question and wait.
6. After approval, invoke only the routed pricing skill. Tell it to treat the preserved handoff as approved input and to skip repeated requirement decomposition.
7. Let that skill ask one batched pricing-input question for fields that remain missing. Do not repeat settled scope questions.
8. Complete the skill's capability preflight, pricing, workbook generation, formula-structure audit, independent recomputation, real spreadsheet-engine verification when available, and visual review.
9. Deliver the IGCE workbook separately. State which approved handoff version and pricing method it used.

## Capability preflight

Delay preflight until the selected pricing workflow first needs external data.

1. Reuse the startup access statuses. If either status operation was missing, stop pricing as an outdated or incomplete MCP/host-profile installation. If BLS is in `limited_fallback`, confirm the planned workload fits 25 requests per day and 10 years per query. When travel is in scope and Per Diem is in `limited_fallback`, confirm the plan fits approximately 10 requests per hour.
2. Inspect available MCP operations by stable server name, operation purpose, and input schema. Do not rely on a generated host prefix.
3. Labor pricing requires both:
   - `bls-oews` with the operations required by the routed skill, including latest-vintage detection and wage retrieval;
   - `gsa-calc` with CALC+ labor-category discovery and ceiling-rate retrieval.
4. Require `gsa-perdiem` only when travel is in scope.
5. Test only the capabilities the active workflow will use. Follow the component skill's preflight sequence.
6. For credentialed BLS or Per Diem requests, preserve at least three seconds between upstream calls. Do not expose credentials.
7. If an operation is missing, unauthenticated, unavailable, rate-limited, outdated/incomplete, or schema-incompatible, stop and identify the server, operation, failure class, and corrective action. Stop means make no further pricing calculation, substitution, comparison, or artifact finalization, even if another source remains available. Preserve all approved work so the user can resume after repair.

**HARD STOP:** After a required MCP capability fails, do not call another pricing MCP, continue a supported portion of the analysis, or suggest an alternate public source. Resume only after the failed capability is restored or the governing component skill accepts user-provided authoritative data through its documented path.

## Revision and repricing

When the user changes scope, staffing, period, CLIN structure, location, travel, or another approved assumption:

1. Identify the exact approved fields affected and the artifacts that depend on them.
2. Reopen only those producer-skill decisions and retain all unaffected approvals.
3. Regenerate and revalidate the SOW/PWS if contract-file content changed.
4. Regenerate the chat-only handoffs and show a concise before/after field list.
5. Require approval before repricing.
6. Rebuild and fully revalidate each affected workbook. Do not patch calculated totals in place.

## Completion record

At completion, report:

- workflow mode;
- user-confirmed pricing method for each workbook;
- delivered artifact names;
- validators and spreadsheet-engine checks run;
- any unavailable validation layer or unresolved user or Contracting Officer decision;
- confirmation that no manual handoff copying was required.
