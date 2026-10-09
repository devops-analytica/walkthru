---
description: Pre-check a supplier invoice or payment request against the PO/LPO, GRNs and billing history before manager review.
argument-hint: [attach invoice + PO/LPO + GRN/delivery notes + prior billing if any]
---
Invoke the `invoice-po-check` skill on: $ARGUMENTS

Normalize the evidence to JSON, run `python3 scripts/operation_checks.py invoice ...` from the skill folder, and return the checks table, exceptions, classification (Hold / Incomplete review / No exceptions in supplied evidence) and draft queries. This does not approve, book or pay anything.
