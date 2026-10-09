#!/usr/bin/env python3
"""Offline validation. Writes releases/local-validation.json, exits non-zero on failure.

Validates helpers, fixture CLI behavior, package/source parity, relative references,
metadata, JSON/MCP configuration, Python syntax and DOCX XML integrity. Does not
authenticate Microsoft 365 or run model-based skill acceptance.
"""
import ast
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'maintenance'))
from build_release import HELPERS, included


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.records = []
    def addSuccess(self, test):
        super().addSuccess(test); self.records.append({'test': test.id(), 'status': 'pass'})
    def addFailure(self, test, err):
        super().addFailure(test, err); self.records.append({'test': test.id(), 'status': 'fail', 'detail': self._exc_info_to_string(err, test)})
    def addError(self, test, err):
        super().addError(test, err); self.records.append({'test': test.id(), 'status': 'error', 'detail': self._exc_info_to_string(err, test)})


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks, failures = [], []
    def verify(name, fn):
        try:
            detail = fn(); checks.append({'check': name, 'status': 'pass', 'detail': detail})
        except Exception as exc:
            failures.append(name); checks.append({'check': name, 'status': 'fail', 'detail': str(exc)})
    paths = sorted(ROOT.glob('WalkThru-Skills/*/*/SKILL.md'))
    def metadata():
        assert len(paths) == 15
        for p in paths:
            text = p.read_text(); assert text.startswith('---\n')
            fm = text.split('---', 2)[1]
            name = re.search(r'^name:\s*(.*)$', fm, re.M).group(1).strip().strip('"')
            desc = re.search(r'^description:\s*"(.*)"$', fm, re.M).group(1)
            assert name == p.parent.name and re.fullmatch('[a-z0-9-]{1,64}', name)
            assert 0 < len(desc) <= 200 and '<' not in desc and '>' not in desc
            assert 'version: "1.1.0"' in fm and 'owner_role:' in fm
        return '15 skill names, descriptions and revision metadata validated'
    verify('Custom skill metadata', metadata)
    def references():
        count = 0
        for p in paths:
            for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
                if '://' not in target and not target.startswith('#'):
                    assert (p.parent / target.split('#')[0]).is_file(), f'{p.relative_to(ROOT)}: missing {target}'
                    count += 1
        return f'{count} entrypoint relative references resolved'
    verify('Skill references', references)
    def python_syntax():
        python = [p for p in ROOT.rglob('*.py') if included(p)]
        for p in python: ast.parse(p.read_text(), filename=str(p.relative_to(ROOT)))
        return f'{len(python)} Python files parsed; not a runtime audit of upstream scripts'
    verify('Python syntax', python_syntax)
    def canonical():
        for helper, targets in HELPERS.items():
            expected = (ROOT / 'maintenance/lib' / helper).read_bytes()
            for name in targets:
                path = next(p.parent for p in paths if p.parent.name == name)
                assert (path / 'scripts' / helper).read_bytes() == expected
                assert (ROOT / 'plugins/walkthru-workflows/skills' / name / 'scripts' / helper).read_bytes() == expected
        return '5 standalone helper copies and plugin equivalents match canonical sources'
    verify('Canonical helper parity', canonical)
    def packages():
        for p in paths:
            package = ROOT / 'WalkThru-Skills/dist' / p.parent.parent.name / (p.parent.name + '.zip')
            with ZipFile(package) as z:
                expected = {p.parent.name + '/' + f.relative_to(p.parent).as_posix(): f.read_bytes() for f in p.parent.rglob('*') if included(f)}
                actual = {name: z.read(name) for name in z.namelist()}
                assert actual == expected, f'ZIP/source mismatch: {package.name}'
            plugin_source = ROOT / 'plugins/walkthru-workflows/skills' / p.parent.name
            original = {f.relative_to(p.parent).as_posix(): f.read_bytes() for f in p.parent.rglob('*') if included(f)}
            generated = {f.relative_to(plugin_source).as_posix(): f.read_bytes() for f in plugin_source.rglob('*') if included(f)}
            assert original == generated, 'Generated plugin skill mismatch'
        plugin = ROOT / 'plugins/walkthru-workflows'
        with ZipFile(ROOT / 'releases/walkthru-workflows-1.1.0.zip') as z:
            expected = {'walkthru-workflows/' + f.relative_to(plugin).as_posix(): f.read_bytes() for f in plugin.rglob('*') if included(f)}
            assert {n:z.read(n) for n in z.namelist()} == expected
        for group, name in [('general','WalkThru-general-skills.zip'),('group-4','WalkThru-group4-skills.zip')]:
            with ZipFile(ROOT / 'WalkThru-Skills/share' / name) as z:
                expected = {p.name:p.read_bytes() for p in (ROOT/'WalkThru-Skills/dist'/group).glob('*.zip')}
                assert {n:z.read(n) for n in z.namelist()} == expected
        return '15 upload ZIPs, generated plugin and 2 skill sharing bundles match exact source bytes'
    verify('Package/source parity', packages)
    def configs():
        for p in ROOT.rglob('*.json'):
            if included(p): json.loads(p.read_text())
        plugin = ROOT / 'plugins/walkthru-workflows'
        cfg = json.loads((plugin / '.mcp.json').read_text())
        assert cfg == {'mcpServers': {'microsoft365': {'type':'http', 'url':'https://microsoft365.mcp.claude.com/mcp'}}}
        assert json.loads((plugin / '.claude-plugin/plugin.json').read_text())['version'] == '1.1.0'
        return 'JSON valid; custom plugin has one official non-empty M365 endpoint; authentication not tested'
    verify('Configuration structure', configs)
    def manifests():
        manifest = json.loads((ROOT/'releases/manifest-1.1.0.json').read_text())
        for section in ['artifacts','custom_sources','canonical_helpers']:
            for name, digest in manifest[section].items(): assert sha(ROOT/name) == digest, 'Stale manifest: '+name
        for line in (ROOT/'releases/SHA256SUMS').read_text().splitlines():
            digest, name = line.split('  ',1); assert sha(ROOT/name) == digest
        return 'Artifact, maintained source and helper hashes match release manifest'
    verify('Release checksums', manifests)
    def documents():
        for name in ['Group-4/Group-4-Training-Plan.docx','report/WalkThru-Claude-Rollout.docx']:
            with ZipFile(ROOT/name) as z:
                assert z.testzip() is None
                for part in z.namelist():
                    if part.endswith('.xml'): ET.fromstring(z.read(part))
        return 'Both modified DOCX archives and all their XML parts parse'
    verify('Word document integrity', documents)
    def fixtures():
        helper = ROOT/'maintenance/lib/operation_checks.py'
        with tempfile.TemporaryDirectory() as d:
            for kind in ['invoice','variance','deadlines']:
                output = Path(d)/(kind+'.json')
                run = subprocess.run([sys.executable,str(helper),kind,str(ROOT/'maintenance/tests/fixtures'/(kind+'.json')),'--out',str(output)],capture_output=True,text=True)
                assert run.returncode == 0, run.stderr
                result = json.loads(output.read_text())
                if kind == 'invoice': assert result['supported_incl_vat'] == '29610.00'
                elif kind == 'variance': assert result['variance_percentage_points'] == '-5'
                else:
                    assert {x['id'] for x in result['items']} == {'PERMIT-1','GUARANTEE-1'}
            run = subprocess.run([sys.executable,str(ROOT/'maintenance/lib/xer_check.py'),str(ROOT/'maintenance/tests/fixtures/multi-project.xer'),'--out-dir',str(Path(d)/'schedule')],capture_output=True,text=True)
            assert run.returncode == 0, run.stderr
            assert 'Should have started' in run.stdout
        return '4 synthetic fixture CLIs produced independently asserted results'
    verify('Fixture CLI outputs', fixtures)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT/'maintenance/tests'), pattern='test_*.py')
    result = unittest.TextTestRunner(stream=stream, resultclass=RecordedResult, verbosity=2).run(suite)
    if not result.wasSuccessful(): failures.append('Helper regression tests')
    report = {'version':'1.1.0','scope':'offline deterministic and structural validation; not a model or tenant acceptance test',
              'status':'pass' if not failures else 'fail', 'checks':checks, 'regression_tests':result.records,
              'tests_run':result.testsRun,'pending_external':'See acceptance-log.json and behavioral-cases.json; no model, live-project or authenticated connector pass is claimed.'}
    (ROOT/'releases/local-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'{len(checks)} release checks; {result.testsRun} regression tests; status={report["status"]}')
    for c in checks:
        if c['status'] != 'pass': print(c['check']+': '+c['detail'])
    if not result.wasSuccessful(): print(stream.getvalue())
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
