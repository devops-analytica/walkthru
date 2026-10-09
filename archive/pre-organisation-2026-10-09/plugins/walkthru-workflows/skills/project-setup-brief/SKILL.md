---
name: project-setup-brief
description: "Turn a new project's contract, BOQ, specs and drawings into a project brief, draft WBS and activity list for the P6 baseline. Use when setting up a new project."
metadata:
  version: "1.1.0"
  review_date: "2026-10-08"
  owner_role: "WalkThru AI lead / trainer"
---

# Project Setup Brief

## When to use

Reads a new WalkThru project's contract documents, BOQ, specifications and drawings and produces a project brief (scope, key dates, milestones, LDs, constraints, risks) plus a draft WBS, activity list with durations, logic and resource assumptions, as a starting point for the baseline programme in P6. Use whenever someone starts a new project, prepares a baseline programme, uploads a tender or contract package, BOQ or scope of works and asks for a WBS, activity list, programme structure, durations, resource loading or a project summary, even if they only say "help me set up this project".

Preparing a new baseline programme takes WalkThru's planning team about a week. Much of it is reading the package to find dates, milestones, scope and constraints, then building the WBS and activity list. This skill drafts both so the planner starts from a structured draft, with assumptions and missing inputs visible.

## Inputs

Contract or appendix (dates, milestones, LDs, programme clause), BOQ, specifications, drawings (PDF), tender programme if any, and site constraints the user mentions. Read everything provided before drafting. Large packages: start with the contract particulars, BOQ summary and drawing list, then go deeper where needed.

## Part 1: Project brief

```
PROJECT BRIEF · <project>
Client / Consultant / Contract form (e.g. FIDIC Red Book 1999, bespoke)
Contract value · Commencement · Completion · Duration (calendar days)
Milestones and sectional completions (with LDs per day/week if stated)
Scope summary: building type, floors/areas, main trades (structure, MEP, fit-out, external)
Key constraints: access, working hours, authority approvals, long-lead items, nominated subcontractors, client-supplied items
Programme requirements: submission deadline, software, level of detail, cost/resource loading, update frequency
Risks and missing information: list, each with the document it should come from
```

Cite the document and page or clause for every date, milestone and LD figure, because the planner will check them.

## Part 2: Draft programme structure

1. **WBS**: Project → Area/Zone (villa, block, floor) → Trade/Phase. Include Preliminaries & Mobilisation, Engineering & Approvals (shop drawings, material submittals, authority NOCs), Procurement (long-lead items), Construction by area, Testing & Commissioning, Handover & Snagging.
2. **Activity list** (Excel): WBS code, Activity ID (follow WalkThru's coding if a sample is given; otherwise `<AREA>-<TRADE>-<nnn>`), name, duration (working days), predecessor(s) with relationship type, resource/trade, quantity basis.
3. **Durations**: work them out as quantity ÷ productivity rate ÷ crew where the BOQ gives quantities. Show the rate and crew used in a column so the planner can adjust them. Mark rates you assumed as "assumed".
4. **Logic**: finish-to-start by default; start-to-start with lag for overlapping trades on the same floor; no open ends except the start and finish milestones; no constraints except contract milestones.
5. **Resources** (if asked): manpower by trade per activity, and a histogram summary by month.

## Output

Brief as Word; activity list as Excel ready to import into P6 (one row per activity, relationships in a second sheet). End with "Assumptions to confirm" and "Information still required", so nothing assumed is mistaken for contract fact.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.
