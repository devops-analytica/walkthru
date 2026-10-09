---
name: daily-site-report-digest
description: "Turn daily site reports from several projects into one exceptions digest: manpower gaps, delays, materials, HSE, quality, instructions and tomorrow's needs."
metadata:
  version: "1.1.0"
  review_date: "2026-10-08"
  owner_role: "WalkThru AI lead / trainer"
---

# Daily Site Report Digest

## When to use

Reads the daily site reports from several WalkThru projects and produces one exceptions digest for the Operations Manager covering manpower against plan, delays, material shortages, equipment, HSE incidents, quality/NCRs, inspections, client or consultant instructions and what needs action tomorrow, with a cross-project manpower view. Use whenever someone uploads or pastes daily reports, DPRs, site diaries or site updates, or asks "what happened on site today", "any issues across projects", "review the daily reports", or wants a next-day resource plan, even if only one report is shared.

WalkThru's Operations Managers read a daily report from every site engineer, every day, across all projects in their emirate. Most of each report is routine. The digest pulls out the exceptions so they can act on problems the same day and plan tomorrow's manpower, materials and equipment.

## Inputs

Daily reports in any form: PDF, Excel, Word, photos of handwritten sheets, pasted WhatsApp updates. Formats differ by engineer; read each one for the facts, not the layout. If a planned manpower figure or the programme look-ahead is provided, use it for comparison.

## What counts as an exception

- **Manpower**: actual below plan by more than 10%, or no-shows in a critical trade; idle labour.
- **Progress**: activity behind its planned date, work stopped or rework.
- **Materials**: shortage, late delivery, rejected delivery, stock running out within 3 days.
- **Equipment**: breakdown, missing, idle hire costing money.
- **HSE**: any incident, near miss, unsafe condition, authority visit. Always list these, even if minor.
- **Quality**: NCRs raised or open, failed inspections, rejected work.
- **Inspections/WIRs**: requested, passed, failed, pending consultant.
- **Instructions**: anything the client or consultant instructed on site. These can carry time or cost impact.
- **Blockers**: missing drawings, pending approvals, access, utilities, other contractors.

Routine progress that matches the plan is summarised in one line per project.

## Output

```
DAILY DIGEST · <date> · <n> projects · <n> reports received / <n> expected

ACTION NEEDED TODAY
| # | Project | Issue | Impact | Suggested action | Who |

HSE: <incidents or "No incidents reported">

BY PROJECT
<Project> 🔴/🟠/🟢 · <one line status>
 - Exceptions: <bullets>
 - Instructions received: <if any; mark "possible time/cost impact">

MANPOWER (all projects)
| Project | Planned | Actual | Gap | Trades short / surplus |
Suggested moves: <e.g. move 6 masons from Project A (surplus) to Project B (short)>

TOMORROW: manpower, materials and equipment to arrange
```

## Rules

- **Dates**: head the digest with the report date. "Action needed today" means the day the manager reads it; "Tomorrow" means the day after the report date, as the site engineers use it. If the reports are older than one working day, say so at the top.
- **Expected reports**: use the project list the user gives, or the previous digest. If neither exists, count the reports received and ask which projects are missing.
- **Status**: 🔴 if a planned milestone, pour, inspection or handover date has slipped, or an HSE incident with injury occurred; 🟠 if a shortage, breakdown, rejection, open NCR or near miss could cause a slip within a week; 🟢 otherwise.
- List missing reports by project at the top. A missing report is itself an exception.
- **Manpower moves**: suggest a move only when trades match, or when the reports say the workers can cover another trade. If the surplus and shortfall are different trades, say there is no direct move and the shortfall needs labour from outside. Count releases that start on a stated future date, and give that date.
- Quote quantities, names and dates exactly from the reports. Do not guess progress percentages.
- Suggested manpower moves must use only surpluses and shortfalls shown in the reports, and are suggestions for the manager to decide.
- Keep the whole digest readable in three minutes. Detail stays in the source reports.
- Offer to add the actions to the walkthru-action-tracker register, or to produce a management version using walkthru-management-update.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.
