#!/usr/bin/env python3
"""Check current sources, relocated resources, plugins, marketplace, packaging and deterministic regressions."""
import ast,importlib.util,io,json,re,subprocess,sys,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'maintenance'))
from build_release import tree,digest,HELPERS,VERSION,MCP,included,plugin_name
MAX_DESCRIPTION=1024

def main():
 checks=[];failures=[]
 def check(name,fn):
  try:result=fn();checks.append({'check':name,'status':'passed','detail':result})
  except Exception as exc:failures.append(name);checks.append({'check':name,'status':'failed','detail':str(exc)})
 release=ROOT/'releases'/VERSION
 pending=release/'validation.json'
 if not pending.exists():pending.write_text('{"status":"running","scope":"local validation in progress"}\n')
 catalog=json.loads((ROOT/'catalog.json').read_text());skills=catalog['skills'];paths={s['name']:ROOT/s['source'] for s in skills}
 categories=sorted({s['category'] for s in skills});plugins={c:ROOT/'plugins'/plugin_name(c) for c in categories+['all']}
 def metadata():
  assert len(paths)==16 and len(skills)==16
  assert {p.parent for p in (ROOT/'skills').glob('*/*/SKILL.md')}==set(paths.values())
  for name,path in paths.items():
   text=(path/'SKILL.md').read_text();fm=text.split('---',2)[1]
   assert re.search(r'^name: '+re.escape(name)+'$',fm,re.M)
   desc=json.loads(re.search(r'^description: (.+)$',fm,re.M)[1]);assert 0<len(desc)<=MAX_DESCRIPTION,f'{name}: description {len(desc)} chars'
   assert 'Use when' in desc,f'{name}: description lacks a "Use when" trigger clause'
   assert f'version: "{VERSION}"' in fm
   assert 'python scripts/' not in text,f'{name}: use python3'
   if (path/'scripts').exists():assert re.search(r'^allowed-tools: .*Bash\(python3 \*\)',fm,re.M),f'{name}: scripts present but no allowed-tools Bash(python3 *)'
   for file in path.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',file.read_text()):
     if '://' not in link and not link.startswith('#'):assert (file.parent/link.split('#')[0]).exists(),f'{file}: {link}'
  return '16 unique current names, trigger descriptions, python3 helpers and local skill links'
 check('Catalogue and references',metadata)
 def commands():
  count=0
  for c in (ROOT/'commands').glob('*/*.md'):
   assert c.parent.name in categories,c
   fm=c.read_text().split('---',2)[1];assert re.search(r'^description: .+$',fm,re.M),c
   names={s['name'] for s in skills if s['category']==c.parent.name}|{s['name'] for s in skills if s['category']=='general'}
   referenced=set(re.findall(r'`([a-z0-9-]+)` skill',c.read_text()))
   assert referenced,f'{c}: no `skill-name` skill reference'
   assert referenced<= {s['name'] for s in skills},f'{c}: unknown skill {referenced-{s["name"] for s in skills}}'
   count+=1
  return f'{count} routine commands reference existing skills'
 check('Routine commands',commands)
 def plugin_layout():
  for c,plugin in plugins.items():
   manifest=json.loads((plugin/'.claude-plugin/plugin.json').read_text())
   assert manifest['name']==plugin_name(c) and manifest['version']==VERSION
   expected={s['name'] for s in skills if c=='all' or s['category']==c}
   assert {p.name for p in (plugin/'skills').iterdir()}==expected,c
   for name in expected:assert tree(plugin/'skills'/name)==tree(paths[name]),f'{c}/{name} drifted from source'
   assert json.loads((plugin/'.mcp.json').read_text())==MCP
   expected_commands={p.name for cat in (categories if c=='all' else [c]) for p in (ROOT/'commands'/cat).glob('*.md')}
   assert {p.name for p in (plugin/'commands').glob('*.md')} if (plugin/'commands').exists() else set()==expected_commands,f'{c}: commands'
   assert '{{' not in (plugin/'README.md').read_text(),f'{c}: README placeholder left'
  marketplace=json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
  assert marketplace['name']=='walkthru' and {p['name'] for p in marketplace['plugins']}=={plugin_name(c) for c in plugins}
  for p in marketplace['plugins']:assert (ROOT/p['source']/'.claude-plugin/plugin.json').exists(),p['source']
  return f'{len(plugins)} plugins match source; marketplace lists them all'
 check('Plugins and marketplace',plugin_layout)
 def claude_validate():
  if not __import__('shutil').which('claude'):return 'claude CLI not on PATH; skipped'
  out=[]
  for target in [ROOT,*plugins.values()]:
   r=subprocess.run(['claude','plugin','validate',str(target)],capture_output=True,text=True)
   assert r.returncode==0 and 'Validation passed' in r.stdout,f'{target.name}: {r.stdout}{r.stderr}'
   out.append(target.name)
  return 'claude plugin validate passed: '+', '.join(out)
 check('claude plugin validate',claude_validate)
 def packages():
  for s in skills:
   folder=paths[s['name']];package=release/'skills'/s['category']/(s['name']+'.zip')
   with ZipFile(package) as z:
    assert z.testzip() is None
    assert {n:z.read(n) for n in z.namelist()}=={s['name']+'/'+k:v for k,v in tree(folder).items()}
  for c,plugin in plugins.items():
   with ZipFile(release/'plugins'/f'{plugin.name}-{VERSION}.zip') as z:assert {n:z.read(n) for n in z.namelist()}=={plugin.name+'/'+k:v for k,v in tree(plugin).items()}
  with ZipFile(release/f'walkthru-all-skills-{VERSION}.zip') as z:assert {n:z.read(n) for n in z.namelist()}=={str(p.relative_to(release/'skills')):p.read_bytes() for p in (release/'skills').rglob('*.zip')}
  for group in categories:
   with ZipFile(release/'bundles'/(group+'.zip')) as z:assert {n:z.read(n) for n in z.namelist()}=={p.name:p.read_bytes() for p in (release/'skills'/group).glob('*.zip')}
  return 'All individual ZIPs, department bundles, all-skills bundle and plugin ZIPs match source bytes'
 check('Package/source parity',packages)
 def canonical():
  for helper,names in HELPERS.items():
   for name in names:assert (paths[name]/'scripts'/helper).read_bytes()==(ROOT/'maintenance/lib'/helper).read_bytes()
  return 'Canonical helper copies match'
 check('Canonical helpers',canonical)
 def hashes():
  manifest=json.loads((release/'manifest.json').read_text())
  for key in ['artifacts','current_sources']:
   for p,h in manifest[key].items():assert digest(ROOT/p)==h,p
  for line in (release/'SHA256SUMS').read_text().splitlines():
   h,p=line.split('  ',1);assert digest(ROOT/p)==h
  return 'Current source/artifact manifest and checksums valid'
 check('Current release checksums',hashes)
 def preserved():
  inventory=json.loads((ROOT/'references/inventory.json').read_text())
  for p,h in inventory['files'].items():assert digest(ROOT/p)==h,p
  return f'{len(inventory["files"])} upstream/employee reference files byte-preserved'
 check('Reference preservation',preserved)
 def syntax():
  count=0
  for base in ['skills','maintenance','plugins']:
   for p in (ROOT/base).rglob('*.py'):
    if included(p):ast.parse(p.read_text());count+=1
  for p in [*(ROOT/'skills').rglob('*.json'),*(ROOT/'plugins').rglob('*.json'),ROOT/'.claude-plugin/marketplace.json']:json.loads(p.read_text())
  return f'{count} maintained/generated Python files parsed; JSON checked, connector not authenticated'
 check('Syntax and config',syntax)
 def website():
  for doc in [ROOT/'index.html',ROOT/'docs/SKILL-CATALOGUE.md']:
   text=doc.read_text()
   for link in re.findall(r'href="([^"]+)"',text)+re.findall(r'\]\(([^)]+)\)',text):
    if not link.startswith(('http:','https:','#','data:','mailto:')):assert ((doc.parent/link) if doc.suffix=='.md' else (ROOT/link)).exists(),f'{doc.name}: {link}'
  return 'Catalogue links resolve to current local sources/packages'
 check('Catalogue links',website)
 stream=io.StringIO();suite=unittest.defaultTestLoader.discover(str(ROOT/'maintenance/tests'),pattern='test_*.py')
 result=unittest.TextTestRunner(stream=stream,verbosity=1).run(suite)
 checks.append({'check':'Original helper regressions','status':'passed' if result.wasSuccessful() else 'failed','tests':result.testsRun,'detail':stream.getvalue()})
 if not result.wasSuccessful():failures.append('Original helper regressions')
 def everyday():
  p=ROOT/'maintenance/everyday-regressions/invoice_regressions.py'
  spec=importlib.util.spec_from_file_location('daily_checks',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  return module.invoice_tests()
 check('Everyday invoice regressions',everyday)
 report={'version':VERSION,'status':'passed' if not failures else 'failed','scope':'Offline deterministic/structural checks only; behavioral evals run separately with `claude plugin eval`','checks':checks,'employee_model_acceptance':'pending','authenticated_connector_acceptance':'pending'}
 (release/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'checks':len(checks),'original_regression_tests':result.testsRun,'failures':failures},indent=2))
 for c in checks:
  if c['status']=='failed':print(c)
 return bool(failures)
if __name__=='__main__':sys.exit(main())
