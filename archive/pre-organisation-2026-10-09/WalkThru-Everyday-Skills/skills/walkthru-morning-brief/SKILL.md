---
name: walkthru-morning-brief
description: "Sort supplied emails or an authorized inbox into project priorities, replies and FYI. Use for morning briefs and email triage."
metadata:
  version: "1.0.0"
  reviewed: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Morning priorities and email triage

## Inputs and scope
Read [project-context.md](references/project-context.md). Use emails with sender, recipients/CC, timestamp, subject, body and message ID. Resolve the employee's role and query window from the request. Without a stated window, propose a clearly labelled window rather than claiming the last working day is known. Read full actionable threads, including relevant CC items; subjects alone are insufficient.

## Workflow
- Consolidate threads and duplicates while preserving message references. A newer resolution can change an earlier action; retain its history.
- Route by the employee's responsibility, not whether they appear in To or CC. Separate **Action today**, **Reply needed**, **FYI** and **No action**. Deadline, site stoppage, reported HSE issue, rejected submission and explicit decision requests warrant attention; a sender's title or the word urgent alone does not establish urgency.
- Turn each action into a concrete verb, owner and confirmed deadline. Label inferred ownership/date as To confirm. If the user is not the decision-maker, describe their coordination action rather than asking them to approve.
- Keep automated messages containing failed submissions or real deadlines; ignore only those with no useful action. Keep source totals reconcilable; report any uninspected messages.
- List the highest-priority items first, followed by remaining actions. Do not silently drop items to meet a length limit. Draft responses only when asked or useful; never claim they were sent.

## Deliverable
Use [brief-template.md](assets/brief-template.md). Include coverage, project, action, owner, due/basis, priority reason and source; a compact FYI section; and unresolved evidence. Preserve amounts/references exactly. Recommendations are separate from message instructions.

## Check before delivery
Confirm every priority can be traced to inspected content, resolved threads are not still chased, and deadlines without a basis remain unknown. The two synthetic requests in [practice.md](references/practice.md) cover ordinary triage and misleading thread updates.
