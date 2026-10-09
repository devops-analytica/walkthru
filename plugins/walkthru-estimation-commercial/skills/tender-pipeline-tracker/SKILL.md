---
name: tender-pipeline-tracker
description: "Maintain the tender register and weekly pipeline: received date, assigned estimator, site visit, clarification deadline, submission date, status and forecast, with overdue, this-week and later lists and draft chase messages. Use when the Estimation, Commercial and Contracts Manager or an estimator says 'what tenders are due this week', 'update the tender list', 'who has which tender', 'tender pipeline', 'forecast tenders', 'clarification deadlines coming up', 'submitted lost awarded list for Saturday', or pastes the handwritten to-do list or an estimation log extract. Drafts only; does not submit, chase or assign anything."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Tender pipeline tracker

## When to use
The estimation team handles about 12 tenders a month, assigned verbally and tracked on "a handwritten list of due tenders, forecast tenders and pipeline", rewritten weekly (Kareem Al Sayed profile, which also asks for "a digital task tracker to replace the handwritten list"). Use this to turn that list, an estimation-log extract or pasted emails into a clean register and a this-week view. It uses the bucket idea of the `walkthru-deadline-watch` skill but with tender-specific dates and statuses. It does not compute win-rate KPIs unless the log supplies outcomes.

## Inputs
Read [project-context.md](references/project-context.md). Need: current list or log (any format), as-of date, and any new tender invitations (email text, ITB). Use [tender-register.csv](assets/tender-register.csv) if no company register exists. Estimator names come from the input only; an unassigned tender stays "To confirm", never guessed.

## Steps
1. **Normalise rows** into the register columns: tender ID/name, client, emirate, received date, estimator, site visit date, clarification deadline, submission date and time, status, estimated value, forecast, source. Keep the source wording of status and value, including "reported" or "approx". Dates in ISO after confirming ambiguous formats.
2. **Statuses.** Use: Received / Assigned / Site visit pending / Pricing / Quotes awaited / Final check / Submitted / Awarded / Lost / Withdrawn / No bid / On hold. Map source wording only where obvious; otherwise keep the original and flag "Status to confirm". Submitted/Awarded/Lost/Withdrawn/No bid stop deadline monitoring but remain in the register; Submitted tenders get a client follow-up date only if one is supplied.
3. **Buckets** for each open tender, by the earliest upcoming of site visit, clarification deadline and submission date (name which date drives the row): Overdue (date passed and no completion evidence), Today to 7 days, 8-14 days, 15-30 days, Later, Missing date. Use calendar days; do not assume weekends or holidays. Submission times matter: a same-day deadline shows its time.
4. **Lead-time flags.** Final check needs 4-6 hours, 2 days before submission (profile); flag tenders within 2 days of submission with no "Final check" status or quotes still awaited, and tenders with a pending site visit or no estimator inside 7 days. Say "profile norm, to confirm".
5. **Forecast.** List forecast/pipeline tenders (not yet invited) separately with the expected date and value as reported; they are not counted as live or won.
6. **Chase drafts** per owner: estimator (status request), subcontractors/suppliers (quote request reminder, see the `quotation-comparison` skill), client or consultant (clarification or extension request). Drafts are unsent; no promises on price or dates.

## Output
```
TENDER PIPELINE · as of <date> · source <file/rows>
OVERDUE (n) | Tender | Client | Estimator | Driving date | Days late | Status |
THIS WEEK (n) | Tender | Estimator | Date type + date/time | Days left | Status | Flag |
8-14 DAYS / 15-30 DAYS / LATER / MISSING DATE
FORECAST (not yet live)
CHANGES since last list: new / status changed / dropped (if a previous list supplied)
DATA GAPS: unassigned, no submission date, unclear status
CHASE DRAFTS (unsent), grouped by recipient
```
Handoff: keep tender IDs, driving dates and open clarifications stable so a later list can show what changed. Offer the updated register as CSV or Excel. Saturday submitted/lost/awarded list: counts and values from supplied rows only.

Update mode: when a previous register is supplied, preserve its rows and notes, change only what the new evidence supports, and list every change with its source.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Interpretation limits
A blank date is a data gap, not "not due". This skill runs on demand; it does not send reminders or monitor continuously. Rehearse with [practice.md](references/practice.md).
