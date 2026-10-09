import copy
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'maintenance/lib' / (name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


xer, ops = load('xer_check'), load('operation_checks')


def tables(float_hours='8', project='P1'):
    return {'PROJECT': [{'proj_id': 'P1', 'proj_short_name': 'First', 'last_recalc_date': '2026-10-01'},
                        {'proj_id': 'P2', 'proj_short_name': 'Second', 'last_recalc_date': '2026-10-20'}],
            'CALENDAR': [{'clndr_id': 'C1', 'day_hr_cnt': '8'}],
            'TASK': [{'task_id': '1', 'proj_id': project, 'clndr_id': 'C1', 'task_code': 'A1', 'task_name': 'Work',
                      'task_type': 'TT_Task', 'status_code': 'TK_NotStart', 'total_float_hr_cnt': float_hours,
                      'target_drtn_hr_cnt': '400', 'remain_drtn_hr_cnt': '8',
                      'early_start_date': '2026-10-15', 'early_end_date': '2026-10-16', 'target_end_date': '2026-10-16'}]}


def flags(t, **kwargs):
    activities, projects, warnings = xer.build_activities(t)
    return activities, [n for n, a in xer.check(t, activities, projects, **kwargs)], warnings


def invoice():
    return {'invoice': {'number': 'GB-2231', 'po_number': 'LPO-4410', 'vendor_id': 'V1', 'project_id': 'VS-02',
                        'currency': 'AED', 'date': '2026-10-05', 'supplier_trn': '100234567800003',
                        'subtotal': '30300', 'vat': '1515', 'total': '31815', 'source': 'invoice.txt lines 1–6',
                        'lines': [{'id': '1', 'description': 'Solid block', 'unit': 'nos', 'qty': '6000', 'rate': '3.25', 'amount': '19500', 'previous_qty': '0', 'delivered_qty': '6000', 'source': 'invoice line 1', 'delivery_source': 'DN-881'},
                                  {'id': '2', 'description': 'Hollow block', 'unit': 'nos', 'qty': '4500', 'rate': '2.40', 'amount': '10800', 'previous_qty': '0', 'delivered_qty': '4000', 'source': 'invoice line 2', 'delivery_source': 'DN-902'}]},
            'po': {'number': 'LPO-4410', 'vendor_id': 'V1', 'project_id': 'VS-02', 'currency': 'AED', 'source': 'LPO-4410',
                   'lines': [{'id': '1', 'description': 'Solid block', 'unit': 'nos', 'qty': '6000', 'rate': '3.10'},
                             {'id': '2', 'description': 'Hollow block', 'unit': 'nos', 'qty': '4000', 'rate': '2.40'}]},
            'history': [], 'history_complete': True, 'history_source': 'Full PO ledger: zero previous invoices',
            'delivery_complete': True, 'tax_rate': '.05', 'tax_source': 'Confirmed synthetic tax fixture', 'tax_invoice': True,
            'deductions_applicable': False}


class ScheduleTests(unittest.TestCase):
    def test_positive_fraction_is_not_zero(self):
        a, f, _ = flags(tables('.16'))
        self.assertEqual(a[0]['total_float_d'], .02)
        self.assertTrue(any(n.startswith('Near-critical') for n in f))
        self.assertFalse(any(n.startswith('Float at/below') for n in f))

    def test_negative_fraction_is_preserved(self):
        _, f, _ = flags(tables('-.16')); self.assertIn('Negative float', f)

    def test_second_project_uses_own_date(self):
        _, f, _ = flags(tables(project='P2'))
        self.assertIn('Should have started (start before project data date)', f)
        self.assertNotIn('Starts in next 21 calendar days', f)

    def test_both_constraints(self):
        t = tables(); t['TASK'][0].update(cstr_type='CS_MSO', cstr_type2='CS_MEO')
        _, f, _ = flags(t); self.assertEqual(len([n for n in f if n.startswith('Hard constraint')]), 2)

    def test_secondary_only(self):
        t = tables(); t['TASK'][0]['cstr_type2'] = 'CS_MEO'
        _, f, _ = flags(t); self.assertIn('Hard constraint (secondary: CS_MEO)', f)

    def test_calendar_conversion(self):
        t = tables('10'); t['CALENDAR'][0]['day_hr_cnt'] = '10'
        a, _, _ = flags(t); self.assertEqual(a[0]['total_float_d'], 1)

    def test_missing_calendar_warns(self):
        t = tables(); t['CALENDAR'] = []
        a, _, w = flags(t); self.assertTrue(a[0]['calendar_assumed']); self.assertTrue(w)

    def test_unknown_project_fails(self):
        with self.assertRaises(ValueError): flags(tables(project='UNKNOWN'))

    def test_missing_date_disables_date_checks(self):
        t = tables(); t['PROJECT'][0]['last_recalc_date'] = ''
        _, f, w = flags(t); self.assertFalse(any('Starts in next' in n for n in f)); self.assertTrue(w)

    def test_nonfinite_float_fails(self):
        for value in ['nan', 'inf', 'bad']:
            with self.subTest(value=value), self.assertRaises(ValueError): flags(tables(value))

    def test_original_duration_is_checked(self):
        _, f, _ = flags(tables()); self.assertIn('Long original duration (> 44d)', f)

    def test_lookahead_includes_in_progress_finishes(self):
        t = tables(); t['TASK'][0].update(status_code='TK_Active', act_start_date='2026-09-29')
        _, f, _ = flags(t); self.assertIn('Finishes in next 21 calendar days', f)

    def test_threshold_is_configurable(self):
        _, f, _ = flags(tables('8'), critical_days=2)
        self.assertIn('Float at/below critical threshold (2d)', f)

    def test_invalid_threshold_fails(self):
        with self.assertRaises(ValueError): flags(tables(), critical_days=20, near_days=10)

    def test_csv_formula_is_text(self):
        self.assertEqual(xer.csv_value('=HYPERLINK("bad")'), '\'=HYPERLINK("bad")')

    def test_malformed_xer_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'bad.xer'; p.write_text('%T\n')
            with self.assertRaises(ValueError): xer.parse_xer(p)

    def test_cli_multi_project_output_and_input_unchanged(self):
        t = tables(project='P2')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'test.xer'; text = 'ERMHDR\t26.0\n'
            for table, rows in t.items():
                keys = list(rows[0]); text += '%T\t' + table + '\n%F\t' + '\t'.join(keys) + '\n'
                text += ''.join('%R\t' + '\t'.join(row.get(k, '') for k in keys) + '\n' for row in rows)
            p.write_text(text)
            run = subprocess.run([sys.executable, str(ROOT / 'maintenance/lib/xer_check.py'), str(p), '--out-dir', str(Path(d) / 'out')], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr); self.assertEqual(p.read_text(), text)
            with (Path(d) / 'out/activities.csv').open() as f: row = next(csv.DictReader(f))
            self.assertEqual(row['project_id'], 'P2'); self.assertTrue(row['data_date'].startswith('2026-10-20'))
            self.assertIn('Not an ordered critical path', run.stdout)


class InvoiceTests(unittest.TestCase):
    def test_fixture_supported_amount(self):
        r = ops.invoice_check(invoice()); self.assertEqual(r['supported_excl_vat'], '28200.00'); self.assertEqual(r['supported_incl_vat'], '29610.00')
        self.assertEqual(sum(ops.number(x['difference_excl_vat']) for x in r['lines']), ops.number('2100'))

    def test_missing_history_is_not_pass(self):
        t = invoice(); t.pop('history'); r = ops.invoice_check(t)
        self.assertIsNone(r['supported_excl_vat']); self.assertTrue(any(x['state'] == 'Not checked' for x in r['checks']))

    def test_missing_delivery_is_not_pass(self):
        t = invoice(); t['delivery_complete'] = False; self.assertIsNone(ops.invoice_check(t)['supported_excl_vat'])

    def test_rate_quantity_overlap_counted_once(self):
        t = invoice(); t['invoice']['lines'][1].update(rate='2.50', amount='11250'); t['invoice'].update(subtotal='30750', vat='1537.50', total='32287.50')
        r = ops.invoice_check(t); self.assertEqual(r['lines'][1]['difference_excl_vat'], '1650.00')

    def test_previous_billing_reduces_available_delivery(self):
        t = invoice(); t['invoice']['lines'][1]['previous_qty'] = '3500'
        r = ops.invoice_check(t); self.assertEqual(r['lines'][1]['supported_excl_vat'], '1200.00')

    def test_duplicate_requires_review(self):
        t = invoice(); t['history'] = [{'vendor_id': 'V1', 'number': 'GB-2231', 'date': '2026-10-05', 'total': '31815'}]
        r = ops.invoice_check(t); self.assertEqual(next(x for x in r['checks'] if x['check'] == 'Duplicates')['state'], 'Exception')

    def test_tax_rate_not_assumed(self):
        t = invoice(); t.pop('tax_rate'); r = ops.invoice_check(t)
        self.assertEqual(next(x for x in r['checks'] if x['check'] == 'VAT')['state'], 'Not checked'); self.assertIsNone(r['supported_incl_vat'])

    def test_zero_rated_tax(self):
        t = invoice(); t['tax_rate'] = '0'; t['invoice'].update(vat='0', total='30300')
        r = ops.invoice_check(t); self.assertEqual(next(x for x in r['checks'] if x['check'] == 'VAT')['state'], 'Pass')

    def test_po_missing(self):
        t = invoice(); t.pop('po'); self.assertIsNone(ops.invoice_check(t)['supported_excl_vat'])

    def test_wrong_vendor_has_no_supported_total(self):
        t = invoice(); t['invoice']['vendor_id'] = 'V2'
        self.assertIsNone(ops.invoice_check(t)['supported_excl_vat'])

    def test_wrong_specification_has_no_supported_total(self):
        t = invoice(); t['invoice']['lines'][0]['description'] = 'Different material'
        self.assertIsNone(ops.invoice_check(t)['supported_excl_vat'])

    def test_duplicate_line_allocations_rejected(self):
        t = invoice(); t['invoice']['lines'].append(copy.deepcopy(t['invoice']['lines'][0]))
        with self.assertRaises(ValueError): ops.invoice_check(t)

    def test_decimal_arithmetic(self):
        self.assertEqual(ops.money(ops.number('.1') * ops.number('3')), ops.number('.30'))


class DateAndVarianceTests(unittest.TestCase):
    def test_behind_variance(self):
        r = ops.progress_variance({'planned':60, 'actual':55}); self.assertEqual(r['variance_percentage_points'], '-5'); self.assertEqual(r['position'], 'behind')

    def test_ahead_variance(self):
        self.assertEqual(ops.progress_variance({'planned':60, 'actual':65})['position'], 'ahead')

    def test_progress_out_of_range(self):
        with self.assertRaises(ValueError): ops.progress_variance({'planned':60, 'actual':105})

    def test_approved_and_renewed_expiries_remain(self):
        data = {'as_of':'2026-10-08', 'items':[{'id':'A', 'date':'2026-10-10', 'date_kind':'expiry', 'status':s} for s in ['Approved','Renewed','Issued']]}
        self.assertEqual(len(ops.deadline_watch(data)['items']), 3)

    def test_approved_task_is_closed(self):
        data = {'as_of':'2026-10-08', 'items':[{'date':'2026-10-10', 'date_kind':'task_due', 'status':'Approved'}]}
        self.assertEqual(ops.deadline_watch(data)['items'], [])

    def test_deadline_boundaries(self):
        dates = ['2026-10-07','2026-10-08','2026-10-15','2026-10-16','2026-10-22','2026-10-23','2026-11-07','2026-11-08',None]
        r = ops.deadline_watch({'as_of':'2026-10-08','items':[{'date':d,'date_kind':'expiry'} for d in dates]})
        self.assertEqual([x['bucket'] for x in r['items']], ['overdue','due in 0–7 days','due in 0–7 days','due in 8–14 days','due in 8–14 days','due in 15–30 days','due in 15–30 days','later','missing date'])

    def test_invalid_date_rejected(self):
        with self.assertRaises(ValueError): ops.deadline_watch({'as_of':'2026-10-08','items':[{'date':'10/11/26','date_kind':'expiry'}]})

    def test_date_kind_required(self):
        with self.assertRaises(ValueError): ops.deadline_watch({'as_of':'2026-10-08','items':[{'date':'2026-10-10'}]})

    def test_lead_time_warning(self):
        r = ops.deadline_watch({'as_of':'2026-10-08','items':[{'date':'2026-10-12','date_kind':'expiry','lead_time_days':10}]})
        self.assertTrue(r['items'][0]['lead_time_warning'])


if __name__ == '__main__':
    unittest.main()
