---
name: walkthru-chat-to-actions
description: "Turn a pasted or exported WhatsApp or Teams chat into decisions, actions with owners and dates, open questions and escalations. Use when a chat export (.txt/.zip) or thread is pasted or uploaded, or someone asks 'what was agreed in the group', 'summarise this chat', 'what do I need to follow up from WhatsApp', 'actions from the site group', even without the word actions. Handles mixed English/Arabic messages."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Chat to Actions

## When to use

Turns an exported or pasted WhatsApp or Teams chat (site groups, project groups, supplier chats) into decisions made, actions with owner and due date, open questions, and items to escalate. Use whenever someone pastes chat messages, uploads a WhatsApp "Export chat" .txt or .zip, shares a Teams thread, or asks "what was agreed in the group", "summarise this chat", "what do I need to follow up from WhatsApp", even if they don't mention actions. Handles mixed English and Arabic messages.

Site teams, project managers, suppliers and subcontractors run much of WalkThru's day-to-day coordination on WhatsApp. Decisions and promises get buried in long threads. This skill pulls them out so nothing agreed in a chat is forgotten.

## Input

- WhatsApp export: lines like `12/10/2026, 08:14 - Ahmed Site Eng: Concrete pour postponed to Sunday` (formats vary by phone; read whatever date format is there). Media shows as `<Media omitted>` or a file name; note it if the message depends on it.
- Teams: pasted thread or meeting chat.
- If the user gives a date range ("since Monday"), only use messages in that range.

## What to extract

1. **Decisions**: something agreed or instructed ("approved", "go ahead", "use the alternative tile", "pour on Sunday").
2. **Actions**: someone committed to or was asked to do something. Record who, what, and when. If no date was given, write "not stated" rather than inventing one.
3. **Open questions**: asked but not answered in the chat.
4. **Escalate**: safety issues, client or consultant instructions, cost or time impact, anything blocking work, payment disputes.

Read Arabic messages and write the output in English unless the user asks otherwise; keep names and quoted figures as written.

## Output

```
CHAT SUMMARY · <chat name> · <date range> · <N> messages

DECISIONS
- <date> · <decision> · (by <person>)

ACTIONS
| # | Action | Owner | Due | Source (date, sender) |

OPEN QUESTIONS
- <question> · asked by <person> on <date>

ESCALATE
- <issue> · why it matters (time, cost, safety, client)
```

Keep it short: one line per item. Skip greetings, "ok", "noted", forwarded memes and duplicate messages. If the chat contains photos the user needs to look at (site photos, invoices sent by photo), list them under a final "Check attachments" line with the date and sender.

Offer to add the actions to the walkthru-action-tracker register.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.
