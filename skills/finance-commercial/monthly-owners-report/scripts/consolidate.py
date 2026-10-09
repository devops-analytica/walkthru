#!/usr/bin/env python3
"""Owners' report arithmetic: per-project figures and entity totals from normalized JSON.

Usage: python3 consolidate.py input.json --out result.json [--csv projects.csv]
Missing figures stay n/a and make totals partial; nothing is estimated. Totals are kept per
(entity, currency); no FX conversion and no intercompany elimination. Decimal arithmetic,
quantized to 0.01 ROUND_HALF_UP at output only. See references/consolidate-input.md.
"""
import argparse
import csv
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

FIELDS = ['original_contract', 'approved_variations', 'pending_variations', 'certified_to_date',
          'invoiced_to_date', 'collected_to_date', 'ar_aging_balance', 'cost_to_date',
          'unbooked_cost', 'committed_cost']
DERIVED = ['revised_contract', 'receivable_calc', 'receivable_vs_aging', 'margin_to_date']
SUMMED = FIELDS + DERIVED
NA = 'n/a (source not supplied)'


def amount(field, project_id):
    """Return (Decimal or None, source). A figure without a source is rejected."""
    if field is None:
        return None, None
    if not isinstance(field, dict) or 'value' not in field:
        raise ValueError(f'{project_id}: figures must be {{"value": ..., "source": ...}} or null')
    raw, source = field['value'], field.get('source')
    if raw is None:
        return None, None
    if isinstance(raw, bool) or not source:
        raise ValueError(f'{project_id}: every supplied figure needs a numeric value and a source')
    try:
        n = Decimal(str(raw).replace(',', ''))
    except InvalidOperation as exc:
        raise ValueError(f'{project_id}: invalid number {raw!r}') from exc
    if not n.is_finite():
        raise ValueError(f'{project_id}: numbers must be finite')
    return n, source


def sub(a, b):
    return None if a is None or b is None else a - b


def fmt(n):
    return NA if n is None else str(n.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def pct(num, den):
    if num is None or den is None or den == 0:
        return None
    return (num / den * 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def project_row(p):
    pid = p.get('id')
    if not pid:
        raise ValueError('every project needs an id')
    vals, sources = {}, {}
    for f in FIELDS:
        vals[f], sources[f] = amount(p.get(f), pid)
    tender, sources['tender_margin_pct'] = amount(p.get('tender_margin_pct'), pid)
    vals['revised_contract'] = (None if vals['original_contract'] is None or vals['approved_variations'] is None
                                else vals['original_contract'] + vals['approved_variations'])
    vals['receivable_calc'] = sub(vals['invoiced_to_date'], vals['collected_to_date'])
    vals['receivable_vs_aging'] = sub(vals['receivable_calc'], vals['ar_aging_balance'])
    vals['margin_to_date'] = sub(vals['certified_to_date'], vals['cost_to_date'])
    margin_pct = pct(vals['margin_to_date'], vals['certified_to_date'])
    return {'id': pid, 'name': p.get('name', ''), 'entity': p.get('entity'), 'currency': p.get('currency'),
            'intercompany': bool(p.get('intercompany')), 'values': vals,
            'margin_pct': margin_pct, 'tender_margin_pct': tender,
            'margin_vs_tender_pp': None if margin_pct is None or tender is None else margin_pct - tender,
            'sources': sources}


def consolidate(data):
    projects = data.get('projects')
    if not isinstance(projects, list) or not projects:
        raise ValueError('input needs a non-empty "projects" list')
    rows = [project_row(p) for p in projects]
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('duplicate project id')
    unresolved, groups = [], {}
    for r in rows:
        if not r['entity'] or not r['currency']:
            unresolved.append(f"{r['id']}: entity or currency not supplied; excluded from all totals")
            continue
        groups.setdefault((r['entity'], r['currency']), []).append(r)
        unresolved += [f"{r['id']}: {f} {NA}" for f in FIELDS if r['values'][f] is None]
        if r['intercompany']:
            unresolved.append(f"{r['id']}: intercompany; elimination not performed")
    totals = []
    for (entity, currency), members in sorted(groups.items()):
        cols = {}
        for f in SUMMED:
            missing = [m['id'] for m in members if m['values'][f] is None]
            supplied = sum((m['values'][f] for m in members if m['values'][f] is not None), Decimal(0))
            cols[f] = {'total': None if missing else supplied, 'supplied_sum': supplied, 'missing': missing}
        complete = cols['margin_to_date']['total'] is not None and cols['certified_to_date']['total'] is not None
        totals.append({'entity': entity, 'currency': currency, 'projects': [m['id'] for m in members], 'columns': cols,
                       'margin_pct': pct(cols['margin_to_date']['total'], cols['certified_to_date']['total']) if complete else None})
    currencies = {r['currency'] for r in rows if r['currency']}
    excluded = [r['id'] for r in rows if not r['entity'] or not r['currency']]
    group_note = ('group total withheld: ' + ('; '.join(filter(None, [
        f"unmapped projects {excluded}" if excluded else '',
        f"multiple currencies {sorted(currencies)} and no confirmed FX basis" if len(currencies) > 1 else '']))))
    group_ok = not excluded and len(currencies) == 1
    return rows, totals, unresolved, group_ok, group_note


def render(rows, totals, unresolved, group_ok, group_note, data):
    out_rows = [{'id': r['id'], 'name': r['name'], 'entity': r['entity'] or NA, 'currency': r['currency'] or NA,
                 **{f: fmt(r['values'][f]) for f in SUMMED},
                 'margin_pct': fmt(r['margin_pct']), 'tender_margin_pct': fmt(r['tender_margin_pct']),
                 'margin_vs_tender_pp': fmt(r['margin_vs_tender_pp']),
                 'sources': {k: v or NA for k, v in r['sources'].items()}} for r in rows]
    out_totals = [{'entity': t['entity'], 'currency': t['currency'], 'projects': t['projects'],
                   'margin_pct': fmt(t['margin_pct']),
                   **{f: (fmt(c['total']) if c['total'] is not None else NA if len(c['missing']) == len(t['projects'])
                          else f"partial: {fmt(c['supplied_sum'])} excl. {', '.join(c['missing'])}")
                      for f, c in t['columns'].items()}} for t in totals]
    return {'period': data.get('period', NA), 'as_of': data.get('as_of', NA), 'rounding': '0.01 ROUND_HALF_UP at output',
            'formulas': {'revised_contract': 'original_contract + approved_variations (pending excluded)',
                         'receivable_calc': 'invoiced_to_date - collected_to_date',
                         'receivable_vs_aging': 'receivable_calc - ar_aging_balance',
                         'margin_to_date': 'certified_to_date - cost_to_date (unbooked_cost shown separately)',
                         'margin_pct': 'margin_to_date / certified_to_date * 100'},
            'projects': out_rows, 'entity_totals': out_totals,
            'group_total': 'single currency, all projects mapped: sum entity totals' if group_ok else group_note,
            'unresolved': unresolved}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input')
    ap.add_argument('--out', required=True)
    ap.add_argument('--csv')
    a = ap.parse_args()
    src = Path(a.input).resolve()
    if src in {Path(a.out).resolve(), Path(a.csv).resolve() if a.csv else None}:
        sys.exit('refusing to overwrite the input file')
    try:
        data = json.loads(src.read_text(encoding='utf-8'))
        result = render(*consolidate(data), data)
    except (OSError, ValueError, AttributeError, TypeError) as exc:
        sys.exit(f'error: {exc}')
    Path(a.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    if a.csv:
        cols = ['id', 'name', 'entity', 'currency'] + SUMMED + ['margin_pct', 'tender_margin_pct', 'margin_vs_tender_pp']
        with open(a.csv, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(cols)
            for r in result['projects']:
                w.writerow([cell(r[c]) for c in cols])


def cell(v):
    """Keep numbers (including negatives) numeric; stop other text becoming a spreadsheet formula."""
    try:
        Decimal(v)
        return v
    except (InvalidOperation, TypeError, ValueError):
        return "'" + v if isinstance(v, str) and v[:1] in '=+-@' else v


if __name__ == '__main__':
    main()
