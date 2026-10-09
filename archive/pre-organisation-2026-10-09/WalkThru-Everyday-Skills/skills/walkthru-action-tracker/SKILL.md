---
name: walkthru-action-tracker
description: "Create or update an action register from project records, with overdue items, change history and draft follow-ups."
metadata:
  version: "1.0.0"
  reviewed: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Action tracker and follow-up assistant

## Inputs
Read [project-context.md](references/project-context.md). Use the latest register plus new emails, minutes, site notes or a task list. Preserve the user's column structure where usable; otherwise use [register.csv](assets/register.csv). Establish the as-of date and working calendar for any date-based chase.

## Maintain the register
- Keep stable IDs. Match updates by project + reference + action scope, not title alone. Similar tasks on different sites remain separate. If matching is ambiguous, show the candidate update without merging it.
- Retain existing rows and IDs, including completed/cancelled history. Close only with explicit completion evidence; a follow-up email or partial completion is not closure.
- Due date means an agreed/supplied date. Separate a requested/proposed date and next chase date. Do not move an original deadline when someone asks for an extension; record Proposed due and approval pending.
- For new tasks, capture owner or Owner unknown, source, raised date where known, and status. Do not invent a responsible individual.
- Append changes to a separate Change log: ID, old value, new value, evidence, effective date. Return the full updated register, plus added/changed/closed counts.

## Follow-up output
Group active items into Overdue, Due today/within the requested window, Waiting on others and Due unknown. Sort confirmed due dates chronologically and avoid counting closed rows. State day basis; an item due today is not yet overdue. Keep no-date items visible without assigning fabricated deadlines.
Draft concise messages grouped by owner and project, with IDs, requested action and known dates. Suggested chase dates are recommendations. Nothing is sent by generating them.

## Deliverable and checks
Return the register, change log, chase list and missing-information list. XLSX: filters, frozen headers, date cells and separate Change log; otherwise separate CSV files. Check row/ID preservation, no cross-project merges and evidence for every closure/date change. Use [practice.md](references/practice.md) to rehearse conflicting updates.
