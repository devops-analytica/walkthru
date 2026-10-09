#!/usr/bin/env python3
"""Deterministic checks on normalized evidence JSON; no document extraction or approvals.

Usage: python operation_checks.py invoice|deadlines|variance input.json --out result.json
Amounts use Decimal, with invoice line/VAT rounding to 0.01 unless supplied otherwise.
Do not treat this helper as evidence that omitted documents were checked.
"""
import argparse
import json
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


def number(value):
    try:
        n = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f'Invalid number: {value!r}') from exc
    if not n.is_finite():
        raise ValueError('Numbers must be finite')
    return n


def money(n):
    return number(n).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def progress_variance(data):
    planned, actual = number(data['planned']), number(data['actual'])
    if not 0 <= planned <= 100 or not 0 <= actual <= 100:
        raise ValueError('Progress must be percentages between 0 and 100')
    delta = actual - planned
    return {'variance_percentage_points': str(delta), 'position': 'behind' if delta < 0 else 'ahead' if delta > 0 else 'on plan',
            'formula': 'actual - planned', 'source': data.get('source', 'not supplied')}


def deadline_watch(data):
    as_of = date.fromisoformat(data['as_of'])
    rows = []
    for item in data['items']:
        kind = item.get('date_kind')
        if kind not in {'expiry', 'task_due', 'review_due'}:
            raise ValueError('Every item needs date_kind: expiry, task_due or review_due')
        status = item.get('status', '').strip().lower()
        terminal = {'cancelled', 'closed'} if kind == 'expiry' else {'complete', 'completed', 'closed', 'cancelled', 'approved'}
        if status in terminal:
            continue
        raw = item.get('date')
        days = (date.fromisoformat(raw) - as_of).days if raw else None
        bucket = 'missing date' if days is None else 'overdue' if days < 0 else 'due in 0–7 days' if days <= 7 else 'due in 8–14 days' if days <= 14 else 'due in 15–30 days' if days <= 30 else 'later'
        lead = item.get('lead_time_days')
        if lead is not None and (not isinstance(lead, int) or lead < 0):
            raise ValueError('Lead time must be a non-negative integer')
        rows.append({**item, 'days_left': days, 'bucket': bucket,
                     'lead_time_warning': days is not None and lead is not None and days < lead,
                     'deadline_basis': item.get('deadline_basis', 'supplied date; contractual basis not confirmed')})
    return {'as_of': str(as_of), 'items': sorted(rows, key=lambda x: (x['days_left'] is None, x['days_left'] or 0))}


def invoice_check(data):
    checks, lines = [], []
    def record(name, state, detail, source=None):
        checks.append({'check': name, 'state': state, 'detail': detail, 'source': source or 'not supplied'})
    invoice, po = data['invoice'], data.get('po')
    if not po:
        record('PO', 'Not checked', 'Purchase order missing')
        return {'recommendation': 'Incomplete review — obtain PO', 'checks': checks, 'lines': [], 'supported_excl_vat': None}
    record('PO', 'Pass' if invoice.get('po_number') == po.get('number') and po.get('number') else 'Exception', 'Compare PO identifiers', po.get('source'))
    for key in ['vendor_id', 'project_id', 'currency']:
        if not invoice.get(key) or not po.get(key):
            record(key, 'Not checked', 'Identifiers missing')
        else:
            record(key, 'Pass' if invoice[key] == po[key] else 'Exception', 'Exact identifier comparison; aliases need documented confirmation', po.get('source'))
    history = data.get('history')
    history_complete = data.get('history_complete') is True and isinstance(history, list)
    delivery_complete = data.get('delivery_complete') is True
    if not history_complete:
        record('Duplicates and cumulative billing', 'Not checked', 'Complete invoice history not supplied')
    else:
        matching = [h for h in history if h.get('vendor_id') == invoice.get('vendor_id') and str(h.get('number', '')).strip().casefold() == str(invoice.get('number', '')).strip().casefold() and h.get('number')]
        suspect = [h for h in history if h.get('vendor_id') == invoice.get('vendor_id') and h.get('date') == invoice.get('date') and h.get('total') is not None and money(h['total']) == money(invoice['total'])]
        record('Duplicates', 'Exception' if matching or suspect else 'Pass', 'Same vendor/invoice number' if matching else 'Possible duplicate: amount/date match; investigate' if suspect else 'None found in supplied complete history', data.get('history_source'))
    po_lines = {str(x['id']): x for x in po['lines']}
    if len(po_lines) != len(po['lines']):
        raise ValueError('Duplicate PO line IDs')
    if len({str(x['id']) for x in invoice['lines']}) != len(invoice['lines']):
        raise ValueError('Duplicate invoice line IDs; normalize allocations before review')
    claimed_sum, supported_sum = Decimal(0), Decimal(0)
    support_known = all(c["state"] == "Pass" for c in checks if c["check"] in {"PO", "vendor_id", "project_id", "currency"})
    for line in invoice['lines']:
        lid = str(line['id']); ordered = po_lines.get(lid)
        qty, rate, amount = number(line['qty']), number(line['rate']), money(line['amount'])
        if qty < 0 or rate < 0 or amount < 0:
            raise ValueError('Credit notes need a separate signed reconciliation; do not mix negative lines')
        claimed_sum += amount
        record('Arithmetic line ' + lid, 'Pass' if money(qty * rate) == amount else 'Exception', f'{qty} × {rate} vs {amount}', line.get('source'))
        if ordered is None:
            record('Match line ' + lid, 'Exception', 'Line not in PO', line.get('source')); support_known = False; continue
        for key in ['description', 'unit']:
            state = 'Not checked' if not line.get(key) or not ordered.get(key) else 'Pass' if line[key].strip().casefold() == ordered[key].strip().casefold() else 'Exception'
            record(key + ' line ' + lid, state, 'Match source description/unit; do not equate different specifications', line.get('source'))
            if state != 'Pass':
                support_known = False
        porate, poqty = number(ordered['rate']), number(ordered['qty'])
        if porate < 0 or poqty < 0:
            raise ValueError('PO quantity/rate cannot be negative')
        record('Rate line ' + lid, 'Pass' if rate == porate else 'Exception', f'Invoice {rate}; PO {porate}', ordered.get('source'))
        previous = line.get('previous_qty')
        delivered = line.get('delivered_qty')
        if not history_complete or previous is None:
            record('Cumulative quantity line ' + lid, 'Not checked', 'Previous booked quantity/history missing'); support_known = False
        elif not delivery_complete or delivered is None:
            record('Delivery line ' + lid, 'Not checked', 'Complete GRN/DN quantities missing'); support_known = False
        else:
            previous, delivered = number(previous), number(delivered)
            if previous < 0 or delivered < 0:
                raise ValueError('Previous and delivered quantities must be non-negative')
            allowed = max(Decimal(0), min(poqty, delivered) - previous)
            record('Quantity line ' + lid, 'Pass' if qty <= allowed else 'Exception', f'Invoice {qty}; unbilled supported quantity {allowed}', line.get('delivery_source'))
            supported = money(min(qty, allowed) * min(rate, porate))
            supported_sum += supported
            # One line reconciliation prevents quantity/rate exceptions being double counted.
            lines.append({'id': lid, 'claimed_excl_vat': str(amount), 'supported_excl_vat': str(supported),
                          'difference_excl_vat': str(amount - supported), 'source': line.get('source', 'not supplied')})
    record('Subtotal', 'Pass' if money(invoice['subtotal']) == money(claimed_sum) else 'Exception', 'Sum of invoiced line amounts', invoice.get('source'))
    tax_rate = data.get('tax_rate')
    if tax_rate is None:
        record('VAT', 'Not checked', 'Tax rate/treatment not supplied; no universal 5% assumption')
    else:
        tax_rate = number(tax_rate)
        if not 0 <= tax_rate <= 1:
            raise ValueError('Tax rate is a fraction between 0 and 1')
        expected = money(number(invoice['subtotal']) * tax_rate)
        record('VAT', 'Pass' if money(invoice['vat']) == expected else 'Exception', f'Expected VAT {expected}; supplied treatment must be confirmed', data.get('tax_source'))
    record('Total', 'Pass' if money(invoice['total']) == money(number(invoice['subtotal']) + number(invoice['vat'])) else 'Exception', 'Subtotal plus VAT', invoice.get('source'))
    if data.get('tax_invoice') is True:
        record('TRN', 'Pass' if invoice.get('supplier_trn') else 'Exception', 'Presence only; registration validity not verified', invoice.get('source'))
    else:
        record('TRN', 'Not applicable' if data.get('tax_invoice') is False else 'Not checked', 'Confirm invoice type')
    record('Deductions', 'Not applicable' if data.get('deductions_applicable') is False else 'Not checked', 'Applicable retention/advance/contra-charges require contract reconciliation')
    states = {c['state'] for c in checks}
    recommendation = 'Hold — resolve exceptions' if 'Exception' in states else 'Incomplete review — obtain missing evidence' if 'Not checked' in states else 'No exceptions in supplied evidence — manager review required'
    return {'recommendation': recommendation, 'checks': checks, 'lines': lines,
            'supported_excl_vat': str(money(supported_sum)) if support_known else None,
            'supported_incl_vat': str(money(supported_sum + money(supported_sum * tax_rate))) if support_known and tax_rate is not None else None,
            'source': invoice.get('source', 'not supplied'), 'scope': 'Material invoice comparison only; no certification, tax validation or ERP approval'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=['invoice', 'deadlines', 'variance'])
    parser.add_argument('input')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text())
        result = {'invoice': invoice_check, 'deadlines': deadline_watch, 'variance': progress_variance}[args.kind](payload)
        output = Path(args.out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2) + '\n')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f'Invalid evidence/input/output: {exc}\n')


if __name__ == '__main__':
    main()
