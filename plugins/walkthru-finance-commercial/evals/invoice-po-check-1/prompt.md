---
max_turns: 10
runs: 1
allowed_tools: [Read, Glob, Grep, Skill]
tags: [invoice, invoice-po-check]
---

Review the normalized material invoice in assets/invoice.json.

Synthetic PO 100 pcs at 10.00; accepted delivered 80, previously booked 20. Current invoice 70 at 12.00, subtotal 840.00, tax 42.00, total 882.00; supplied tax fraction .05.
