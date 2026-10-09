#!/usr/bin/env python3
"""Offline packaging/structural validation and deterministic invoice regressions."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[2]
def invoice_tests():
    path = ROOT / 'skills/finance-commercial/invoice-po-check/scripts/operation_checks.py'
    spec = importlib.util.spec_from_file_location('invoice_checks', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    baseline = json.loads((ROOT / 'skills/finance-commercial/invoice-po-check/assets/invoice.json').read_text())
    tests = []
    def check(name, predicate):
        if not predicate:
            raise AssertionError(name)
        tests.append({'name': name, 'status': 'passed'})
    result = module.invoice_check(baseline)
    check('Quantity and rate excess reconciled once', result['supported_excl_vat'] == '600.00' and result['lines'][0]['difference_excl_vat'] == '240.00' and result['supported_incl_vat'] == '630.00')
    check('Exceptions require hold rather than approval', result['recommendation'].startswith('Hold'))
    clean = copy.deepcopy(baseline)
    clean['invoice'].update(subtotal='600.00', vat='30.00', total='630.00')
    clean['invoice']['lines'][0].update(qty='60', rate='10', amount='600')
    r = module.invoice_check(clean)
    check('Complete matching material evidence remains manager review', r['recommendation'] == 'No exceptions in supplied evidence — manager review required' and all(c['state'] in {'Pass', 'Not applicable'} for c in r['checks']))
    missing = copy.deepcopy(clean)
    missing['history_complete'] = False
    missing['delivery_complete'] = False
    missing['invoice']['lines'][0].update(previous_qty=None, delivered_qty=None)
    r = module.invoice_check(missing)
    check('Missing history/delivery cannot produce a supported amount or clean review', r['supported_excl_vat'] is None and r['recommendation'].startswith('Incomplete') and any(c['state'] == 'Not checked' for c in r['checks']))
    duplicate = copy.deepcopy(clean)
    duplicate['history'].append({'vendor_id':'DEMO-V1','number':'DEMO-INV-01','date':'2026-10-09','total':'630'})
    check('Prior same-vendor invoice identifier triggers exception', any(c['check']=='Duplicates' and c['state']=='Exception' for c in module.invoice_check(duplicate)['checks']))
    no_tax = copy.deepcopy(clean)
    no_tax['tax_rate'] = None
    check('Unconfirmed tax treatment stays unreviewed', module.invoice_check(no_tax)['recommendation'].startswith('Incomplete'))
    foreign = copy.deepcopy(clean)
    foreign['invoice']['project_id'] = 'OTHER-PROJECT'
    r = module.invoice_check(foreign)
    check('Wrong project cannot have final supported amount', r['supported_excl_vat'] is None and r['recommendation'].startswith('Hold'))
    previous = copy.deepcopy(clean)
    previous['invoice']['lines'][0]['previous_qty'] = '90'
    check('Previously booked beyond accepted delivery gives zero remaining support', module.invoice_check(previous)['supported_excl_vat'] == '0.00')
    zero = copy.deepcopy(clean)
    zero['history'] = []
    zero['invoice']['lines'][0]['previous_qty'] = '0'
    check('Explicit complete zero-history evidence is accepted', module.invoice_check(zero)['recommendation'].startswith('No exceptions'))
    with tempfile.TemporaryDirectory() as directory:
        out = Path(directory)/'result.json'
        before = hashlib.sha256((ROOT/'skills/finance-commercial/invoice-po-check/assets/invoice.json').read_bytes()).hexdigest()
        run = subprocess.run([sys.executable,str(path),'invoice',str(ROOT/'skills/finance-commercial/invoice-po-check/assets/invoice.json'),'--out',str(out)],capture_output=True,text=True)
        after = hashlib.sha256((ROOT/'skills/finance-commercial/invoice-po-check/assets/invoice.json').read_bytes()).hexdigest()
        check('CLI produces expected output without modifying input', run.returncode == 0 and json.loads(out.read_text())['supported_excl_vat']=='600.00' and before==after)
        malformed = Path(directory)/'bad.json'
        malformed.write_text('{bad')
        failed = subprocess.run([sys.executable,str(path),'invoice',str(malformed),'--out',str(Path(directory)/'bad-output.json')],capture_output=True,text=True)
        check('Malformed input exits nonzero without creating review', failed.returncode != 0 and not (Path(directory)/'bad-output.json').exists())
    return tests

if __name__ == '__main__':
    print(json.dumps(invoice_tests(), indent=2))
