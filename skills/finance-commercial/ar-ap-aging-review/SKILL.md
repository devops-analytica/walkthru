---
name: ar-ap-aging-review
description: "Receivable and payable aging review from ePromis or Excel aging exports: buckets (current, 1-30, 31-60, 61-90, 91-120, 120+ days past due), top overdue clients and suppliers/subcontractors, retention receivable by release date, items with disputes, holds or missing IPC/certificates, draft collection follow-up emails, and payment prioritisation inputs for the CFO. Use when someone says 'review the aging', 'AR aging', 'AP aging', 'who owes us', 'overdue invoices', 'weekly overdue list for the CFO', 'which clients to chase', 'draft collection emails', 'which suppliers to pay first', 'retention receivable', or pastes a receivables or payables aging list, statement of account or supplier chaser. Prioritisation is a recommendation, not a payment run; never promises payment to a supplier."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# AR / AP aging review

## When to use
The Chief Accountant keeps an Excel receivables aging and tells the CFO every week which client invoices are overdue. He also schedules supplier and subcontractor invoices by credit terms, aiming to pay 95% on agreed terms (profile: Islam ElGammal). The Finance Manager prepares AR/AP aging reports, follows up overdue client balances, and tracks certified amounts, retention and advances (profile: Hady Gebran). The CFO calls clients about overdue amounts and tracks receivable and retention release dates (profile: Rawad Saliby). This skill turns the aging exports into the weekly exceptions list and drafts the follow-ups.

## Inputs
Read [project-context.md](references/project-context.md). Use the as-of date and these exports:
- AR aging: client, project, tax invoice / IPC no., invoice date, due date, outstanding amount, notes.
- Retention schedule with release conditions or dates.
- Submitted-but-uncertified IPAs.
- AP aging: supplier/subcontractor, project, invoice / payment certificate no., due date or credit terms, amount, ePromis approval status, holds.
- Optional: the cash headroom from the `cash-position-reconciliation` skill, and any supplier chasers (email/WhatsApp).
Map columns using [aging.csv](assets/aging.csv) if the layout is unclear.

## Steps
1. **Bucket by days past due date** (Calculation, calendar days at the as-of date): Current (not yet due), 1–30, 31–60, 61–90, 91–120, 120+. If only the invoice date is given, use credit terms from the source to find the due date. If there are no terms, bucket by invoice age and label that basis. A missing due date goes on a "Missing date" list, not into Current.
2. **Take out of the buckets:**
   - Retention receivable: list it by release date or condition (handover, DLP end). It is not overdue before release.
   - Advances: list separately.
   - Submitted IPAs without a certificate or tax invoice: these are missing certificates, not receivables.

   **Keep in their age bucket but flag:** disputed items, and AP items on hold or not yet approved in ePromis. Give them their own follow-up. Keep them out of the standard chasers and out of "payable now".
3. **Totals per bucket**, separately for AR and AP and per entity and currency. Cross-check them against the export's own totals and show any difference.
4. **Top overdue.** List the top 5 clients and top 5 suppliers by overdue amount, with their oldest item and notes.
5. **Collection follow-ups (AR).** Draft one email per client, citing invoice/IPC numbers, amounts and due dates. Keep the tone factual and add no threats. Disputed items get a separate draft that asks for the specific point in dispute. Sender and recipient are "To confirm".
6. **Payment prioritisation inputs (AP)**, a recommendation for the CFO. Rank approved, undisputed items by:
   - overdue days against credit terms;
   - site impact, such as a supplier threatening to stop deliveries (impact to confirm with the PM);
   - urgency approved by the Operations Manager.
   Show each item's total against the cash headroom when it is supplied. Items not yet approved or on hold are listed as "not payable until resolved".
7. **Supplier replies.** Acknowledge the chaser, state the invoice's factual status, and say Accounts will revert once the payment schedule is approved. Never promise a date or amount, and never confirm payment.

## Output
```
AGING REVIEW · <entity> · as of <date> · sources: <files>
AR BUCKETS  | Current | 1–30 | 31–60 | 61–90 | 91–120 | 120+ | Total | (export total, diff)
AP BUCKETS  | same
TOP OVERDUE CLIENTS / SUPPLIERS  | Name | Overdue | Oldest item | Days | Notes |
RETENTION RECEIVABLE  | Client | Project | Amount | Release date/condition | Status |
DISPUTES / HOLDS / MISSING CERTIFICATES  | Item | Amount | Issue | Next step (owner: To confirm) |
COLLECTION DRAFTS  (one per client)
PAYMENT PRIORITISATION INPUTS (recommendation for CFO, not a payment run)  | Rank | Payee | Invoice | Amount | Days overdue | Reason |
SUPPLIER REPLY DRAFTS  (no date or amount promised)
```

## Project context and evidence
Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Interpretation limits
This skill does not send emails, approve, schedule or release payments, or change credit terms. The CFO decides payment priority and the authorised signatory releases payments. Pre-checking an individual supplier invoice belongs to the `invoice-po-check` skill. See [practice.md](references/practice.md).
