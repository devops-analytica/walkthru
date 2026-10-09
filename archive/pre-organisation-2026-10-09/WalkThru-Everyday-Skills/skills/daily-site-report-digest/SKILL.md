---
name: daily-site-report-digest
description: "Draft a daily site report or consolidate site updates into an evidence-based exceptions digest and next-day needs."
metadata:
  version: "1.0.0"
  reviewed: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Daily site report and next-day priorities

## Modes and inputs
Read [project-context.md](references/project-context.md). **Site report mode:** convert one engineer's raw notes into a DPR. **Operations digest mode:** consolidate existing DPRs across the supplied project list. Choose from the request; do not summarise away detail needed in a DPR.
Use report date, location/workfront, activities, quantities/units, manpower by trade, equipment, deliveries, inspections, HSE/quality entries, instructions and next-day needs. Compare with a supplied plan/look-ahead only. Show report date and review date separately; mixed-date reports must be grouped by date, not summed into one day.

## Analyse
- In site mode, organise reported facts using [site-report-template.md](assets/site-report-template.md). Unknown weather, incident status or quantities remain Not reported, not guessed.
- In digest mode, report received/expected projects and missing reports; without an expected list, say coverage unknown. Identify stopped/delayed work, missing materials/drawings, equipment failures, reported HSE issues, failed inspections, NCRs and consultant instructions.
- Calculate manpower gap = actual minus planned by the same trade, site and date. No plan means no measured shortfall. Do not impose an unapproved 10% alarm threshold. Progress variance requires comparable scope/measurement; do not infer percentages from narrative.
- Distinguish No incidents reported from Verified no incidents. Keep HSE findings visible rather than evaluating whether the site is safe.
- Record workfront and stated impact. Schedule criticality needs a programme link; label unmatched links Inference to confirm.
- Suggest resource moves only from evidenced released capacity of the right trade, on the available date, subject to qualifications/access/transport constraints. Never deploy workers or treat a future release as available today.
- Next-day needs refer to the next working/reporting date established by the user; if the calendar is unknown, label the intended date rather than assuming it.

## Deliver and check
Return DPR/digest, issue/action table, comparable manpower table, instructions requiring review and next-day arrangements. Use [manpower.csv](assets/manpower.csv) if no company table is supplied. Separate reported facts from suggested actions and unknown owners. Check duplicate reports, dates, trade matching, units and missing evidence. See [practice.md](references/practice.md).
