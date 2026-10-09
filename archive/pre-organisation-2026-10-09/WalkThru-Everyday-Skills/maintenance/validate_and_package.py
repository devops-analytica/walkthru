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

ROOT = Path(__file__).resolve().parents[1]
def invoice_tests():
    path = ROOT / 'skills/invoice-po-check/scripts/operation_checks.py'
    spec = importlib.util.spec_from_file_location('invoice_checks', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    baseline = json.loads((ROOT / 'skills/invoice-po-check/assets/invoice.json').read_text())
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
        before = hashlib.sha256((ROOT/'skills/invoice-po-check/assets/invoice.json').read_bytes()).hexdigest()
        run = subprocess.run([sys.executable,str(path),'invoice',str(ROOT/'skills/invoice-po-check/assets/invoice.json'),'--out',str(out)],capture_output=True,text=True)
        after = hashlib.sha256((ROOT/'skills/invoice-po-check/assets/invoice.json').read_bytes()).hexdigest()
        check('CLI produces expected output without modifying input', run.returncode == 0 and json.loads(out.read_text())['supported_excl_vat']=='600.00' and before==after)
        malformed = Path(directory)/'bad.json'
        malformed.write_text('{bad')
        failed = subprocess.run([sys.executable,str(path),'invoice',str(malformed),'--out',str(Path(directory)/'bad-output.json')],capture_output=True,text=True)
        check('Malformed input exits nonzero without creating review', failed.returncode != 0 and not (Path(directory)/'bad-output.json').exists())
    return tests

def main():
    manifest = json.loads((ROOT/'manifest.json').read_text())
    structural = []
    dist = ROOT/'dist'
    dist.mkdir(exist_ok=True)
    for skill in manifest['skills']:
        name = skill['name']
        folder = ROOT/'skills'/name
        entry = (folder/'SKILL.md').read_text()
        front = entry.split('---',2)[1]
        assert re.search(r'^name: '+re.escape(name)+r'$',front,re.M), name
        desc = re.search(r'^description: (.+)$',front,re.M)
        assert desc and 0 < len(json.loads(desc[1])) <= 200, name
        assert len(name)<64 and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',name)
        assert '[TODO:' not in entry
        for file in folder.rglob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)',file.read_text()):
                if not link.startswith(('https://','http://','#')):
                    assert (file.parent/link).exists(), f'{name}: missing link {link}'
        assert list((folder/'assets').iterdir()), name
        assert (folder/'references/practice.md').exists(), name
        json.loads((folder/'references/project-context.example.json').read_text())
        for file in folder.rglob('*.py'):
            compile(file.read_text(),str(file),'exec')
        package = dist/(name+'.zip')
        files = sorted(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
        with ZipFile(package,'w',ZIP_DEFLATED) as archive:
            for file in files:
                archive.write(file,str(Path(name)/file.relative_to(folder)))
        with ZipFile(package) as archive:
            assert set(archive.namelist()) == {str(Path(name)/p.relative_to(folder)) for p in files}
            assert archive.testzip() is None
            for file in files:
                assert archive.read(str(Path(name)/file.relative_to(folder))) == file.read_bytes()
        structural.append({'skill':name,'status':'passed','files':len(files),'checks':['frontmatter/name/description','local links','assets and practice cases','context JSON','Python syntax where applicable','ZIP byte parity/integrity']})
    tests = invoice_tests()
    cases = json.loads((ROOT/'evaluation-cases.json').read_text())
    assert len(cases)==16 and all(c['status'].startswith('pending') for c in cases)
    report = {'status':'passed','scope':'Offline structure, packaging and deterministic material-invoice helper only','skills':structural,'invoice_regressions':tests,'model_behavioral_cases':{'total':len(cases),'status':'pending; not executed'},'real_project_acceptance':'pending departmental review','live_integrations':'not configured or tested'}
    (ROOT/'validation-report.json').write_text(json.dumps(report,indent=2)+'\n')
    bundle=ROOT/'WalkThru-Everyday-Skills-1.0.0.zip'
    with ZipFile(bundle,'w',ZIP_DEFLATED) as archive:
        for package in sorted(dist.glob('*.zip')):
            archive.write(package,'dist/'+package.name)
        for name in ['README.md','manifest.json','validation-report.json','evaluation-cases.json','review.html','skill-format-validation.json']:
            if (ROOT/name).exists(): archive.write(ROOT/name,name)
    sums=[]
    for file in [*sorted(dist.glob('*.zip')),bundle]:
        sums.append(hashlib.sha256(file.read_bytes()).hexdigest()+'  '+str(file.relative_to(ROOT)))
    (ROOT/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    print(json.dumps({'status':'passed','skills':len(structural),'invoice_regressions':len(tests),'pending_model_cases':len(cases),'bundle':str(bundle)},indent=2))

if __name__=='__main__':
    main()
