---
name: walkthru-morning-brief
description: "Sort a WalkThru inbox into Action today, Reply needed and FYI by project. Use for email triage, catching up on email, or 'what do I need to do today'."
metadata:
  version: "1.1.0"
  review_date: "2026-10-08"
  owner_role: "WalkThru AI lead / trainer"
---

# WalkThru Morning Brief

## When to use

Sorts a WalkThru employee's inbox into a short morning brief of what needs action today, what needs a reply, and what is FYI, grouped by project. Use whenever someone asks to check, triage, summarise or catch up on their emails, says "what do I need to do today", "what did I miss", "anything urgent in my inbox", or pastes or forwards a batch of emails, even if they don't say "brief". Works with the Microsoft 365 (Outlook) connector when it is connected, or with pasted or exported emails when it is not.

WalkThru managers get 30 to 60 emails a day across 10 to 30 construction projects. Most need no action from them. The brief's job is to surface the few that do, so they can act before reading everything.

## Get the emails

1. If the Microsoft 365 connector is available, search the user's mailbox for emails received since their last working day (default: since yesterday 06:00 UAE time; after a weekend, since the last working day). Read the full body of anything that looks actionable. Include emails sent to others where the user is in CC, since managers are copied on submissions they own.
2. If the connector is not available, ask the user to paste the emails or upload an exported thread. Do not guess at emails you have not seen.

## Sort each email

Put every email in exactly one bucket:

- **Action today**: the user must do, approve, decide or attend something, or a deadline falls within 2 working days. Includes consultant rejections, client instructions, NCRs, safety incidents, payment chases from key subcontractors, and anything from the MD or GM that asks for something.
- **Reply needed**: someone is waiting for an answer from the user, but not urgently.
- **FYI**: information worth knowing (approvals received, minutes circulated, reports issued).
- **Ignore**: newsletters, automatic notifications with no action, duplicates.

When unsure between two buckets, choose the more urgent one and say why in a few words. Missing an urgent item costs more than over-flagging one.

## Output

```
MORNING BRIEF · <day, date> · <N> emails since <time>

ACTION TODAY (<n>)
| # | Project | From | What is needed | By when | Link/subject |

REPLY NEEDED (<n>)
| # | Project | From | Question | Suggested reply (one line) |

FYI (<n>)
- <Project>: <one line>

IGNORED: <n> (newsletters, notifications)
```

- Name the project using the project name or code from the subject or signature; use "General" when there is none.
- Write "What is needed" as a verb phrase the user can act on: "Approve subcontractor invoice SC-112 (AED 84,500)", not "Invoice email".
- Quote amounts, dates and reference numbers exactly as they appear. Never invent a figure.
- Keep the whole brief readable in under two minutes. If there are more than 10 action items, list the 10 most urgent and say how many more there are.

## After the brief

Offer to draft replies for the "Reply needed" items, or to add the action items to the user's follow-up tracker (see the walkthru-action-tracker skill). Do not send any email; drafts only, the user sends.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Search coverage

Microsoft 365 requires admin consent plus the user's own connection. Use only available search/read tools. Record mailbox, query window, timezone, pagination and number of messages inspected. Follow all available result pages; if search is capped or a tool fails, label the brief Partial coverage and explain the missing interval. Respect the user's supplied working week and holidays. Do not discard an automated notification when it contains a material deadline or failure.

