"""Read-only validation of this static book. No network, model calls or experiments."""
import json, hashlib, re
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
for name,digest in m['files'].items():
 p=root/name
 assert p.is_file(), name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
for p in root.glob('*.ipynb'):
 n=json.loads(p.read_text()); assert n['nbformat']==4 and n['nbformat_minor']==5
 assert len({c['id'] for c in n['cells']})==len(n['cells'])
 for c in n['cells']:
  assert c['cell_type']=='markdown' and 'outputs' not in c
  for link in re.findall(r'\]\(([^)]+)\)', ''.join(c['source'])):
   if '://' not in link and not link.startswith('#'):
    assert (p.parent/link.split('#')[0]).is_file(),(p.name,link)
intro=''.join(''.join(c['source']) for c in json.loads((root/'00_READ_FIRST.ipynb').read_text())['cells'])
for filename,condition in [('oko_assessment.json','access'),('fa18_assessment.json','feasibility'),('fa18_assessment.json','effect')]:
 text=json.loads((root/'sources'/filename).read_text())['practical_control'][condition]['rationale']
 assert text in intro,(filename,condition)
full=''.join(''.join(c['source']) for c in json.loads((root/'01_COMPLETE_CASE_RECORDS.ipynb').read_text())['cells'])
for filename in ['oko_assessment.json','zg710_assessment.json','fa18_assessment.json']:
 for condition in ['access','comprehension','authority','feasibility','exercise','effect']:
  exact=json.loads((root/'sources'/filename).read_text())['practical_control'][condition]['rationale']
  assert exact in full,(filename,condition)
print(json.dumps({'manifest_files_passed':len(m['files']),'notebooks_checked':len(list(root.glob('*.ipynb'))),'selected_exact_rationales_checked':3,'complete_chapter_rationales_checked':18,'static_local_links':'passed','execution':'no notebook cells, original study code, model calls or network requests executed'},indent=2))
