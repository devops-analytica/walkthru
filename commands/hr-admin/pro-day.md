---
description: Daily PRO routine - run-list from the application tracker, today's expiry items, and documents to chase.
argument-hint: [as-of date, then the PRO tracker / visa list / WhatsApp updates]
---
Invoke the `permit-visa-status-tracker` skill. Input: $ARGUMENTS

Build today's PRO run-list grouped by authority/location, with stage, days in stage, evidenced blocker and who holds the next action. Then use the `walkthru-deadline-watch` skill on any visa, Emirates ID, passport, licence or insurance expiry list supplied, and flag expiring items that have no application in the tracker. Finish with the documents to chase and draft reminders (not sent). If workers are ready to file a renewal batch, offer the `mohre-renewal-batch` skill. Mark missing stage dates "Not reported" and blockers with no recorded reason "Reason not recorded - PRO to confirm"; never assume a reason, submit or mark anything issued.
