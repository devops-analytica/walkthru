# Synthetic practice requests

Adapted in structure from the upstream finance plugin skill `reconciliation`: the bank reconciliation layout and the timing / adjustment / investigate categories (Apache License 2.0; see `references/upstream-plugins/LICENSE-financial-services-plugins` in the toolkit repository). Rewritten for WalkThru's daily bank check. These are fictional records, not live WalkThru data. Expected outcomes are reviewer criteria, not evidence of a model test pass.

## Case 1: returned payment, unbooked receipt, duplicate posting

Request: Morning bank check for AUH Bank A ••4410, AED, statement 08-Oct-2026.

Input:
- Bank: opening 3,000,000.00, closing 3,671,450.00. Lines:
  - receipt 850,000 "IPC-11 P-303";
  - PAY-5501 −120,000;
  - PAY-5502 −45,500, returned +45,500;
  - charges −1,050;
  - PAY-5503 −60,000;
  - cash deposit +2,500, reference only.
- ePromis: closing 2,504,500.00. PAY-5503 is booked twice, and PAY-5504 −210,000 is booked.
- Excel: closing 2,566,500.00.
- Today's sheet: 400,000 + 150,000 + WPS 1,900,000.

Expected:
- Bank − ePromis = 1,166,950, fully explained by:
  - +850,000 receipt to book;
  - +45,500 returned payment to reverse;
  - −1,050 charges;
  - +60,000 duplicate posting;
  - +210,000 PAY-5504 not on the statement;
  - +2,500 to identify.
- Excel − ePromis = 62,000. The duplicate explains 60,000, so **unexplained 2,000** is reported, not plugged.
- Commitments 2,450,000. Headroom 1,221,450, or 1,011,450 if PAY-5504 may still debit; the basis is stated.

## Case 2: partial evidence

Request: Same account, but only the bank statement and today's payment sheet are supplied.

Expected:
- Balances and statement lines are listed. The ePromis and Excel comparisons are marked Not checked (source not supplied).
- No item is called "unbooked" without the ledger. Credits are "to match when ePromis export is supplied".
- Yesterday's payments cannot be confirmed against an approved list. Ask for the list.
- Headroom is shown from the bank balance, with that limitation stated. The account is not called reconciled.
