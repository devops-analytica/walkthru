---
description: Prepare this week's (or month's) planning progress report from the P6 export and progress data.
argument-hint: [project name(s), period, attached .xer/Excel and progress files]
---
Prepare the planning report. Input: $ARGUMENTS

1. If an `.xer` is attached, invoke the `p6-programme-review` skill first and run its `xer_check.py` helper; keep `findings.csv` for the report.
2. Invoke the `planning-weekly-report` skill using those findings plus progress, manpower, procurement and submittal data supplied.
3. Offer a one-page version through the `walkthru-management-update` skill if available.

State clearly which data was supplied and which sections are missing inputs.
