"""Check revised sources, generated HTML references/math, and PDF render agreement."""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
WORK=Path(json.loads((OUT/'render-state.json').read_text())['work'])
NAMES=[f'lecture{i:02d}' for i in range(1,13)]+['solution']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.refs=[]; self.assets=[]; self.math=[]; self.depth=0; self.parts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a' and 'href' in a: self.refs.append(a['href'])
        if tag in ['img','script'] and 'src' in a: self.assets.append(a['src'])
        if tag=='link' and 'href' in a: self.assets.append(a['href'])
        if tag=='span' and 'math' in a.get('class','').split():
            self.depth=1; self.parts=[]; self.display='display' in a.get('class','').split()
        elif tag=='span' and self.depth: self.depth+=1
    def handle_endtag(self,tag):
        if tag=='span' and self.depth:
            self.depth-=1
            if not self.depth: self.math.append({'tex':''.join(self.parts),'display':self.display})
    def handle_data(self,data):
        if self.depth: self.parts.append(data)
def absent(url):
    u=urlsplit(url)
    return not (u.scheme or u.netloc) and bool(u.path) and not (WORK/unquote(u.path)).exists()

render=json.loads((OUT/'render-results.json').read_text())
results={}; errors=[]; math={}
for name in NAMES:
    source=(ROOT/(name+'.qmd')).read_text()
    expanded=source
    for inc in re.findall(r'\{\{<\s*include\s+([^ ]+)\s*>\}\}',source): expanded+='\n'+(ROOT/inc).read_text()
    labels=re.findall(r'\{#((?:eq|fig|tbl|sec)-[\w-]+)',expanded)+re.findall(r'^#\|\s*label:\s*((?:eq|fig|tbl|sec)-[\w-]+)',expanded,re.M)
    refs=re.findall(r'(?<![\w])@((?:eq|fig|tbl|sec)-[\w-]+)',expanded)
    html=(OUT/'html'/(name+'.html')).read_text(); p=Parser(); p.feed(html)
    r={
       'rendered_source_matches_live':render[name]['source_sha256']==sha(ROOT/(name+'.qmd')),
       'rendered_html_matches_work':sha(OUT/'html'/(name+'.html'))==sha(WORK/(name+'.html')),
       'rendered_pdf_matches_work':sha(OUT/'pdf'/(name+'.pdf'))==sha(WORK/(name+'.pdf')),
       'source_duplicate_labels':[v for v,n in Counter(labels).items() if n>1],
       'source_missing_refs':sorted(set(refs)-set(labels)),
       'html_duplicate_ids':[v for v,n in Counter(p.ids).items() if n>1],
       'html_missing_fragments':[v for v in p.refs if v.startswith('#') and v!='#' and unquote(v[1:]) not in p.ids],
       'html_missing_assets':[v for v in p.assets if absent(v)],
       'unresolved_html_markers':'?@' in html or 'quarto-unresolved-ref' in html,
       'even_math_delimiters':len(re.findall(r'^\$\$\s*$',expanded,re.M))%2==0,
       'math_spans':len(p.math),
    }
    for key,val in r.items():
        if key in ['rendered_source_matches_live','rendered_html_matches_work','rendered_pdf_matches_work','even_math_delimiters']:
            if not val: errors.append([name,key,val])
        elif key!='math_spans' and val: errors.append([name,key,val])
    results[name]=r; math[name]=p.math
(OUT/'artifact-checks.json').write_text(json.dumps({'results':results,'errors':errors},ensure_ascii=False,indent=2)+'\n')
(OUT/'html-math.json').write_text(json.dumps(math,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'documents':len(results),'math_spans':sum(r['math_spans'] for r in results.values()),'errors':errors},ensure_ascii=False,indent=2))
if errors: sys.exit(1)
