# Synthetic practice requests

These are fictional records, not live WalkThru data. Expected outcomes are reviewer criteria, not evidence of a model test pass.

## Case 1

Request: Batch of 3 contract renewals; rule supplied: passport at least 6 months valid at 09-Oct-2026 (example figure); no fee table.

Input: W1 passport expires 2027-03-01, all documents present. W2 passport expires 2027-12-01, medical not reported. W3 passport expires 2027-01-15, photo missing.

Expected: W1 fails the rule (about 4.7 months), so Ready = No. W2 Ready = No, medical "Not reported - to confirm". W3 Ready = No, photo missing. Fees "n/a". One draft message per worker; nothing submitted.

## Case 2

Request: Same batch, no passport rule supplied.

Expected: Passport check "To confirm" for all, so no worker Ready = Yes; asks for the rule; order proposed by expiry only, labelled provisional.
