---
name: submittal-wir-tracker
description: "Turn submittal and WIR logs into chase lists: what WalkThru must close, what is overdue with the consultant, and what blocks upcoming site work."
metadata:
  version: "1.1.0"
  review_date: "2026-10-08"
  owner_role: "WalkThru AI lead / trainer"
---

# Submittal and WIR Tracker

## When to use

Reads WalkThru's submittal log (shop drawings, material submittals, method statements) and WIR/inspection request log for one or more projects and produces a chase list split into "action on WalkThru's side" and "waiting on consultant", with overdue items, rejections to resubmit, and items that block upcoming site work. Use whenever someone uploads a submittal log, document register, WIR log, inspection request register or RFI log, or asks "what's pending with the consultant", "which submittals are overdue", "what do the engineers need to close", even if they only paste part of the log.

Unapproved shop drawings, materials and inspections are one of the most common reasons WalkThru's site work stops. The operations manager needs two lists every week: what WalkThru's own engineers and subcontractors must close, and what the consultant is sitting on. This skill builds both from the existing logs.

## Inputs

- Submittal log (Excel/PDF): reference, title, type, revision, submitted date, consultant due date, status/code (A Approved, B Approved as noted, C Revise and resubmit, D Rejected, or the project's own codes), response date.
- WIR / inspection log: reference, activity, location, requested date, inspection date, result.
- Optional: the programme look-ahead (to find items blocking upcoming work) and the confirmed contractual review period and calendar-day/working-day basis. Do not invent 14-day or 1–2-day contractual periods. If neither a due date nor a confirmed review rule exists, mark Due unknown and request the basis.

Read the project's own status codes from the log's legend if present, and say how you mapped them.

## Classify each open item

**WalkThru side (our action)**
- Code C or D: revise and resubmit; days since the response.
- Approved as noted (B) with comments to incorporate before construction.
- Not yet submitted but needed for work in the next 3 weeks.
- WIR failed: rectify and re-inspect.

**Consultant side (chase)**
- Submitted and past a supplied due date or confirmed review period with no response; state the due-date source and day basis. If the basis is missing, show Submitted / due unknown rather than Overdue.
- WIR requested and not inspected on the requested date.

**Blocking work**: any open item linked to an activity starting in the next 21 days (match by trade, area or activity name when the log has no activity link; say it is a match to confirm).

## Output

```
SUBMITTAL & WIR STATUS · <project(s)> · as of <date>

BLOCKING UPCOMING WORK (<n>)
| Ref | Title | Needed for | Start date | Status | Action |

OUR SIDE: TO CLOSE (<n>)
| Ref | Title | Status/code | Days open | Responsible (engineer/subcontractor) | Action |

CONSULTANT SIDE: TO CHASE (<n>)
| Ref | Title | Submitted | Due | Days overdue |

SUMMARY: submitted <n> · approved <n> · under review <n> · to resubmit <n> · overdue with consultant <n>
```

Offer a draft chase email to the consultant listing all overdue items with references and dates (polite, factual, noting potential programme impact for items blocking work), and a list per engineer for the internal follow-up. Nothing is sent by Claude.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Due-date evidence

An explicit log due date remains traceable to its row; verify its contractual basis separately when needed for a notice. If the user asks for an assumed internal planning deadline, label it Provisional and keep it outside confirmed-overdue totals. Use the project's status legend; flag unknown codes instead of forcing the generic A–D mapping. Revised submissions are separate revision records; calculate review time from the applicable revision, not the superseded submission.

