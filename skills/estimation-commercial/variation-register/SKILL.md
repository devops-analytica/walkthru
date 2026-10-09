---
name: variation-register
description: "Create or update a VO/VR register from client or consultant instructions, emails and site notes: VR number, reference instruction, scope, status (notified, submitted, under review, approved, rejected), claimed vs approved value, time impact flag and a revised contract value summary, and draft the variation request cover note. Use when a commercial, projects or QS person says 'update the VO register', 'log this variation', 'new VR for this instruction', 'what is our revised contract value', 'variation status', 'draft the VR cover letter', or pastes an instruction, RFI reply, email chain or site note that changes scope. Approval status comes only from evidence; it does not submit or approve."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Variation register (VO / VR)

## When to use
Projects coordinators and QS prepare and maintain variation registers, compile requests with supporting documents, track VO/VR status, values and approvals, and keep revised contract-value information updated (Hana Rifai profile, task 3). The commercial manager tracks "every change on each project", and each variation takes about 2 hours: BOQ breakdown, Word letter, merged PDF, submit, update the register (Kareem Al Sayed profile). Use this for the register and cover note; the BOQ breakdown values come from the user or from the `quotation-comparison` skill output.

## Inputs
Read [project-context.md](references/project-context.md). Need: the existing register (if any), new instruction/email/site note, original contract value and previously approved variations, as-of date. Use [variation-register.csv](assets/variation-register.csv) if no company register exists. VR and VO numbering follows the project's convention; never invent a number: propose "Next number to confirm".

## Steps
1. **Classify each source item** as Instruction received (VO from client/consultant), Contractor-initiated request (VR), Notice of change/possible claim, or Not a variation (clarification only). Record the instruction reference, date, issuer and quoted words. A verbal or site-note instruction is "Instruction not in writing" and flagged, because the contract notice conditions need confirmation (FIDIC or project contract clause to confirm).
2. **Match to the register** by VR/VO number or instruction reference. Update the existing row; keep earlier status and value in a history note rather than overwriting. Duplicates and split instructions are flagged.
3. **Status from evidence only.** Notified / Submitted / Under review / Approved / Rejected / Withdrawn. Approved requires a cited approval document (signed VO, approval email, instruction with value). "Verbally agreed", "no objection" or silence stays Under review or Submitted. Keep source qualifiers ("pending", "reported").
4. **Values.** Claimed amount (ours, as submitted), approved amount (as approved), each with source, currency, VAT basis. Approved can differ from claimed; show the difference as a calculation. Unknown is blank/"Not supplied", not zero. Do not price the variation unless the user supplies the breakdown.
5. **Time impact.** Flag Yes / No / Unknown with reason and any EOT notice reference. "Unknown" is the default; do not assert delay without programme evidence.
6. **Revised contract value summary.** Original contract value + approved variations (sum of approved only) = revised contract value, shown beside pending (submitted/under review) and rejected totals separately. Needs the original value and a complete register; otherwise show "Partial: register may be incomplete".
7. **Cover note.** Draft the variation request letter: project, to-whom (To confirm), reference instruction, scope summary, claimed value and basis, time impact statement or reservation, enclosures list, notice-clause reference as supplied. Unsent draft, for the authorised signatory.

## Output
```
VARIATION REGISTER · <project> · as of <date> · source <files>
REGISTER | VR/VO no | Ref instruction (date, issuer) | Scope | Status + evidence | Claimed | Approved | Diff | Time impact | Next action/owner (To confirm) |
CHANGES THIS UPDATE: new / status changed / values changed
REVISED CONTRACT VALUE | Original | Approved VOs | Revised | Pending | Rejected | Basis + completeness
FLAGS: instruction not in writing; approved without document; time impact unknown; duplicate
Reported fact / Calculation / Inference to confirm / Recommendation
COVER NOTE (draft, unsent)
```

Handoff: keep project ID, as-of date, VR/VO numbers and unresolved flags for payment-application or cash-flow work; the register totals are inputs to those, not approvals. Offer the register as CSV or Excel.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Interpretation limits
No entitlement, approval or time extension is asserted. Notice deadlines depend on the contract; this skill does not compute them without the clause. Rehearse with [practice.md](references/practice.md).
