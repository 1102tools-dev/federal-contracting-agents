---
name: other-transaction-workflow
description: Coordinate project-description-only, cost-analysis-only, end-to-end OT project-description-to-cost-analysis, and milestone revision or recosting workflows using the bundled 1102tools skills. Trigger when OT work spans scope and cost, carries an approved milestone handoff forward, encounters a missing pricing MCP, or requests a reserved authority, participant, contribution, successful-completion, price-reasonableness, or follow-on determination.
license: MIT
---

# Other Transaction Workflow

Coordinate the bundled skills. Do not replace their OT logic, artifact specifications, approval gates, or validators.

Runtime requirements: the bundled OT Project Description and OT Cost Analysis skills, Python 3.10+, `uvx`, and document and spreadsheet artifact support. Pricing requires the bundled BLS OEWS and GSA CALC+ MCP servers; travel also requires GSA Per Diem.

## Startup data-access readiness

On every new invocation, before mode selection or any other user-visible
response, call `bls-oews.get_access_status` and
`gsa-perdiem.get_access_status`. These are local, presence-only checks. Never
display, request, or transmit credential values.

Show a `Data access readiness` block before continuing whenever either status
is limited or unavailable:

- BLS `limited_fallback`: `BLS_API_KEY is not configured. BLS v1 remains
  available at 25 requests per day and 10 years per query.`
- Per Diem `limited_fallback`: `PERDIEM_API_KEY is not configured. Travel
  pricing will use the shared DEMO_KEY fallback, limited to approximately 10
  requests per hour.`
- missing status operation: identify the server and say its MCP package or the
  shared `1102tools-host` profile is outdated or incomplete. Project-description
  work remains available, but cost-analysis readiness is not verified.

End the block with `Setup: https://1102tools.com/setup#credentials`. For
`configured_unverified`, remain quiet and never claim the key is valid. A later
401/403 is a rejected credential; 429 is rate limiting. Neither is an upstream
outage. Do not retry automatically.

## Artifact-mode preflight

Show the selected route's outcome preview and complete useful intake before testing artifact dependencies. Before the first artifact-specific approval, follow the active host's authoritative document and spreadsheet instructions and state whether full artifact mode is available. Do not bypass a host hard stop by guessing dependency paths or changing authoring libraries. If workbook generation is unavailable, preserve the approved inputs, offer the cost skill's structured JSON plus Markdown or CSV fallback, or ask the user to continue in a maintained client surface that supports `.xlsx`; never call that fallback a completed workbook.

## Required-capability hard stop

Apply this before mode selection or any remaining cost analysis when the request states that a required pricing capability is missing, unauthenticated, unavailable, or schema-incompatible.

1. Stop the cost analysis immediately. Do not continue with an available pricing server, a partial comparison, a substituted source, or an improvised public API.
2. Identify the failed server, required operation, failure class, and corrective action.
3. Preserve every approved milestone, authority fact, contribution treatment, cost input, and pending decision already captured.
4. State that work resumes from that preserved state only after the failed capability is restored or the `ot-cost-analysis` skill accepts user-provided authoritative data through its documented path.
5. End without offering to continue a supported portion of the cost analysis.

## Operating rules

1. Preserve user and Agreements Officer authority. Never originate an authority, participant-status, successful-completion, cost-share, price-reasonableness, or follow-on eligibility determination. If asked to write or decide a reserved conclusion, do not provide sample, suggested, bracketed, or template determination text. Only a component skill's controlled path may carry exact determination text that the user already supplied.
2. Preserve every existing component-skill pause. Carry an approved answer forward, but never answer a gate on the user's behalf.
3. Keep the project-description `.docx`, milestone handoff, and cost-analysis `.xlsx` distinct. The handoff remains an internal chat workpaper and never enters either artifact.
4. Reuse approved milestone and authority facts exactly. Ask only for required fields that remain missing or that the user explicitly reopens.
5. Preserve unresolved authority, contribution, payment-type, and eligibility issues as pending decisions rather than filling them with assumptions.
6. Do not bypass a missing MCP capability by calling an improvised public API.

## Post-selection outcome contract

After a productive selection or an unambiguous direct route, the first response must begin with these exact labels in this order, before intake, capability preflight, or artifact preflight:

```text
Recommended outcome: <named product>
Includes: <major contents>
Boundary/default: <recommended default and reserved decisions>
Next: <first required fact, document, authority choice, or approval>
```

Then ask one bounded question or one batched set of related questions. Reuse all supplied facts, never ask the user to invent or name a report, and offer an alternative only when it materially changes the product or effort. Startup readiness, a directly triggered required-capability hard stop, and a directly triggered reserved authority or determination boundary take precedence over this preview. Preserve every component research, generation, transition, and authority gate.

| Mode | Recommended outcome | Includes | Boundary/default | Next |
|---|---|---|---|---|
| 1 | Validated OT Project Description `.docx` plus chat-only milestone handoff | authority record, objective, milestone structure, deliverables, completion evidence, schedule, and downstream cost handoff | milestone payment type remains pending unless supplied; the user or Agreements Officer retains authority, participant, contribution, successful-completion, and follow-on decisions | collect the concept or source material and missing authority facts |
| 2 | Milestone-based OT Cost Analysis `.xlsx` | milestone should-cost, labor and market benchmarks, materials, travel, ODCs, fees, contribution treatment, funding profile, scenarios, and validation | approved milestones are the default basis; do not infer authority, statutory path, cost share, payment type, ceiling, or a price-reasonableness conclusion | collect approved milestones or concept, authority facts, and missing cost inputs |
| 3 | Validated OT Project Description and OT Cost Analysis with the approved handoff carried forward | both separate artifacts, their validation records, and the approved chat-only milestone transition | every authority, milestone, artifact, and transition approval remains mandatory; reserved Agreements Officer decisions remain open | collect the concept or source material and missing authority facts |
| 4 | Affected artifact rebuild plus before/after milestone register | changed milestones or cost bases, dependent artifacts, preserved approvals, revised handoff, and rebuilt validated outputs | preserve every unaffected decision and never patch calculated totals in place | collect the existing artifacts or handoff and the exact changed milestone or cost facts |

## Select the mode

For a vague invocation with no defined task, show this complete mode menu after
the readiness block and stop at its question:

```text
What would you like to do?

1. Project description only — develop or revise the milestone-based project description and chat-only handoff
2. Cost analysis only — build or revise the milestone-based cost analysis
3. End to end — develop the project description, approve the handoff, then build the cost analysis
4. Milestone revision and recosting — reopen only affected milestone decisions and recost them

Which option would you like? You can reply with the number, label, or your own wording.
```

Infer the mode from the request. If more than one mode is plausible and the difference changes the workflow, ask one concise question and wait.

After selection or direct routing, render the matching row from the post-selection outcome contract before applying the mode rule below.

- **Project description only:** invoke `ot-project-description-builder`. Complete and validate the `.docx` and chat-only milestone handoff, then stop.
- **Cost analysis only:** invoke `ot-cost-analysis` with the user's approved milestones or its own guarded concept-to-milestone workflow.
- **End to end:** invoke `ot-project-description-builder`, preserve its approvals and validated handoff, obtain transition approval, then invoke `ot-cost-analysis`.
- **Milestone revision and recosting:** reopen only affected milestone decisions, rerun the relevant document gate, identify changed handoff fields, obtain approval, and rebuild the cost analysis.

## End-to-end sequence

1. Invoke `ot-project-description-builder` and follow its authority, path, contribution, milestone, document, validation, and delivery gates.
2. Capture the validated chat-only output headed `MILESTONE HANDOFF TABLE: FOR OT COST ANALYSIS` in the active conversation. Do not ask the user to copy, upload, or restate it.
3. Before transition, verify that the handoff preserves:
   - milestone IDs and sequence;
   - phase, title, and technical objective;
   - deliverables and objective completion evidence;
   - duration or start and end timing;
   - payment type or an explicit pending decision;
   - performance location and travel relevance;
   - authority facts and unresolved authority questions;
   - contribution treatment and participant-status facts as user-supplied facts, not agent findings;
   - user overrides and all pending decisions.
4. Confirm that the project-description `.docx` passed its separation audit and contains no cost estimate, labor rate, milestone amount, funding profile, contribution arithmetic, pricing conclusion, or handoff text.
5. If a required field is absent or inconsistent, return to the specific producer step and obtain approval for the correction. Do not silently repair it.
6. Ask: `The project description and internal milestone handoff are validated. Do you approve moving the approved handoff into OT Cost Analysis?` This transition approval is always the next action after handoff validation. Do not ask for cost inputs before it. End at the question and wait.
7. After approval, invoke `ot-cost-analysis`. Tell it to treat the preserved milestone handoff as approved input and to skip repeated milestone decomposition.
8. Let the cost skill ask one batched question for missing cost inputs. Do not repeat settled project-scope, milestone, authority, contribution, or location questions.
9. Complete the skill's capability preflight, cost analysis, workbook generation, formula-structure audit, independent recomputation, real spreadsheet-engine verification when available, and visual review.
10. Deliver the cost-analysis workbook separately. State which approved handoff version it used.

## Capability preflight

Delay preflight until OT Cost Analysis first needs external data.

1. Reuse the startup access statuses. If either status operation was missing, stop cost analysis as an outdated or incomplete MCP/host-profile installation. If BLS is in `limited_fallback`, confirm the planned workload fits 25 requests per day and 10 years per query. When travel is in scope and Per Diem is in `limited_fallback`, confirm the plan fits approximately 10 requests per hour.
2. Inspect available MCP operations by stable server name, operation purpose, and input schema. Do not rely on a generated host prefix.
3. Labor pricing requires both:
   - `bls-oews` with latest-vintage detection and wage retrieval;
   - `gsa-calc` with CALC+ labor-category discovery and ceiling-rate retrieval.
4. Require `gsa-perdiem` only when travel is in scope.
5. Test only the capabilities the active workflow will use. Follow the cost skill's preflight sequence.
6. For credentialed BLS or Per Diem requests, preserve at least three seconds between upstream calls. Do not expose credentials.
7. If an operation is missing, unauthenticated, unavailable, rate-limited, outdated/incomplete, or schema-incompatible, stop and identify the server, operation, failure class, and corrective action. Stop means make no further costing calculation, substitution, comparison, or artifact finalization, even if another source remains available. Preserve all approved work so the user can resume after repair.

**HARD STOP:** After a required MCP capability fails, do not call another pricing MCP, continue a supported portion of the analysis, or suggest an alternate public source. Resume only after the failed capability is restored or the `ot-cost-analysis` skill accepts user-provided authoritative data through its documented path.

## Milestone revision and recosting

When the user changes a milestone, deliverable, completion criterion, duration, payment type, location, travel basis, contribution treatment, or another approved assumption:

1. Identify the exact approved fields affected and the artifacts that depend on them.
2. Reopen only those producer-skill decisions and retain all unaffected approvals.
3. Regenerate and revalidate the project description if agreement-file content changed.
4. Regenerate the chat-only handoff and show a concise before/after field list.
5. Require approval before recosting.
6. Rebuild and fully revalidate the cost-analysis workbook. Do not patch calculated totals in place.

## Boundaries

When asked to make a reserved determination, identify the exact decision that belongs to the user or Agreements Officer, preserve the supporting facts and neutral analysis, and stop short of the conclusion. A user-supplied controlled finding may be inserted only through the component skill's authorized memo-fill path.

## Completion record

At completion, report:

- workflow mode and OT path handled;
- delivered artifact names;
- validators and spreadsheet-engine checks run;
- any unavailable validation layer or unresolved user or Agreements Officer decision;
- confirmation that no manual milestone-handoff copying was required.
