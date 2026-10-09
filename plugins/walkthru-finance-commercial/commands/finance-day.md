---
description: Daily finance routine - bank and cash reconciliation, then AR/AP exceptions, then items for the CFO.
argument-hint: [entity and date, then paste or attach bank statements, ePromis ledger, daily Excel sheet, payment lists, aging exports]
---
Run today's finance routine on: $ARGUMENTS

1. Run the `cash-position-reconciliation` skill on each bank account supplied. Return balances (bank vs ePromis vs Excel), unmatched items by category, status of yesterday's payments, today's commitments vs available cash, and the draft cash note. Report differences; never force them.
2. If AR or AP aging exports or supplier chasers are supplied, run the `ar-ap-aging-review` skill. Return only today's exceptions: new or worsening overdue items, disputes and holds, missing certificates, collection drafts, and payment prioritisation inputs that use the cash headroom from step 1.
3. If a bank guarantee or retention register is supplied, run the `walkthru-deadline-watch` skill for expiries and release dates due in the next 30 days.
4. Finish with **For the CFO**: at most 5 lines covering decisions needed, cash risks and unresolved differences, each with a source.

Skip any step whose inputs were not supplied, and say so. Everything is a draft or recommendation. Nothing is booked, sent, approved or paid.
