#!/usr/bin/env python3
"""Build catalog-driven skill ZIPs, department plugins, the all-in-one plugin and the marketplace from the single maintained source tree."""
import hashlib,json,re,shutil
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED,ZipInfo
ROOT=Path(__file__).resolve().parents[1]
VERSION='2.1.0'
ZIP_DATE=(2026,10,9,0,0,0)
MARKETPLACE_REPO='analytica-data/WalkThru-Claude-Toolkit'  # update when the repo is pushed
HELPERS={'xer_check.py':['p6-programme-review','planning-weekly-report'],'operation_checks.py':['invoice-po-check','walkthru-deadline-watch','planning-weekly-report']}
MCP={'mcpServers':{'microsoft365':{'type':'http','url':'https://microsoft365.mcp.claude.com/mcp'}}}
CATEGORY_TITLES={'general':'General and coordination','site-operations':'Site and operations','engineering':'Engineering, technical and document control','procurement':'Procurement and materials','finance-commercial':'Finance and commercial','planning':'Planning and project controls','estimation-commercial':'Estimation, tendering and contracts','hr-admin':'HR, administration and PRO'}
ALL_PLUGIN='walkthru-workflows'
def included(p):return p.is_file() and p.name!='.DS_Store' and '__pycache__' not in p.parts and p.suffix!='.pyc'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p):return {str(f.relative_to(p)):f.read_bytes() for f in sorted(p.rglob('*')) if included(f)}
def zip_files(contents,dest):
 dest.parent.mkdir(parents=True,exist_ok=True)
 with ZipFile(dest,'w',ZIP_DEFLATED) as z:
  for name,data in sorted(contents.items()):
   info=ZipInfo(name,ZIP_DATE);info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data)
def plugin_name(category):return ALL_PLUGIN if category=='all' else 'walkthru-'+category
def plugin_description(category,skills):
 if category=='all':return f'All {len(skills)} maintained WalkThru daily and recurring employee workflows. Evidence-based drafts, optional Microsoft 365 read access and uploaded-export fallback.'
 return f'WalkThru {CATEGORY_TITLES[category]} workflows ({len(skills)} skills): '+', '.join(s['title'] for s in skills)+'. Evidence-based drafts; optional Microsoft 365 read access.'
def write_plugin(category,skills,names):
 plugin=ROOT/'plugins'/plugin_name(category)
 if plugin.exists():shutil.rmtree(plugin)
 (plugin/'.claude-plugin').mkdir(parents=True)
 (plugin/'.claude-plugin/plugin.json').write_text(json.dumps({'name':plugin_name(category),'version':VERSION,'description':plugin_description(category,skills),'author':{'name':'WalkThru internal toolkit'}},indent=2)+'\n')
 (plugin/'.mcp.json').write_text(json.dumps(MCP,indent=2)+'\n')
 for s in skills:shutil.copytree(names[s['name']],plugin/'skills'/s['name'],ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store'))
 categories=sorted({s['category'] for s in skills})
 commands=[c for cat in categories for c in sorted((ROOT/'commands'/cat).glob('*.md'))]
 if commands:
  (plugin/'commands').mkdir()
  for c in commands:shutil.copyfile(c,plugin/'commands'/c.name)
 evals=ROOT/'evals'
 if evals.exists():
  wanted={s['name'] for s in skills}
  for case in sorted(evals.glob('*/prompt.md')):
   if case.parent.name.rsplit('-',1)[0] in wanted:shutil.copytree(case.parent,plugin/'evals'/case.parent.name)
 readme=(ROOT/'config/plugin-setup.md').read_text()
 readme=readme.replace('{{PLUGIN}}',plugin_name(category)).replace('{{VERSION}}',VERSION).replace('{{REPO}}',MARKETPLACE_REPO).replace('{{SKILLS}}','\n'.join(f'- `{s["name"]}` — {s["title"]}' for s in skills))
 (plugin/'README.md').write_text(readme)
 return plugin
def render_catalogue(skills,categories):
 """Regenerate index.html filter/cards and docs/SKILL-CATALOGUE.md from catalog.json; static copy stays."""
 esc=lambda s:s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
 options='<option value="all">All departments</option>'+''.join(f'<option value="{c}">{esc(CATEGORY_TITLES[c])}</option>' for c in categories)
 cards=''.join(f'<article data-category="{s["category"]}" data-search="{esc((s["title"]+" "+s["description"]+" "+s["roles"]).lower())}"><span class="dept">{esc(CATEGORY_TITLES[s["category"]])}</span><h2>{esc(s["title"])}</h2><p class="roles">{esc(s["roles"])}</p><p>{esc(s["description"])}</p><div class="actions"><a class="button" href="releases/{VERSION}/skills/{s["category"]}/{s["name"]}.zip" download>Download ZIP</a><a href="{s["source"]}/SKILL.md">Source instructions</a></div><p class="meta">Version {VERSION} · employee acceptance pending</p></article>' for s in skills)
 html=ROOT/'index.html';text=html.read_text()
 text=re.sub(r'(<select id="department">).*?(</select>)',lambda m:m[1]+options+m[2],text,count=1,flags=re.S)
 text=re.sub(r'(<section class="grid" id="skills">).*?(</section>)',lambda m:m[1]+cards+m[2],text,count=1,flags=re.S)
 text=re.sub(r'(<span class="count" id="count" aria-live="polite">)\d+ skills',lambda m:m[1]+f'{len(skills)} skills',text,count=1)
 html.write_text(text)
 rows='\n'.join(f'| {CATEGORY_TITLES[s["category"]]} | {s["title"]} | [Edit source](../{s["source"]}/SKILL.md) | [Download](../releases/{VERSION}/skills/{s["category"]}/{s["name"]}.zip) |' for s in skills)
 (ROOT/'docs/SKILL-CATALOGUE.md').write_text('# Current maintained skills\n\nEdit the source listed here; install generated ZIPs, not reference snapshots. All department/model acceptance is pending. Generated by `maintenance/build_release.py` from `catalog.json`.\n\n| Department | Skill | Source | Current ZIP |\n|---|---|---|---|\n'+rows+'\n')
def main():
 catalog=json.loads((ROOT/'catalog.json').read_text());skills=catalog['skills'];names={s['name']:ROOT/s['source'] for s in skills}
 assert len(names)==len(skills),'duplicate skill names'
 found={str(p.parent.relative_to(ROOT)) for p in (ROOT/'skills').glob('*/*/SKILL.md')}
 assert found=={s['source'] for s in skills},'Catalogue/source mismatch'
 for s in skills:
  source=names[s['name']];text=(source/'SKILL.md').read_text()
  assert re.search(r'^name: '+re.escape(s['name'])+'$',text,re.M)
  assert f'version: "{VERSION}"' in text,f'{s["name"]}: metadata.version must be {VERSION}'
  refs=source/'references';refs.mkdir(exist_ok=True)
  shutil.copyfile(ROOT/'config/evidence-rules.md',refs/'project-context.md')
  shutil.copyfile(ROOT/'config/project-context.example.json',refs/'project-context.example.json')
 for helper,targets in HELPERS.items():
  for name in targets:
   scripts=names[name]/'scripts';scripts.mkdir(exist_ok=True)
   shutil.copyfile(ROOT/'maintenance/lib'/helper,scripts/helper)
   if helper=='operation_checks.py':shutil.copyfile(ROOT/'config/operation-checks.md',names[name]/'references/operation-checks.md')
 categories=sorted({s['category'] for s in skills})
 for stale in (ROOT/'plugins').iterdir():
  if stale.is_dir() and stale.name not in {plugin_name(c) for c in categories+['all']}:shutil.rmtree(stale)
 plugins={c:write_plugin(c,[s for s in skills if s['category']==c],names) for c in categories}
 plugins['all']=write_plugin('all',skills,names)
 (ROOT/'.claude-plugin').mkdir(exist_ok=True)
 marketplace={'$schema':'https://anthropic.com/claude-code/marketplace.schema.json','name':'walkthru','description':'WalkThru contracting workflows for Claude: one general plugin for everyone plus one plugin per department, or the all-in-one package.','owner':{'name':'WalkThru internal toolkit'},'metadata':{'version':VERSION},'plugins':[{'name':plugin_name(c),'source':'./plugins/'+plugin_name(c),'description':plugin_description(c,[s for s in skills if c=='all' or s['category']==c]),'version':VERSION,'category':'productivity','author':{'name':'WalkThru internal toolkit'}} for c in ['all']+categories]}
 (ROOT/'.claude-plugin/marketplace.json').write_text(json.dumps(marketplace,indent=2)+'\n')
 release=ROOT/'releases'/VERSION
 evals_record=(release/'evals.json').read_bytes() if (release/'evals.json').exists() else None  # keep the recorded eval run across rebuilds
 if release.exists():shutil.rmtree(release)
 release.mkdir(parents=True)
 if evals_record:(release/'evals.json').write_bytes(evals_record)
 packages=[]
 for s in skills:
  path=release/'skills'/s['category']/(s['name']+'.zip')
  zip_files({s['name']+'/'+k:v for k,v in tree(names[s['name']]).items()},path);packages.append(path)
 for category in categories:
  zip_files({p.name:p.read_bytes() for p in packages if p.parent.name==category},release/'bundles'/(category+'.zip'))
 zip_files({str(p.relative_to(release/'skills')):p.read_bytes() for p in packages},release/f'walkthru-all-skills-{VERSION}.zip')
 for c,plugin in plugins.items():
  zip_files({plugin.name+'/'+k:v for k,v in tree(plugin).items()},release/'plugins'/f'{plugin.name}-{VERSION}.zip')
 shutil.copyfile(ROOT/'.claude-plugin/marketplace.json',release/'marketplace.json')
 artifacts=[p for p in release.rglob('*.zip') if included(p)]
 source_files=[ROOT/'catalog.json',*list((ROOT/'skills').rglob('*')),*list((ROOT/'commands').rglob('*')),*list((ROOT/'config').rglob('*')),*list((ROOT/'maintenance/lib').rglob('*')),*(list((ROOT/'evals').rglob('*')) if (ROOT/'evals').exists() else [])]
 manifest={'version':VERSION,'status':'built; see validation.json for local checks; departmental/tenant acceptance pending','plugins':{p.name:sorted(d.name for d in (p/'skills').iterdir()) for p in plugins.values()},'artifacts':{str(p.relative_to(ROOT)):digest(p) for p in sorted(artifacts)},'current_sources':{str(p.relative_to(ROOT)):digest(p) for p in sorted(source_files) if included(p) and 'results' not in p.parts}}
 (release/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (release/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT)}\n' for p in sorted(artifacts)))
 (ROOT/'releases/CURRENT.json').write_text(json.dumps({'version':VERSION,'path':'releases/'+VERSION,'individual_skills':len(skills),'plugins':sorted(p.name for p in plugins.values()),'plugin_is_generated':True,'acceptance':'local validation separate; employee/project/tenant acceptance pending'},indent=2)+'\n')
 render_catalogue(skills,categories)
 for doc in [ROOT/'index.html',ROOT/'docs/SKILL-CATALOGUE.md']:
  text=doc.read_text()
  for pat,rep in [(r'releases/\d+\.\d+\.\d+/',f'releases/{VERSION}/'),(r'-\d+\.\d+\.\d+\.zip',f'-{VERSION}.zip'),(r'TOOLKIT \d+\.\d+\.\d+',f'TOOLKIT {VERSION}'),(r'Version \d+\.\d+\.\d+ ·',f'Version {VERSION} ·')]:text=re.sub(pat,rep,text)
  doc.write_text(text)
 print(f'Built {len(skills)} individual skills, {len(categories)} department bundles, all-skills bundle, {len(plugins)} plugins and marketplace.json for {VERSION}')
if __name__=='__main__':main()
