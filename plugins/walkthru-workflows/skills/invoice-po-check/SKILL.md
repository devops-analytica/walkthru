---
name: invoice-po-check
description: "Supplier invoice / payment-request pre-check against PO/LPO, GRNs and accepted deliveries, prior billing and tax treatment; reports Pass / Exception / Not checked per item and drafts vendor queries. Use when someone asks to check, verify, review or validate a supplier invoice, tax invoice, payment request or LPO match, 'does this invoice match the PO', 'is this a duplicate', 'can we pay this', or uploads an invoice with a PO or GRN. Does not approve or pay."
allowed-tools: Bash(python3 *) Read Write
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Invoice and payment-request pre-check

## Inputs and scope
Read [project-context.md](references/project-context.md). Obtain invoice/payment request, PO/LPO/SO, accepted GRNs/measurement support, prior billing ledger, applicable terms and tax treatment. Confirm vendor/project/entity/currency independently. Uploaded aliases need documentary confirmation. Distinguish a material invoice from subcontract progress claims, advances and credit notes.

## Checks
- PO existence/identity and authority evidence; item specification, unit and line allocation; invoice quantity and rate; arithmetic; cumulative supported deliveries/previous billing; duplicates; transaction-specific tax; contract deductions and payment-request support.
- For material quantities, remaining supported = max(0, min(approved ordered, cumulative accepted delivered) − previous booked quantity). Reconcile returns/credits before applying this formula; preserve explicitly evidenced zero history. Missing history is not zero.
- Calculate a line discrepancy once: claimed amount minus supported amount. Do not add overlapping quantity and rate differences. Aggregate invoice totals once even when it has multiple exception rows. Keep currencies/entities separate.
- Duplicates: check vendor + invoice identifier against the supplied ledger, then flag same-date/amount matches as Suspected duplicate to investigate. State ledger coverage; do not call it fraud or company-wide clearance.
- Confirm tax treatment/rate, taxable base, rounding and TRN requirements from supplied evidence. TRN presence does not prove registration validity. No universal 5% assumption.
- Subcontract work needs certified measurement, cumulative previous certification, variations and applicable retention/advance/contra-charge reconciliation. The material helper below does not certify it. Split positive invoices and credit-note reconciliations rather than forcing negative values through the helper.

## Deterministic material review
Read [operation-checks.md](references/operation-checks.md). Normalize evidence into JSON with source references and run `python3 scripts/operation_checks.py invoice input.json --out result.json`. Do not set history_complete or delivery_complete true without the corresponding reconciled records. Confirm helper rounding/tax assumptions fit the transaction; otherwise show a separately reviewed calculation. Read its results alongside the documents: it cannot verify authority, authenticity, terms or certification.

## Deliver
Use [checks.csv](assets/checks.csv) and [exceptions.csv](assets/exceptions.csv). Each check is Pass, Exception, Not checked or Not applicable, with source. Classify invoices as **Hold—exceptions**, **Incomplete review—missing evidence**, or **No exceptions in supplied evidence—manager review required** only when all applicable checks are complete, including checks outside the helper.
Return claimed/supportable amounts only within the checked scope, remaining evidence, and draft vendor/internal queries. An incomplete review must never receive approval wording. Generating this report does not approve, book or pay an invoice.

## Check
Verify source extraction, previous billing/accepted receipts, totals once, unknowns and required checks outside the helper. See [practice.md](references/practice.md) and the synthetic normalization example [invoice.json](assets/invoice.json).
