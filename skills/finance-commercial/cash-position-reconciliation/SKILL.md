---
name: cash-position-reconciliation
description: "Daily cash position and bank reconciliation: matches bank portal balances and statement lines against the ePromis bank ledger and the finance team's daily Excel sheet, lists unmatched items (returned payments, unbooked client receipts, duplicates, bank charges, timing), confirms whether yesterday's approved payments and transfers went out, compares today's payment sheet and commitments with available cash, and drafts a short cash note for the Finance Manager or CFO. Use when someone says 'morning bank check', 'daily cash position', 'match the bank to ePromis', 'did yesterday's payments go out', 'any returned payments', 'which client receipts need booking', 'can we cover today's payment list', 'bank rec', or pastes a bank statement, ePromis ledger or daily payment sheet. Differences are reported, never forced."
metadata:
  version: "2.1.0"
  review_date: "2026-10-09"
  owner_role: "WalkThru AI lead / trainer"
---

# Cash position reconciliation

## When to use
Every morning the Chief Accountant matches bank balances (2 banks) against ePromis and the daily Excel sheet. The checks are: did yesterday's payments go out, are there returned payments, and which client receipts need booking (profile: Islam ElGammal). The Finance Manager reviews daily cash against immediate payment commitments (profile: Hady Gebran). The CFO checks bank portals each morning for balances and client receipts, and wants a daily cash digest across all banks (profile: Rawad Saliby, task 14). This skill does the matching and drafts the note. It does not book, reverse or release anything.

## Inputs
Read [project-context.md](references/project-context.md). For each bank account (entity, bank, last 4 digits, currency, as-of date):
- Bank statement or portal export: opening and closing balance, plus lines with date, amount, reference and narrative.
- ePromis bank ledger for the same account and dates.
- The daily finance Excel sheet: balance, payments released, expected receipts.
- Yesterday's approved payment list, and today's proposed payment sheet or known commitments (salaries/WPS, guarantees, urgent advances).
Mask account numbers to the last 4 digits. Do not repeat IBANs or beneficiary bank details in the output.

## Steps
1. **Balances.** Per account, set bank closing vs ePromis closing vs Excel closing side by side, each with its source and date. Do not compare balances of different dates or currencies.
2. **Match lines.** Match on amount and reference first, then on amount and date. State the date tolerance you used. One-to-many matches need a reference that links them. Classify each unmatched item:
   - **Timing.** Released in ePromis but not yet on the bank (outstanding transfer), or a receipt in transit. No entry needed if it clears in the normal cycle.
   - **Needs booking / adjustment, to confirm.** Client receipt not booked, bank charge or interest, a returned payment still booked as paid, or a duplicate posting.
   - **Investigate.** Unidentified credit or debit, amount mismatch, an item older than the normal cycle, or a repeated difference.
3. **Reconcile.** Bank closing ± listed items should equal ePromis closing; do the same check for Excel. Show any residual as **"Unexplained difference: AED x"**. Never plug it, net it into another item, or call the account reconciled.
4. **Yesterday's payments.** For each payment on the approved list, report one of: Confirmed (bank debit and reference cited), Not on statement (check portal release status), Returned (narrative cited), or Amount differs.
5. **Today's cash.** Per account and entity: available = bank closing balance as reported (Calculation). Commitments = today's payment sheet + other cited commitments + yesterday's unconfirmed payments that may still debit. Headroom = available − commitments. Unidentified credits are flagged rather than counted as freely available. This is information for prioritisation, not a release decision.
6. **Client receipts.** List credits that look like client receipts. Give the probable project/IPC only where the narrative or reference supports it; otherwise say "to identify".

## Output
Use [cash-reconciliation.csv](assets/cash-reconciliation.csv) for the item list when a file is wanted.
```
CASH POSITION · <entity> · as of <date/time> · sources: <files>
BALANCES   | Account (••last4) | Ccy | Bank | ePromis | Excel | Bank–ePromis | Bank–Excel |
UNMATCHED  | # | Account | Date | Amount | Ref/narrative | Side (bank/ePromis/Excel) | Category | Suggested action (to confirm) |
RECONCILIATION  Bank closing ± items = <x> vs ePromis <y> → Unexplained difference: <z or 0>
YESTERDAY'S PAYMENTS  | Payment ref | Payee | Amount | Status | Evidence |
TODAY  Available <x> · Commitments <y> (listed) · Headroom <x−y> · Items needing a decision
CASH NOTE (draft, ≤6 lines, for Finance Manager / CFO)
```

## Project context and evidence
Read [project-context.md](references/project-context.md) before interpreting evidence or handing results to another skill. Use the supplied project configuration; the bundled example is not live data. Cite each material finding to a file and page, row, activity or message reference.

## Interpretation limits
Suggested entries are for the accountant to review. This skill does not post journals, reverse payments, re-release transfers or approve the payment sheet. A partial statement (missing pages or accounts) means partial coverage; name what was not supplied. Payment prioritisation goes through the `ar-ap-aging-review` skill and the CFO. See [practice.md](references/practice.md).
