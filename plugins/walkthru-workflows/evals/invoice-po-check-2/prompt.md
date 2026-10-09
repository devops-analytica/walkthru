---
max_turns: 10
timeout_seconds: 600
runs: 1
allowed_tools: [Read, Glob, Grep, Skill]
tags: [invoice, invoice-po-check]
---

Review same invoice but omit previous-billing/delivery completeness evidence.

history_complete false, delivery_complete false, previous_qty null, delivered_qty null. All other values as sample.
