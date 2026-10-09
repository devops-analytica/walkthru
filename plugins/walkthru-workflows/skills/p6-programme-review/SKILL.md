---
name: p6-programme-review
description: "Primavera P6 schedule health and float review from an .xer or Excel activity export: negative, critical and near-critical float, slippage vs planned dates, should-have-started, open ends, hard constraints, leads, long durations and a 3-week look-ahead, using the bundled xer_check.py helper. Use when someone uploads or mentions a P6 schedule, XER, programme, baseline, look-ahead, critical path, float, schedule health check, 'what's critical', 'what's delayed', 'review this programme', even without saying P6."
allowed-tools: Bash(python3 *) Read Write
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# P6 Schedule Health and Float Review

## When to use

Reviews a Primavera P6 programme (.xer file or Excel activity export) for WalkThru's planning and operations teams. It finds activities at/below a supplied critical-float threshold and near-critical activities, negative float, delays against planned dates, open ends, hard constraints, leads, long durations, activities that should already have started, and what starts in the next three weeks, then explains the risks and the actions needed. Use whenever someone uploads or mentions a P6 schedule, XER, programme, baseline, look-ahead, critical path, float, schedule health check, or asks "what's critical", "what's delayed", "review this programme", even if they don't say P6.

WalkThru's planning team runs 15 projects with two people, and the operations managers review progress against the programme every week. This skill does the mechanical schedule checks in seconds so the planner's time goes on judgement: why something is late and what to do about it.

## Step 1: Get the data

**If the user uploads a `.xer` file**, run the bundled script:

```bash
python3 scripts/xer_check.py <file.xer> --out-dir <output dir>
```

Options: `--critical-float-days` (default 0 days, provisional until P6 settings are confirmed), `--near-critical-days` (default 10 converted working days), `--lookahead-days` (default 21 calendar days), `--fallback-hours-per-day` (default 8, explicitly warned when used). `--out-dir` is required. Float and duration are compared at full precision; only displayed values are formatted. It prints a summary table and writes `activities.csv` (all activities with durations and float in days) and `findings.csv` (one row per flagged activity and check). Read `findings.csv` for the detail.

If the `.xer` upload is refused, ask the user to rename it to `.txt` or export activities to Excel instead.

**If the user uploads an Excel export**, map the columns yourself. Typical P6 headers: Activity ID, Activity Name, Original Duration, Remaining Duration, Start, Finish, BL Project Start, BL Project Finish, Total Float, Activity Status, Primary Constraint, Predecessors, Successors. Say which columns you used. Run the same checks as below with code on the sheet.

## Step 2: The checks

| Check | Why it matters |
|---|---|
| Negative float | The programme already misses a constraint or the completion date |
| Float at/below critical threshold and near-critical | Risk indicators; not proof of an ordered driving path |
| Finishing later than planned / baseline | Slippage to explain and recover |
| Should have started (start before data date, no actual start) | Out of sequence or progress not updated |
| Open start / open finish | Missing logic makes float and the critical path unreliable |
| Hard constraints (Must Start/Finish On, Mandatory) | They override logic and can hide real delays |
| Leads (negative lags) and start-to-finish links | Usually poor practice; consultants often reject them |
| Long durations (> 44 working days) | Too coarse to track progress |
| Starts or finishes in the next 21 days | Project-specific look-ahead; identify what must be ready |

**About baseline vs planned:** in an XER, the dates compared are P6's *planned* dates of the current project, which may not be the approved baseline. For a true baseline comparison, ask for an Excel export with the BL Project Finish column, or the baseline project XER.

## Step 3: Report

```
PROGRAMME REVIEW · <project> · data date <date>

SUMMARY
<3–4 sentences: forecast completion vs contract/planned completion, how many activities at/below a supplied critical-float threshold and near-critical activities, the biggest risk>

FLOAT FLAGS AND PLANNED-DATE SLIPPAGE
| Activity ID | Name | Float (d) | Slip (d) | Likely cause / question | Action needed | Owner |

PROGRAMME QUALITY ISSUES
- <n> open ends, <n> hard constraints, <n> leads, <n> long durations · list the IDs · what to fix in P6

LOOK-AHEAD (next 3 weeks)
| Activity ID | Name | Start | Prerequisites to confirm (materials, approvals, drawings, manpower) |

MANAGEMENT ACTION POINTS
| # | Action | Who | By | Impact if not done |
```

Rules:
- Quote IDs, dates and float exactly from the data. Do not invent causes; where the cause isn't in the data, write it as a question for the site team ("Slab L1: is the delay pending pour approval?").
- Order delays by their effect on completion, worst first.
- Prerequisites in the look-ahead come from activity names and the user's knowledge; mark them as items to confirm.
- Offer the report as Excel (findings plus look-ahead sheets) or Word, and offer a management version through the walkthru-management-update skill.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Interpretation limits

The helper does not reschedule P6, calculate a longest path, establish delay causation or assess EOT entitlement. It separates activities by project ID and uses each project's own data date. Both primary and secondary constraints are checked. Unknown/invalid project IDs, numeric values and dates fail with a clear error; missing calendars produce explicit fallback warnings. Obtain P6's hours/day and critical settings before relying on converted day values. If no data date is available, date-dependent checks are not performed.

For an ordered driving path, request P6's verified longest-path / float-path export with activity IDs, relationship details and scheduling settings. Label conclusions from float-only exports as indicators. The current-project planned-finish comparison is not a baseline comparison. Match approved baseline and current rows by project/activity ID before calculating baseline slippage. Preserve source hours and project IDs in evidence.

