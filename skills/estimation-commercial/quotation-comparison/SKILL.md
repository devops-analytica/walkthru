---
name: quotation-comparison
description: "Compare supplier and subcontractor quotations for one package against the BOQ and specification scope: normalise units and inclusions/exclusions, flag missing items, non-compliant specs, validity, payment terms and lead times, and produce a comparison table with clarification questions. Use when an estimator or QS says 'compare these quotes', 'which supplier is cheapest', 'level the quotations', 'quote comparison for the MEP package', 'check this subcontractor offer against the BOQ', 'what is missing from their quote' or pastes two or more quotations for a tender or an LPO. Recommends and lists clarifications; never awards or accepts."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Quotation comparison

## When to use
Estimators and QS at WalkThru send drawings, specs and BOQ packages to suppliers and subcontractors, then line up replies that arrive in different formats (Kareem Al Sayed profile: "a quote comparison sheet that lines up different suppliers' formats"). Operations managers also compare quotes for small inquiries and specific activities (Wissam Alhadwi profile). A lowest total is only comparable once scope, units and exclusions are levelled. Use this when two or more quotes exist for the same package, or one quote must be checked against the BOQ/spec before negotiation or an LPO request.

## Inputs
Read [project-context.md](references/project-context.md). Need: the package scope (BOQ lines and spec sections or the RFQ as sent), each quotation (pasted, PDF, Excel, email), and the as-of date. Optional: budget/dry-cost per item, required-on-site date, company payment-term preferences. If the RFQ as sent is missing, compare against the BOQ and say the scope baseline is the BOQ, not the RFQ.

## Steps
1. **Baseline.** List the BOQ/spec items the package must cover (item ref, description, unit, quantity, governing spec). This is the yardstick, not any bidder's offer.
2. **Normalise each quote** into the baseline items: unit (m, m2, m3, nos, LS, kg vs tonne), quantity quoted, rate, amount, currency, VAT stated or not. Recompute amount = quantity x rate and report arithmetic differences; do not silently correct them. Do not convert units or treat products as equivalent without a stated basis; mark "Conversion to confirm".
3. **Scope level.** Per bidder mark each baseline item: Included / Excluded / Not mentioned / Alternative offered / Quoted as provisional or LS. "Not mentioned" is not "included". Capture common exclusions (supply only vs supply and install, testing and commissioning, shop drawings, transport/offloading, scaffolding, warranty, builder's work, taxes, permits).
4. **Spec compliance.** Compare brand, model, grade, thickness, finish, standards and approvals with the spec. Flag deviations, "or equivalent" offers and anything needing consultant approval. Compliance is "Not verified" without the datasheet.
5. **Commercial terms.** Validity (expiry vs as-of date), payment terms, advance/retention requested, delivery or lead time (with its trigger), price basis (fixed/rate-only), warranty, currency, conditions that conflict with the contract.
6. **Levelled view.** Show the quoted total and, only where every adjustment is evidenced, an "indicative adjusted" figure adding a clearly sourced allowance for gaps (for example another bidder's price for the same missing item, or the dry-cost line). Label allowances as Calculation or Inference, never as the bidder's price.
7. **Recommendation, not award.** State which quote looks best on supplied evidence and why, which are not yet comparable, and the clarifications that would change the ranking. Commitment, negotiation outcome and PO/LPO approval stay with the authorised WalkThru approver.

## Output
```
QUOTATION COMPARISON · <package> · <project/tender> · as of <date>
Baseline: <BOQ/RFQ ref, revision>   Quotes received: <n> (<names + dates>)

TABLE (one row per baseline item; one column group per bidder)
| Item | Unit/Qty | Bidder A rate/amount/status | Bidder B ... | Budget | Note + source |
TERMS | Bidder | Validity | Payment | Lead time | Warranty | Price basis | VAT |
EXCLUSIONS / MISSING | Bidder | Item | Status | Why it matters |
SPEC FLAGS | Bidder | Item | Offered vs required | Datasheet seen? |
TOTALS | Quoted | Arithmetic check | Indicative adjusted (basis) |

Reported fact / Calculation / Inference to confirm / Recommendation
CLARIFICATIONS (per bidder, drafted, ready to send after review)
NOT CHECKED: <what could not be assessed and why>
```
Offer the table as [comparison.csv](assets/comparison.csv) or an Excel file if available. Quote bidder wording for exclusions.

## Project context and evidence

Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Interpretation limits
Prices are as quoted and unverified against market. Missing items are not zero cost. Do not rank on price while scope gaps are open; say "not yet comparable". Rehearse with [practice.md](references/practice.md).
