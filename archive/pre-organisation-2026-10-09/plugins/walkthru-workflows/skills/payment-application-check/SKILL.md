---
name: payment-application-check
description: "Check a client or subcontractor payment application against BOQ, last certificate, site progress, variations, advance and retention; list queries."
metadata:
  version: "1.1.0"
  review_date: "2026-10-08"
  owner_role: "WalkThru AI lead / trainer"
---

# Payment Application Check

## When to use

Reviews a WalkThru monthly payment application (client interim payment application/IPC, or a subcontractor's payment application) against the BOQ, the previous application, site progress records and approved variations. It checks claimed progress against actual work, cumulative maths, advance recovery, retention, variations and VAT, and lists the queries and the amount supported. Use whenever someone uploads a payment application, IPA, IPC, valuation, progress claim or subcontractor payment certificate and asks to check, review, prepare or verify it, or asks "does this claim match site progress", even if only the Excel sheet is shared.

Payment applications decide WalkThru's cash flow (client IPAs) and its costs (subcontractor claims). Over-claiming from the client leads to rejection and lost credibility; over-certifying subcontractors leads to overpayment. The operations managers must confirm that claimed progress matches what is actually built. This skill does the arithmetic and cross-checks so they can focus on the site judgement.

## Inputs

- The payment application (Excel or PDF).
- The previous application/certificate for cumulative figures.
- The BOQ / schedule of values with contract quantities and rates.
- Progress records: daily reports, measurement sheets, progress %, photos, P6 actual %.
- Variation register (approved vs pending).
- Contract or subcontract terms: retention %, retention cap, advance payment % and recovery rate, payment terms.

Work with what is provided and list what was not available to check.

## Checks

1. **Arithmetic**: each line's previous + this period = cumulative; qty × rate = amount; totals add up; rates match the BOQ.
2. **Progress vs evidence**: claimed cumulative % or quantity per item vs progress records. Flag items claimed ahead of evidence, and items with evidence but not claimed (under-claimed money for client IPAs).
3. **Over 100%**: cumulative quantity above BOQ quantity without an approved variation.
4. **Variations**: only approved variations at their approved values; pending ones shown separately if the contract allows.
5. **Materials on site**: claimed only where the contract allows and with delivery evidence.
6. **Advance recovery**: deducted at the contract rate, and the cumulative recovery does not exceed the advance.
7. **Retention**: correct % on the right base; cap applied; release only when contractually due.
8. **Previous certified vs previous claimed**: start from the certified figures, not the previous claim.
9. **VAT**: establish the applicable rate and taxable base from the supplied contract/transaction evidence and finance policy. Show that base and calculation separately; do not automatically apply 5% to net cash due.

## Output

```
PAYMENT APPLICATION CHECK · <project> · <client IPA No. / subcontractor + PA No.> · period <month>

SUMMARY
Claimed this period: AED <x> · Supported by evidence: AED <y> · Difference: AED <x−y>

QUERIES
| BOQ item | Description | Claimed (cum.) | Evidence shows | Difference (AED) | Query / action |

DEDUCTIONS CHECK
Advance recovery: <ok / issue> · Retention: <ok / issue> · Variations: <ok / issue> · VAT: <ok / issue>

UNDER-CLAIMED (client IPAs only)
| BOQ item | Work done not claimed | Value (AED) |

NOT CHECKED: <items or documents not provided>
```

Offer a corrected application sheet with comments in a separate column, and draft comments to the PM or subcontractor. The manager decides the certified amount; Claude only recommends.

The figures in any certificate are binding once signed, so quote every number from the source documents and use Decimal arithmetic at full calculation precision and apply only the confirmed currency/tax rounding policy at the specified step. Document that policy; do not silently round comparisons.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Evidence and reconciliation states

Use Pass / Exception / Not checked / Not applicable for every deduction and evidence check. Without prior certified amounts, agreed retention/advance rules or a measured progress basis, do not present a final supported certificate total. Show a provisional line reconciliation and the unresolved inputs instead. P6 physical %, duration % and measured BOQ progress are different measures; one cannot certify another without an agreed quantity/valuation mapping. Distinguish approved variations from pending ones, and cite the approval reference. Certification remains the responsible manager's decision.

