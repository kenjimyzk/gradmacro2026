"""Check source references and preservation without modifying course materials."""
from pathlib import Path
from collections import Counter
import hashlib, json, re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
names = [f'lecture{i:02d}' for i in range(1,13)]+['solution']
before = json.loads((OUT/'source-before-sha256.json').read_text())
changed = [p for p,h in before.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
checks = {}
for name in names:
    text = (ROOT/(name+'.qmd')).read_text()
    for inc in re.findall(r'\{\{<\s*include\s+([^ ]+)\s*>\}\}',text):
        text += '\n'+(ROOT/inc).read_text()
    labels = re.findall(r'\{#((?:eq|fig|tbl|sec)-[\w-]+)',text)
    labels += re.findall(r'^#\|\s*label:\s*((?:eq|fig|tbl|sec)-[\w-]+)',text,re.M)
    refs = re.findall(r'(?<![\w])@((?:eq|fig|tbl|sec)-[\w-]+)',text)
    assets = re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text)
    checks[name] = {
        'labels':len(labels), 'internal_references':len(refs),
        'duplicate_labels':[v for v,n in Counter(labels).items() if n>1],
        'unresolved_internal_references':sorted(set(refs)-set(labels)),
        'missing_images':[a for a in assets if not a.startswith(('https:','http:','data:')) and not (ROOT/a.split()[0]).exists()],
        'display_math_delimiters':len(re.findall(r'^\$\$\s*$',text,re.M)),
        'source_sha256':hashlib.sha256((ROOT/(name+'.qmd')).read_bytes()).hexdigest(),
    }
result={'protected_file_count':len(before),'protected_changed':changed,'documents':checks}
(OUT/'source-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
