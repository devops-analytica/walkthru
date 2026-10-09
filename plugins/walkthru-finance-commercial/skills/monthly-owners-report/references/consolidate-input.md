# consolidate.py input

Normalize the supplied exports to JSON first and check the extraction against the source. The helper reads JSON only. Run `python3 scripts/consolidate.py input.json --out result.json [--csv projects.csv]`. It refuses to overwrite the input, and it exits non-zero on bad input: a non-numeric value, a figure without a source, a missing or duplicate project id.

```json
{
  "period": "2026-09",
  "as_of": "2026-09-30",
  "projects": [
    {
      "id": "P-101", "name": "Villa cluster", "entity": "AUH", "currency": "AED", "intercompany": false,
      "original_contract":   {"value": "40000000", "source": "Projects tab row 4"},
      "approved_variations": {"value": "2000000",  "source": "SharePoint VO log V-01..V-03 (approved)"},
      "pending_variations":  {"value": "500000",   "source": "SharePoint VO log V-04 (pending)"},
      "certified_to_date":   {"value": "25000000", "source": "IPC-14 certified"},
      "invoiced_to_date":    {"value": "24000000", "source": "AR list row 12"},
      "collected_to_date":   {"value": "20000000", "source": "AR list row 12"},
      "ar_aging_balance":    {"value": "4000000",  "source": "aging.xlsx total P-101"},
      "cost_to_date":        {"value": "21000000", "source": "ePromis cost export 30-Sep"},
      "unbooked_cost":       {"value": "300000",   "source": "CFO adjustment note"},
      "committed_cost":      {"value": "9000000",  "source": "ePromis open LPO/subcontract report"},
      "tender_margin_pct":   {"value": "14",       "source": "tender summary"}
    }
  ]
}
```

Rules:
- Every figure is `{"value", "source"}`, or `null` when it was not supplied. Use `null`, never 0, for missing figures. Use 0 only when a source says zero, and cite it.
- `entity` and `currency` come only from the supplied entity map. If either is missing, use `null`. The project is then excluded from all totals and listed as unresolved.
- Output: per-project values and derived figures (revised contract, receivable calc, receivable vs aging, margin to date, margin %, margin vs tender in pp). Entity totals are per (entity, currency). A column with any missing project shows `partial: <sum> excl. <ids>`. The group total is withheld if any project is unmapped or more than one currency is present. The output also gives an unresolved list.
- The helper does no FX conversion and no intercompany elimination; intercompany projects are flagged. Cash position is reported per bank and entity from the bank evidence, outside the helper.
- CSV text cells starting with `=`, `+`, `-` or `@` are prefixed with `'`. Numeric values, including negatives, stay numeric.
