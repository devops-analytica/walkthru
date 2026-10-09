---
name: planning-weekly-report
description: "Weekly or monthly project progress report drafted from P6 exports, progress %, manpower, procurement and submittal status, in WalkThru's report structure for the Planning Manager to review. Use when someone asks for a weekly report, monthly report, progress report, project status report, planned vs actual, S-curve, 'prepare this week's report', or uploads last week's report with new data, even without the word report."
allowed-tools: Bash(python3 *) Read Write
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Planning Weekly / Monthly Report

## When to use

Drafts WalkThru's weekly or monthly project progress report from P6 exports, progress updates, manpower, procurement and engineering status, ready for the Planning Manager to review. Use whenever someone asks for a weekly report, monthly report, progress report, project status report, planned vs actual, S-curve, or "prepare this week's report" for one or several projects, or uploads last week's report together with new data, even if they don't say "report".

WalkThru's Planning Manager spends about 2 days a week on the weekly report and 2 days a month on the monthly report, across 15 projects. Most of that time goes on copying numbers between files and writing the same sections. This skill drafts the report so the planner only reviews, corrects and adds judgement.

## Inputs (use whatever is provided)

- P6: `.xer` or Excel export of the current update. For an `.xer`, run `python3 scripts/xer_check.py <file.xer> --out-dir <dir>`: it writes `activities.csv` (dates, float, durations in days) and `findings.csv` (float flags, current-planned slippage and look-ahead).
- Progress: planned % and actual % (overall and by area or trade), or the progress sheet.
- Manpower: planned vs actual headcount by trade.
- Procurement log: items, required-on-site date, status.
- Engineering / submittals log: shop drawings and material submittals with status.
- Last period's report: **if provided, keep its structure, headings and wording style**. Carry forward open issues and update them rather than starting fresh.
- The WalkThru report template if uploaded; it overrides the default structure below.

If a section has no data, keep the heading and write "No update received" so the reader knows it was not forgotten.

## Default structure

1. **Executive summary**: overall progress planned vs actual and variance, forecast completion vs contract completion, top three issues.
2. **Progress**: planned vs actual % overall and by area; S-curve (cumulative planned vs actual) as a chart when the data has periods.
3. **Programme status**: schedule health and float flags, delays with evidenced causes, float trend versus last period. An ordered driving path needs a verified P6 longest-path/float-path export. Do not infer a path from zero float alone.
4. **Look-ahead**: activities starting or finishing in the next 3 weeks.
5. **Engineering and submittals**: approved, under review, rejected, overdue (counts plus the overdue list).
6. **Procurement**: items at risk of arriving after the required date.
7. **Manpower**: planned vs actual by trade, with shortfalls.
8. **Risks and EOT**: open risks, delay events and notices issued or to issue.
9. **Management action points**: action, owner, date, impact (same format as the walkthru-management-update skill).

**Monthly report** adds: period progress and earned value if cost-loaded data is available, month-on-month comparison, and EOT/claims status.

## Rules

- Every number comes from the inputs. Never fill gaps with estimates; flag them in a "Data to confirm" list at the end.
- Progress variance = actual minus planned, in **percentage points (pp)**. Actual 55%, planned 60% → −5 pp, behind. Keep cost variance separate and identify favorable/unfavorable by revenue or expense. Use `python3 scripts/operation_checks.py variance <normalized.json> --out <result.json>` for the progress calculation; input keys: planned, actual, source.
- Explain delays as cause → impact → recovery action. Where the cause is unknown, ask it as a question for the project team.
- Keep the executive summary under 120 words. Management reads that and the action points first.
- Default output: Word for the report, Excel for any tables the planner wants to reuse. For several projects, produce one report per project plus a one-page portfolio summary table.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.
