---
name: walkthru-material-delivery-tracker
description: "Track material requirements, procurement stages and accepted deliveries against site need dates; draft supplier follow-ups and flag shortages."
metadata:
  version: "1.0.0"
  reviewed: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Materials and delivery tracker

## Inputs
Read [project-context.md](references/project-context.md). Use material requests, requisitions/RFQs, quotations, POs/LPOs, approval/fabrication logs, supplier commitments, GRNs/delivery notes, stock/issues/returns and a site look-ahead. Use [materials-register.csv](assets/materials-register.csv) if no company register exists. Confirm as-of date, project, item/specification, unit and workfront.

## Reconcile the chain
- Keep stages distinct: Requested → RFQ → Selected/approval pending → Ordered → Supplier acknowledged → Fabrication/shipped → Received → Accepted. A quotation is not an order; a PO date is not a delivery commitment; received/rejected goods are not usable stock.
- Match project + item/specification + PO line + unit. Keep partial deliveries separate and preserve delivery-note IDs. Deduplicate re-sent notes; reconcile cancellations/returns and conflicting revisions without silently overwriting them.
- Calculate accepted receipts net of returns; usable on-site balance = opening usable stock + accepted receipts − issued/consumed − returns, for the same period and unit. Do not subtract returns twice if a supplied accepted figure is already net. Unknown opening stock or movements means Usable balance unknown, not zero.
- Compare required quantity with known usable/unallocated quantity on the required date. Record future accepted/confirmed receipts separately from today's stock. No unit conversion, alternative product equivalence or allocation across sites without a confirmed basis.
- Separate Required-on-site date, Requested delivery, Supplier confirmed delivery and Actual receipt. Flag late confirmed dates, missing commitments and prerequisites (technical approval, payment, fabrication, permits). Quoted lead time needs its trigger date and calendar; otherwise an expected arrival is provisional.
- Describe programme exposure from the supplied activity link. A shortage with no required date is a quantity concern with date unknown, not proven delay. Do not place/cancel orders or promise suppliers payment.

## Deliver
Return stage register, confirmed late deliveries, missing commitments, known shortages/unknown balances, prerequisite actions and grouped supplier follow-up drafts. Preserve references and source-based dates; use the company escalation thresholds if supplied. Separate total ordered, received, accepted and usable quantities.

## Check
Confirm no duplicate receipts, no rejected goods counted as usable, no double-counted returns, mixed units or project stock. Rehearse with [practice.md](references/practice.md).
