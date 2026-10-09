---
name: walkthru-letters
description: "Project correspondence drafting in English, Arabic or bilingual on WalkThru templates, from supplied facts and references only. Use when someone asks to write or draft a letter, email, notice, reply or response to a consultant, client, subcontractor, supplier or authority: 'write to the consultant about', 'draft a delay notice', 'reply to this letter', 'chase the supplier formally', 'letter in Arabic'. Returns a draft plus a pre-issue checklist; never issues it."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Project correspondence assistant

## Inputs and routing
Read [project-context.md](references/project-context.md). Establish the purpose, recipient, contracting entity, project, supporting chronology, references, language and intended signatory. Confirm the entity from the contract or approved letterhead; geographic location alone is not evidence. Missing reference numbers can be marked To confirm without blocking a useful draft.

This skill formats the user's correspondence. For RFI technical findings, commercial calculations or contractual notice requirements, use the supplied findings rather than inventing an engineering/legal analysis.

## Draft
- Prefer the approved letterhead/template or a supplied previous example. Otherwise use [letter-template.md](assets/letter-template.md); keep document numbering provisional unless supplied by the register.
- Structure around the reference, verified facts, the intended position/request and a clear next action. Distinguish confirmed dates from requested response dates.
- Keep chronology and source references correct. If evidence conflicts, flag it to the reviewer instead of silently selecting a favourable account.
- Do not add admissions, acceptance of price/scope, waived rights, guaranteed completion or threats unless instructed and supported. A routine delivery chase does not need automatic rights-reservation wording.
- For notices/time-bar-sensitive correspondence, ask for the applicable clause, service method and trigger evidence if absent; prepare the factual draft and label notice compliance Unverified. Do not invent a notice period or assert compliance from a generic FIDIC assumption.
- For Arabic/bilingual output, align factual content, numbering, names, dates, amounts and obligations between versions. Flag wording whose translation changes legal effect.

## Deliver
Return the draft and a separate pre-issue checklist: entity/signatory, references, dates/amounts, attachments and unresolved facts. Include cited source chronology in the reviewer copy, not invented attachments. Generate DOCX if available or editable Markdown otherwise. The draft is not issued correspondence.

## Check
Verify no invented reference, entity or commitment, and no material change in meaning from the requested response. Rehearse with [practice.md](references/practice.md).
