# Synthetic practice requests

Adapted in structure from the upstream finance plugin skill `reconciliation`: aging buckets with escalation by age, and the "investigate / escalate" handling of open items (Apache License 2.0; see `references/upstream-plugins/LICENSE-financial-services-plugins` in the toolkit repository). Rewritten for WalkThru receivables, payables and retention. These are fictional records, not live WalkThru data. Expected outcomes are reviewer criteria, not evidence of a model test pass.

## Case 1: retention, dispute, uncertified IPA, supplier chaser

Request: Weekly aging review, AUH, AED, as of 09-Oct-2026.

Input:
- AR:
  - TI-2051 due 24-Sep, 1,200,000;
  - TI-1990 due 01-Jul, 650,000;
  - TI-2033 due 10-Aug, 900,000;
  - TI-2060 due 30-Oct, 1,500,000;
  - TI-1801 due 15-May, 300,000, disputed;
  - retention 2,100,000, release 31-Mar-2027;
  - IPA-8, 1,100,000, not certified.
- AP:
  - Gulf Steel, 400,000, due 20-Sep, approved;
  - Al Noor, 150,000, due 25-Aug, approved;
  - Cool Breeze, 210,000, due 20-Oct;
  - Readymix, 85,000, on hold;
  - Desert Plant, 60,000, awaiting approval.
- Gulf Steel asks for confirmation of payment on Thursday.

Expected:
- AR buckets: current 1,500,000; 1–30 1,200,000 (15 days); 31–60 900,000 (60 days); 91–120 650,000 (100 days); 120+ 300,000 (147 days, disputed).
- Retention and IPA-8 are shown separately.
- AP priority input for the CFO: Gulf Steel, then Al Noor. Readymix and Desert Plant are not payable until resolved.
- The Gulf Steel reply commits to no date or amount.

## Case 2: no due dates in the export

Request: Same AR list, but with invoice dates only and no credit terms.

Expected:
- Bucket by invoice age, and state that this is not days past due.
- Ask for the credit terms per client contract.
- Draft no collection email that calls an item "overdue" until its due date is confirmed.
