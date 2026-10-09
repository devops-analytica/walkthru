---
description: Daily morning routine — email triage into priorities, then update the action register with anything new. Use at the start of the day.
argument-hint: [as-of date/time, project filter, or pasted emails]
---
Run the WalkThru morning routine for today. Arguments (may be empty): $ARGUMENTS

1. Invoke the `walkthru-morning-brief` skill. Use the authorized Outlook connector if available; otherwise ask for pasted/exported emails. Produce the brief.
2. Then invoke the `walkthru-action-tracker` skill with the actions found in step 1 plus the user's current register if supplied. Return the updated register, change log and today's chase list.
3. Finish with a 5-line summary: top 3 actions, anything overdue, anything needing a decision from someone else.

Nothing is sent or changed outside this chat.
