---
name: programme-comment-response
description: "Comment Response Sheet for consultant or client comments on a submitted programme (baseline, revised or recovery), plus the list of P6 revisions to make. Use when someone uploads programme comments, a rejection or 'Revise and Resubmit' letter, a comment sheet, or asks to respond to programme comments, prepare a compliance statement, or 'reply to the consultant's comments on the baseline', including comments inside an email or marked-up PDF."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Programme Comment Response Sheet

## When to use

Turns a consultant's or client's comments on a submitted WalkThru programme (baseline, revised or recovery programme) into a Comment Response Sheet showing the response and action taken for each comment, plus the list of revisions to make in P6. Use whenever someone uploads consultant comments, a programme rejection or "Revise and Resubmit" letter, a comment sheet, or asks to respond to programme comments, prepare a compliance statement, or "reply to the consultant's comments on the baseline", even if the comments are inside an email or a marked-up PDF.

Consultants usually return programmes with a list of comments, and resubmissions are judged on whether each comment was addressed. A clear response sheet that ties each comment to a specific change in the programme gets approvals faster and protects WalkThru's position on comments it does not accept.

## Inputs

- The consultant's comments (letter, comment sheet, email or marked-up PDF).
- The programme: P6 `.xer` or Excel export, and the narrative if any. Use it to check whether each comment is already addressed and to cite activity IDs.
- The contract requirements if provided (programme clause, milestones, specification section on programmes).

## Steps

1. Number every comment exactly as the consultant numbered it. If they didn't number them, number them in order and keep their wording verbatim in the sheet.
2. For each comment, decide the response type:
   - **Proposed revision**: a change is needed but not yet made. Describe the intended change and references; keep it Open. **Implemented**: the revised programme contains the change, with a revision/date and activity references. **Verified**: the Planning Manager or documented comparison confirms the change meets the comment. Only Verified items can be Closed.
   - **Clarified**: the programme already complies; explain where, with activity IDs.
   - **Not accepted**: give the contractual or technical reason, politely and factually. Recommend this only with a clear reason and mark it for the Planning Manager's decision.
   - **Information required**: WalkThru needs something from the consultant or client to respond.
3. Build the list of P6 revisions the planner must make for every proposed or implemented revision.

## Output

**Comment Response Sheet** (Excel, also shown in the reply):

| No. | Consultant comment (verbatim) | Response type | Proposed action / verified response | Programme revision and source | Activity ID / WBS | Evidence state | Reviewer | Status |

Evidence state: Proposed / Implemented / Verified. Status: Closed only after verification; otherwise Open. An intended future change is never evidence of completion.

**P6 revision list**:

| # | Change in P6 | Activities affected | Related comment No. |

**Cover note**: a short draft letter for the resubmission (use the walkthru-letters skill style) reporting the actual count of Verified/Closed and Open items. Say all comments are addressed only when every item has verified supporting evidence. Otherwise state what remains and the intended next revision; do not draft a false completion claim.

## Tone

Respectful and factual. Agree where the consultant is right. Where WalkThru disagrees, say so once, with the reason and a reference, and avoid argument. If a comment asks for something that changes WalkThru's time or cost entitlement (for example removing float ownership or adding constraints that absorb delays caused by others), flag it to the user before answering.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.
