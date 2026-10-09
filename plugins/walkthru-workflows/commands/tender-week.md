---
description: Weekly tender view for estimation and commercial — pipeline status, overdue and upcoming clarification deadlines, outstanding supplier/subcontractor quotations to chase.
argument-hint: [attach tender list or estimation log; as-of date; optionally quotation request log or quotes received]
---
Prepare the weekly tender review. Input: $ARGUMENTS

1. Invoke the `tender-pipeline-tracker` skill on the tender list or log. Return the overdue, this-week and later lists, missing dates, forecast tenders and unsent chase drafts.
2. For each open tender with quotations outstanding or received, list the packages awaiting replies and draft supplier/subcontractor reminders. Where two or more quotes are in for a package, invoke the `quotation-comparison` skill and show only the headline: comparable or not, missing scope, clarifications.
3. Close with: top 3 tenders needing a decision this week, clarification deadlines inside 7 days, and data gaps to confirm with the estimators.

Nothing is sent, assigned or submitted from here. Unknown dates stay "Missing date"; estimators are named only from the supplied data.
