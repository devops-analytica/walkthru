# WalkThru Skills

Revision 1.1.0 · Built 08 Oct 2026 from the 13 WalkThru role profiles (`../Re__Walk_Thru_AI_Program_Presentation_Day_1/`).

```
general/    7 skills for every employee (share company-wide)
group-4/    8 skills for Operations (Wissam, Rami) and Planning (Hosam, Menna)
dist/       UPLOAD THESE: one zip per skill (Claude takes one skill per zip)
share/      bundles for emailing or passing around; do NOT upload these to Claude
samples/    made-up daily reports, LPO and invoice for demos when trainees forget samples
```

## General: for everyone

| Skill | What it does | Profiles asking for it |
|---|---|---|
| walkthru-morning-brief | Inbox into Action today / Reply / FYI by project | 8 of 13 |
| walkthru-action-tracker | Excel follow-up register, chase list, chase messages | 7 |
| walkthru-chat-to-actions | WhatsApp/Teams chat into decisions, actions, open questions | 6 |
| walkthru-management-update | One-page MD/GM update: issue, impact, recommendation, owner, date | 6 |
| walkthru-meeting-minutes | Notes or transcript into a formal MOM with action table | 5 |
| walkthru-letters | Letters and formal emails in house style, English/Arabic | 5 |
| walkthru-deadline-watch | Any dated register into overdue / 7 / 14 / 30-day lists | 4 |

## Group 4: Operations and Planning

| Skill | For | What it does |
|---|---|---|
| p6-programme-review | Hosam, Menna, Ops | XER or Excel export into schedule-health/float indicators, planned-date slippage, logic issues, project-specific look-ahead and actions (includes `scripts/xer_check.py`) |
| planning-weekly-report | Hosam, Menna | Weekly/monthly report draft from P6 + progress + logs |
| programme-comment-response | Hosam, Menna | Consultant comments into a comment response sheet + P6 revision list |
| project-setup-brief | Hosam, Menna | Contract/BOQ/specs into project brief, draft WBS and activity list |
| daily-site-report-digest | Rami, Wissam | All daily reports into one exceptions digest + manpower moves |
| invoice-po-check | Wissam, Rami | Invoices vs PO/GRN into evidence-state / exception list + vendor emails |
| payment-application-check | Rami, Wissam | IPA or subcontractor claim vs progress, BOQ, deductions |
| submittal-wir-tracker | Rami, Wissam | Submittal and WIR logs into "our side" vs "consultant side" chase lists |

## Install

1. **Turn on code execution.** Skills only work when "Code execution and file creation" is enabled. On Team/Enterprise the org owner enables it (and Skills) for the organisation first.
2. **Upload.** Upload one zip from `dist/` per skill in Claude's Skills settings. On Team/Enterprise the org owner can provision them for everyone instead; see Anthropic's "Provision and manage skills for your organization" help article.
3. **Claude Code:** copy the skill folder into `~/.claude/skills/`.

All 15 meet claude.ai's upload rules: description ≤ 200 characters, name ≤ 64, skill folder at the zip root. The current release validates metadata, relative references, exact ZIP/source parity, canonical helper parity and Python syntax using `maintenance/validate_release.py`. These checks do not prove model behavior. Each skill's detailed trigger wording sits in its "When to use" section, because the 200-character description is too short to hold it.

## Before the workshops (Sat 10 and 17 Oct)

- The defaults (report layouts, MOM format, letter reference style) are generic. When WalkThru sends its real templates, put them in each skill (or just upload them alongside a request; every skill follows an uploaded template over its default).
- The P6 helper has deterministic synthetic regression tests, including multi-project dates and fractional float. Real WalkThru XER acceptance is still required before the session; record it in `releases/acceptance-log.json`.
- All skills draft and recommend; none send, approve or change anything.

## 1.1.0 evidence and release changes

Shared configuration/evidence references are included in every skill ZIP. Invoice checks never turn missing history into a pass; deadline monitoring preserves approved/renewed expiry rows; report variance is actual minus planned in percentage points; programme revisions stay Open until verified. No universal tax or contractual review-period assumptions.

Use one route: role-specific standalone skills, or the generated `walkthru-workflows` plugin. Installing both creates duplicate skills. The sharing ZIPs contain upload ZIPs; upload the individual files from `dist/`, not the sharing bundle.

Rebuild packages from the canonical helpers using `python3 maintenance/build_release.py` at toolkit root. Run `python3 maintenance/validate_release.py` after any change. See root CHANGELOG and the release manifest. Upload replacement ZIPs and confirm the version; previous installs do not update automatically.
