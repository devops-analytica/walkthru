---
name: invoice-po-check
description: "Check supplier and subcontractor invoices against POs, GRNs and ePromis exports; list exceptions with approve or hold advice and draft vendor emails."
metadata:
  version: "1.1.0"
  review_date: "2026-10-08"
  owner_role: "WalkThru AI lead / trainer"
---

# Invoice vs PO Check

## When to use

Checks WalkThru supplier and subcontractor invoices against their purchase orders (PO/LPO/SO), delivery notes or measured quantities, and ePromis exports before the Operations Manager approves them to Accounts. It lists only the exceptions (no PO, quantity or rate above the order, duplicates, arithmetic or VAT errors, missing deductions or support) with a hold/approve recommendation and draft comment emails. Use whenever someone uploads invoices with POs or an ePromis invoice or PO export and asks to check, verify, approve or review them, or asks "which invoices can I approve", even for a single invoice.

Every WalkThru supplier and subcontractor invoice passes Project Manager, Cost Control, Commercial and Operations Manager approval before Accounts books it, and invoices often wait at the Operations Manager stage. This skill does the line-by-line comparison so the manager reviews only the exceptions and approves the clean ones quickly.

## Inputs

- Invoices: PDF, photo or Excel (one or many).
- Purchase orders / LPOs / subcontract orders: PDF or an ePromis export.
- Optional: delivery notes/GRNs, measurement sheets or progress for subcontract work, previous invoices from the same vendor (for duplicates and cumulative checks), the vendor's TRN.

If only an ePromis export is provided, work from it and say that supporting documents were not checked.

## Checks per invoice

1. **PO exists** and is for the same vendor and project.
2. **Items match the PO**: description, unit.
3. **Quantity**: compare the current invoice to unbilled supported quantity: max(0, min(approved ordered quantity, cumulative accepted delivered quantity) − previous booked quantity). Reconcile returns, cancellations and credits separately. Without complete GRN/DN history or prior billing quantities, mark this check Not checked.
4. **Rate**: invoiced rate = PO rate. Any difference is an exception, even if it's small.
5. **Arithmetic**: qty × rate = line total; lines sum to subtotal.
6. **VAT**: confirm transaction-specific rate, treatment and taxable base from supplied evidence; do not assume all transactions are 5%. Check arithmetic and supplier TRN presence where applicable. Presence of a TRN is not validation of registration.
7. **Duplicates**: same invoice number, or same amount and date from the same vendor, already seen.
8. **Subcontract deductions**: retention, advance recovery, contra-charges, back-charges applied as per the subcontract terms if provided.
9. **Support**: delivery notes, timesheets or measurement attached where the PO type needs them.

## Output

Start with a one-line answer to the user's question, for example "No, hold it: rate and quantity exceed LPO-4410 by AED 2,205.00 incl. VAT" or "Yes, all 12 invoices match their POs".

```
INVOICE CHECK · <date> · <n> invoices · AED <total>

NO EXCEPTIONS IN SUPPLIED EVIDENCE — MANAGER REVIEW REQUIRED (<n>) · AED <total>
| Invoice No. | Vendor | Project | PO | Amount (AED) |

HOLD: EXCEPTIONS (<n> invoices) · AED <total of held invoices>
| Invoice No. | Vendor | Project | PO | Invoice amount | Exception | Difference excl. VAT | Difference incl. VAT | Recommended action |

INCOMPLETE REVIEW (<n>): <missing PO, billing history, GRNs, terms or unreadable evidence>
```

- Use one row per exception. When an invoice has several exceptions, repeat the invoice number on each row and show the invoice amount only on the first row, so totals are not double-counted.
- After the table, give the total overcharge per invoice and the amount the documents actually support.
- Add a check matrix with **Pass / Exception / Not checked / Not applicable**, plus the evidence reference. List missing evidence explicitly. A complete supplied ledger can support “no duplicates found in this ledger”; a partial or absent history cannot.
- Match vendor and project IDs independently of the PO number. Accept naming aliases only when the project configuration or source documents confirm them; otherwise flag a match to confirm.

Then draft short emails:
- **To the vendor:** one per vendor, listing each issue and what is needed (credit note, revised invoice, missing delivery note).
- **To the Project Manager:** only when a quantity exceeds the PO or delivered quantity, or the work needs site confirmation. Ask them to confirm with Estimation before anything is booked.

## Rules

- Show the exact figures from both documents for every exception, so the manager can see it without opening the files.
- "Recommended action" is a suggestion. The manager approves, and nothing is approved or sent by Claude.
- Quantities above the PO need PM and Estimation confirmation before booking (company procedure); say so in the action.
- Offer the results as an Excel sheet the Accounts team can use.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Deterministic reconciliation

For material invoices normalize the supplied evidence into JSON and run `python scripts/operation_checks.py invoice <normalized.json> --out <result.json>`. Read [operation-checks.md](references/operation-checks.md) for fields and limits. Preserve the original files and cite the extraction. This helper does not extract PDFs, certify subcontract work, validate tax registration or approve in ePromis.

Reconcile each line once: invoiced amount minus the amount supported by the permitted quantity and rate. Do not add overlapping quantity and rate differences twice. Use complete history to verify prior quantities; preserve explicitly supplied zero-history evidence. Mark suspected duplicates for investigation rather than declaring fraud. Applicable subcontract deductions need a contract reconciliation and stay Not checked until done. Never return a clean-review bucket while a required check is Not checked.

