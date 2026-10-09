---
name: boq-spec-check
description: "Check BOQ item descriptions and quantities against specification sections and the drawing list: flags description/spec conflicts, missing items, quantity sanity gaps between takeoff and BOQ, and dry-cost rate build-up gaps (material, manpower, wastage, subcontract split). Use when an estimator or QS asks 'check the BOQ against the spec', 'does the BOQ match the drawings', 'what did we miss in this tender BOQ', 'review the dry cost breakdown', 'tender final check', 'takeoff vs BOQ quantities', or pastes BOQ lines with spec clauses or a takeoff summary. A review aid, not a takeoff engine; it does not measure drawings."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# BOQ and specification check

## When to use
Tender verification is the biggest single block of the Estimation, Commercial and Contracts Manager's time (4-6 hours per tender, about 60 hours a month, Kareem Al Sayed profile), and includes "checking BOQ descriptions against specs and drawings", reviewing takeoffs "for anything missed", and breaking the dry cost into material, manpower, wastage and subcontract. Use it for the descriptive and quantity review before the final check, so a human reviewer starts from a flagged list. Formula and cell-reference auditing of the Excel file is a separate task; say so if asked.

## Inputs
Read [project-context.md](references/project-context.md). Need: BOQ lines (ref, description, unit, qty, rate if present), the relevant specification sections or clauses, the drawing list with revisions. Optional: takeoff summary (KREO/PlanSwift export), dry-cost build-up, addenda/clarification replies, tender due date. State which revision of each document was used; if an addendum list is missing, say addenda were not checked.

## Checks
1. **Description vs spec.** Compare each BOQ description with the governing spec clause: material, grade, thickness, finish, standard, brand/approved list, installation or testing requirements. Mark Consistent / Conflict / Spec silent / Spec not supplied. Quote both texts for a conflict.
2. **Missing items.** Work from the spec and drawing list, not from memory: scope items named in a spec section or shown as a drawing/schedule with no BOQ line (accessories, testing, commissioning, builder's work, provisional sums, preliminaries, attendance). List as "Possible omission to confirm", with the spec/drawing reference.
3. **Quantity sanity.** Only from supplied numbers: BOQ qty vs takeoff qty (difference and %), unit mismatches (m vs m2, nos vs LS), duplicated lines, zero or blank quantities, lines whose quantity cannot be derived from a drawing in the list. Do not remeasure drawings. Use the company tolerance if supplied; otherwise list differences and let the reviewer judge.
4. **Rate build-up.** For each priced line with a build-up: do material + manpower + wastage + subcontract reconcile to the rate; is wastage stated and plausible against the company allowance (if supplied); is a subcontract component supported by a quotation (see the `quotation-comparison` skill); are daywork, general requirements and margin carried as the offer expects. Missing split = "Build-up not supplied", not zero.
5. **Cross-checks.** Revision mismatches (BOQ based on older drawing revision), spec clauses superseded by addenda, same item priced at different rates in different sections.

## Output
```
BOQ / SPEC CHECK · <tender/project> · BOQ rev <x> · as of <date>
Documents used: <list with revision>   Not supplied / not checked: <list>

CONFLICTS | BOQ ref | BOQ text | Spec ref + text | Severity (price / scope / minor) |
POSSIBLE OMISSIONS | Source (spec/drawing ref) | Expected item | In BOQ? |
QUANTITY FLAGS | BOQ ref | BOQ qty | Takeoff qty | Diff | Why flagged |
RATE BUILD-UP GAPS | BOQ ref | Component missing/inconsistent | Detail |
Reported fact / Calculation / Inference to confirm / Recommendation
QUESTIONS for the estimator, ordered by likely price impact
```
Rank findings by likely price or scope impact and say which could be raised as a tender clarification to the client or consultant.

Handoff: keep tender name, BOQ and drawing revisions, and open questions so the `tender-pipeline-tracker` skill can carry them as clarification items. Offer a drafted clarification list (unsent) grouped by consultant discipline.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Interpretation limits
"Spec silent" and "no drawing found in the supplied list" are not proof of no requirement. Nothing here certifies the BOQ as complete or the tender as ready to submit; the final check stays with the estimator and manager. Rehearse with [practice.md](references/practice.md).
