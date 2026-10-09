# Synthetic practice requests

These are fictional records, not live WalkThru project data. Expected outcomes are reviewer criteria, not evidence of a model test pass.

## Case 1

Request: Review the normalized material invoice in assets/invoice.json.

Input: Synthetic PO 100 pcs at 10.00; accepted delivered 80, previously booked 20. Current invoice 70 at 12.00, subtotal 840.00, tax 42.00, total 882.00; supplied tax fraction .05.

Expected: Remaining support 60 pcs at 10 = 600.00 excl tax; discrepancy 240.00 excl tax, not separately added quantity/rate differences. Helper recommendation Hold. No payment approved.

## Case 2

Request: Review same invoice but omit previous-billing/delivery completeness evidence.

Input: history_complete false, delivery_complete false, previous_qty null, delivered_qty null. All other values as sample.

Expected: Required cumulative/delivery checks Not checked; final supported total unknown. Cannot return clean review or assume zero history. Existing rate exception still reported.
