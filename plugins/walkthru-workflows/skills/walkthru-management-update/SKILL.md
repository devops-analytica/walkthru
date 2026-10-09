---
name: walkthru-management-update
description: "One-page MD/GM management update: issue, impact, recommended action, owner, date and RAG status per project, condensed from reports, trackers, emails or programme data. Use when someone asks for a management summary, GM/MD update, weekly highlights, 'what should management know', executive summary, 'action points for the management meeting', or 'summarise this for the GM'."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Management Update

## When to use

Condenses reports, trackers, emails or programme data into a one-page WalkThru management update for the MD/GM, showing each issue's impact, the recommended action, owner and date, and a RAG status per project. Use whenever someone asks for a management summary, GM/MD update, weekly highlights, "what should management know", key points for a management meeting, an executive summary of a report, or "action points for management", even if they just say "summarise this for the GM".

WalkThru's GM expects managers to "analyse problems before escalation and bring a recommended solution". Management reads many updates, so each one must say quickly what needs their attention, what is recommended, who acts and by when. Detail stays in the source reports.

## Inputs

Anything the user has: weekly or monthly reports, P6 exports, daily site reports, cost reports, trackers, emails, chat summaries. Work only from what is provided. If a key number is missing (for example progress % for a project), write "n/a" instead of estimating.

## Output: one page

```
MANAGEMENT UPDATE · <department/role> · <period> · prepared <date>

HEADLINE
<2–3 sentences: overall position and the single most important thing management must know>

DECISIONS / ACTIONS REQUIRED FROM MANAGEMENT
| # | Project | Issue | Impact (time / cost / client) | Recommended action | Owner | By |

PROJECT STATUS
| Project | Status | Progress (plan vs actual) | Key issue | Next milestone |
Status: 🔴 Critical · 🟠 At risk · 🟢 On track

COMING UP (next 2 weeks)
- <milestones, approvals, payments, inspections, handovers>
```

## Rules that make it useful

- **Impact is specific**: "Handover slips ~3 weeks; LD exposure from 15 Nov" beats "may cause delay". Use the numbers in the source.
- **Every issue has a recommendation**: what the writer suggests management do (approve, decide, call the client, release payment, add resources). If the writer needs a decision, say which options and which one they recommend.
- **Owner is one person or company**, and "By" is a date.
- **Only exceptions**: projects that are on track take one row, no commentary. Limit the decisions table to the items that need management; move the rest to an optional appendix.
- **RAG rules**: 🔴 if a contractual milestone or handover is at risk, a safety incident occurred, or cost overrun exceeds budget contingency; 🟠 if float is being consumed or an approval or payment is overdue; 🟢 otherwise. State the reason in "Key issue".

Produce it as Word or as text in the reply, whichever the user asks; default to text they can paste into an email. Offer a PowerPoint slide version for management meetings.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.
