---
name: walkthru-action-tracker
description: "Create or update a WalkThru follow-up register in Excel and produce a chase list with draft chase messages. Use for to-dos, pending items or overdue follow-ups."
metadata:
  version: "1.1.0"
  review_date: "2026-10-08"
  owner_role: "WalkThru AI lead / trainer"
---

# Action Tracker

## When to use

Creates and maintains a WalkThru follow-up register in Excel (item, project, owner, due date, status, next chase) and turns it into a chase list with draft chase messages. Use whenever someone wants to track follow-ups, pending items, open actions, to-dos or approvals; asks "what's overdue", "who do I need to chase", "update my tracker"; wants to replace a handwritten or email-flag to-do list; or brings new actions from minutes, emails or chats to add to an existing tracker.

Almost every WalkThru role spends hours following up: approvals stuck with consultants, quotes from suppliers, answers from site engineers, documents from subcontractors. Today that lives in handwritten lists and flagged emails. This skill keeps one register and tells the user who to chase today.

## The register

An Excel workbook (`.xlsx`) with one sheet `Register` and these columns:

| Column | Notes |
|---|---|
| ID | A-001, A-002 … never reused |
| Project | Project name or code; "General" if none |
| Item | What must happen, as a verb phrase |
| Owner | Person or company responsible |
| Raised | Date added (DD-MMM-YYYY) |
| Due | Agreed date; blank if none was agreed |
| Status | Open, Waiting on others, Done, Cancelled |
| Last update | Date and one-line note of the latest news |
| Next chase | Date the user should follow up next |
| Source | Where it came from (email subject, MOM ref, chat date) |

Freeze the header row, add filters, and format dates as dates so they sort.

## Creating or updating

- **New register**: build it from whatever the user gives (a list, minutes, a chat summary, a photo of a handwritten list).
- **Update**: the user uploads the current register plus new information. Return the full updated register, not just the changes, and add a short "What changed" summary: added, closed, dates moved.
- Keep existing IDs and rows. Mark items Done or Cancelled instead of deleting them, so history is kept.
- If a new item looks like a duplicate of an open one, merge it and note the new source.

## Chase list

When asked what to chase (or after any update), produce:

```
CHASE TODAY · <date>
OVERDUE (<n>)        | ID | Project | Item | Owner | Due | Days late |
DUE THIS WEEK (<n>)  | ID | Project | Item | Owner | Due |
NO DUE DATE (<n>)    | ID | Project | Item | Owner | Raised |
```

Sort overdue items by days late. Items with no due date and older than 14 days are worth flagging; agreeing a date is often the real fix.

Offer short draft chase messages (email or WhatsApp) per owner, grouping all of one owner's items into a single message. Polite, specific, with the reference and the date needed. Do not send anything; the user sends.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.
