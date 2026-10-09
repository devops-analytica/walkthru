---
name: submittal-wir-tracker
description: "Engineering and document-control follow-up: shop drawing, material and method-statement submittals, RFIs and WIR/inspection requests. Shows who holds the next action, confirmed overdue reviews and what blocks upcoming site work. Use when someone uploads a submittal log, RFI log, WIR register or document-control tracker, or asks 'what's pending with the consultant', 'overdue submittals', 'status of RFI-21', 'which WIRs failed', 'what approvals do we need before next week'."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Submittal, RFI and inspection follow-up

## Inputs
Read [project-context.md](references/project-context.md). Accept shop drawing/material/method-statement submittal logs, RFI logs and WIR/inspection registers, with the project status legend and optional look-ahead. Establish as-of date, applicable revision, actual submission/response date, explicit due date or confirmed review rule/calendar. Use [engineering-register.csv](assets/engineering-register.csv) as fallback.

## Reconcile and classify
- Group by project + document reference + type; retain each revision. A current pending revision must not inherit an approval from a superseded revision. Confirm when the applicable revision is ambiguous.
- Interpret codes using the supplied legend, not a universal A–D assumption. Unknown codes remain Unmapped. Separate review result from whether site execution is permitted.
- **Our action:** not submitted, revise/resubmit, comments not incorporated, failed WIR awaiting rectification or RFI follow-up assigned to WalkThru.
- **External action:** pending consultant/client/authority response or inspection. Record who actually holds the next action, rather than classifying every RFI as consultant-owned.
- **Confirmed overdue:** open item past an evidenced due date under the applicable revision. When only a confirmed working-day rule is given, require a complete working calendar before calculating due dates. Otherwise show Due unknown and submission age in calendar days. Keep provisional internal targets out of contractual-overdue totals.
- A requested WIR date without a confirmed inspection appointment is Pending requested inspection, not a missed consultant commitment. Failed inspection does not equal approval after resubmission.
- Link pending records to scheduled work via explicit activity/location references. Similar title/trade matches are Inference to confirm. State upcoming-work horizon used (default 21 calendar days, adjustable); do not call an item critical without schedule evidence.

## Deliver
Return current-revision summary, our-side list, external-side list, confirmed overdue list, blockers and unmapped/missing evidence. Count documents and revision rows separately. Include draft grouped chase emails with references, dates and factual impacts. Produce a proposed register update/change log if requested; generating a local proposal does not change the live log.

## Check
No inherited approvals, fabricated due dates or conflated RFI/WIR statuses. Cite each finding to a row/page. Use [practice.md](references/practice.md) to test revision and calendar boundaries.
