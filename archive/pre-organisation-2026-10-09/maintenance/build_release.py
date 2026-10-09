#!/usr/bin/env python3
"""Build skill/plugin packages and a hash manifest from maintained local sources.

No downloads or installations. Copies canonical helpers/references to standalone
skills, builds a WalkThru-only plugin, and packages exact source bytes.
"""
import hashlib
import json
import re
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.1.0'
HELPERS = {'xer_check.py': ['p6-programme-review', 'planning-weekly-report'],
           'operation_checks.py': ['invoice-po-check', 'walkthru-deadline-watch', 'planning-weekly-report']}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def included(path):
    return path.is_file() and '.DS_Store' not in path.parts and '__pycache__' not in path.parts and path.suffix != '.pyc'


def zip_tree(source, destination, prefix=None):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob('*')):
            if included(path):
                name = path.relative_to(source).as_posix()
                if prefix: name = prefix + '/' + name
                info = ZipInfo(name, date_time=(2026, 10, 8, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes())


def main():
    skills_root = ROOT / 'WalkThru-Skills'
    skills = sorted(skills_root.glob('*/*/SKILL.md'))
    if len(skills) != 15: raise ValueError('Expected 15 maintained custom skills')
    names = {p.parent.name: p.parent for p in skills}
    for p in skills:
        text = p.read_text()
        name = re.search(r'^name:\s*(.+)$', text, re.M).group(1).strip().strip('"')
        description = re.search(r'^description:\s*"(.*)"$', text, re.M).group(1)
        if name != p.parent.name or not re.fullmatch('[a-z0-9-]{1,64}', name) or len(description) > 200:
            raise ValueError(f'Invalid skill metadata: {p}')
        refs = p.parent / 'references'; refs.mkdir(exist_ok=True)
        shutil.copyfile(ROOT / 'config/evidence-rules.md', refs / 'project-context.md')
        shutil.copyfile(ROOT / 'config/project-context.example.json', refs / 'project-context.example.json')
    for helper, targets in HELPERS.items():
        for name in targets:
            scripts = names[name] / 'scripts'; scripts.mkdir(exist_ok=True)
            shutil.copyfile(ROOT / 'maintenance/lib' / helper, scripts / helper)
            if helper == 'operation_checks.py':
                shutil.copyfile(ROOT / 'config/operation-checks.md', names[name] / 'references/operation-checks.md')
    plugin = ROOT / 'plugins/walkthru-workflows'
    (plugin / '.claude-plugin').mkdir(parents=True, exist_ok=True)
    (plugin / '.claude-plugin/plugin.json').write_text(json.dumps({
        'name': 'walkthru-workflows', 'version': VERSION,
        'description': 'WalkThru project reporting, schedule-health, invoice evidence and draft correspondence workflows. Microsoft 365 search/read or uploaded-export fallback.',
        'author': {'name': 'WalkThru internal toolkit'}}, indent=2) + '\n')
    (plugin / '.mcp.json').write_text(json.dumps({'mcpServers': {'microsoft365': {
        'type': 'http', 'url': 'https://microsoft365.mcp.claude.com/mcp'}}}, indent=2) + '\n')
    for name, source in names.items():
        target = plugin / 'skills' / name
        if target.exists(): shutil.rmtree(target)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
    shutil.copyfile(ROOT / 'config/plugin-setup.md', plugin / 'README.md')
    for p in skills:
        zip_tree(p.parent, skills_root / 'dist' / p.parent.parent.name / (p.parent.name + '.zip'), p.parent.name)
    for group, output in [('general', 'WalkThru-general-skills.zip'), ('group-4', 'WalkThru-group4-skills.zip')]:
        destination = skills_root / 'share' / output
        with ZipFile(destination, 'w', ZIP_DEFLATED) as z:
            for package in sorted((skills_root / 'dist' / group).glob('*.zip')):
                info = ZipInfo(package.name, date_time=(2026,10,8,0,0,0)); info.compress_type = ZIP_DEFLATED
                z.writestr(info, package.read_bytes())
    zip_tree(skills_root / 'samples', skills_root / 'share/WalkThru-sample-inputs.zip', 'samples')
    zip_tree(plugin, ROOT / 'releases/walkthru-workflows-1.1.0.zip', 'walkthru-workflows')
    paths = list(skills_root.glob('dist/*/*.zip')) + list(skills_root.glob('share/*.zip')) + [ROOT / 'releases/walkthru-workflows-1.1.0.zip']
    manifest = {'version': VERSION, 'review_date': '2026-10-08', 'maintainer_role': 'WalkThru AI lead / trainer',
                'department_signoff_roles': ['Planning Manager', 'Operations Manager', 'Finance/Commercial reviewer', 'IT administrator'],
                'status': 'local checks passed; real-project and tenant acceptance pending',
                'sources': json.loads((ROOT / 'sources.json').read_text()),
                'artifacts': {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)},
                'custom_sources': {str(p.relative_to(ROOT)): digest(p) for p in sorted(skills_root.rglob('*')) if included(p) and 'dist' not in p.parts and 'share' not in p.parts},
                'canonical_helpers': {str(p.relative_to(ROOT)): digest(p) for p in sorted((ROOT / 'maintenance/lib').glob('*.py'))}}
    (ROOT / 'releases/manifest-1.1.0.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (ROOT / 'releases/SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT)}\n' for p in sorted(paths)))
    print(f'Built {len(skills)} skill ZIPs, 3 sharing bundles, 1 WalkThru plugin, and release manifest')


if __name__ == '__main__':
    main()
