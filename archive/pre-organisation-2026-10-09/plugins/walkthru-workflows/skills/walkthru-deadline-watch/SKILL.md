---
name: walkthru-deadline-watch
description: "List overdue items and items due in 7, 14 and 30 days from any dated register (guarantees, visas, permits, submittals). Use for expiries, renewals, early warning."
metadata:
  version: "1.1.0"
  review_date: "2026-10-08"
  owner_role: "WalkThru AI lead / trainer"
---

# Deadline Watch

## When to use

Scans any WalkThru register or export that holds dates (bank guarantees, visas and Emirates IDs, trade licences, insurance, permits and NOCs, submittals, procurement required-by dates, retention release, DLP end dates, programme milestones) and lists what is overdue, due in 7, 14 and 30 days, or missing a date. Use whenever someone uploads a tracker or log and asks "what's expiring", "what's due soon", "anything overdue", "renewals coming up", "early warning", or wants a reminder list, even if they don't use the word deadline.

Several WalkThru teams track expiries by hand: the CFO for bank guarantees, HR and the PRO for visas and IDs, planning for approvals and procurement dates, document control for submittals. A missed date costs money (expired guarantees, visa fines, LDs). This skill gives an early-warning list from any register the user already keeps.

## Steps

1. Read the uploaded file(s): Excel, CSV, PDF table or pasted list. Identify the item column, the date column(s) that matter (expiry, due, required-by, target) and any owner, project or status columns. If more than one date column could apply, say which one you used and why.
2. Use today's date (UAE time) unless the user gives a different "as of" date.
3. Identify **date_kind** first: expiry, task_due or review_due. For expiry registers, Approved / Issued / Renewed remain monitored against their current expiry date; only genuinely Closed or Cancelled items stop monitoring. For completed task/review registers, completion/approval can close the task according to the supplied legend. Do not use one global status filter.
4. Group the remaining rows:
   - **Overdue**: date before today
   - **Due today or in 0–7 days**
   - **Due in 8–14 days**
   - **Due in 15–30 days**
   - **Missing date**: rows that should have a date but don't
5. Note lead time where it matters: visa renewals, bank guarantee extensions, authority approvals and long-lead procurement need action well before the date. Flag items whose normal lead time is longer than the time left (for example a guarantee extension due in 5 days when the bank needs 10).

## Output

```
DEADLINE WATCH · <register name> · as of <date>

OVERDUE (<n>)        | Item | Project/Person | Date | Days late | Owner |
DUE IN 7 DAYS (<n>)  | Item | Project/Person | Date | Days left | Owner |
DUE IN 8–14 DAYS (<n>)
DUE IN 15–30 DAYS (<n>)
MISSING DATE (<n>)
LEAD-TIME WARNINGS   - <item>: <why>
```

Sort each group by date. Quote dates and amounts exactly as in the source.

Offer: draft reminder emails per owner, or an updated register with a "Days left" column and conditional colours (red overdue, amber ≤14 days).

This skill runs on demand. It cannot send scheduled reminders by itself; if the user wants automatic weekly alerts, tell them that needs a scheduled task or Power Automate flow set up by IT.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Repeatable date calculation

Normalize dates to ISO YYYY-MM-DD after confirming ambiguous formats. Use `python scripts/operation_checks.py deadlines <normalized.json> --out <result.json>` with an explicit as_of and each row's date_kind. The helper uses calendar-day buckets, includes due-today items, preserves approved/renewed expiry items and rejects invalid dates. See [operation-checks.md](references/operation-checks.md). Working-day contractual deadlines need the supplied project calendar; never label a calendar-day estimate as contractual. A missing date or unknown legend is a data issue, not a closed item.

