"""Check final document contents, local HTML assets, and TeX diagnostics."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from pypdf import PdfReader
import hashlib, json, re
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
WORK=Path(json.loads((OUT/'render-state.json').read_text())['work'])
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.ids=set(); self.math=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d: self.ids.add(d['id'])
        if tag in ['img','script','link']:
            url=d.get('src') or d.get('href')
            if url: self.refs.append(url)
        if tag=='span' and 'math' in d.get('class','').split(): self.math+=1
results={}
for name in ['lecture02','solution']:
    src=ROOT/(name+'.qmd')
    assert src.read_bytes()==(WORK/src.name).read_bytes(), 'source changed after rendering'
    html=(WORK/(name+'.html')).read_text()
    parser=Links(); parser.feed(html)
    missing=[]
    for ref in parser.refs:
        u=urlsplit(ref)
        if not u.scheme and u.path and not (WORK/unquote(u.path)).exists(): missing.append(ref)
    assert not missing, missing
    assert parser.math>0
    assert 'AR(1)ショックと前向き方程式' in html
    assert 'quarto-unresolved-ref' not in html
    reader=PdfReader(WORK/(name+'.pdf'))
    pages=[p.extract_text() or '' for p in reader.pages]
    (OUT/(name+'-text.txt')).write_text('\n\n'.join(f'PAGE {i+1}\n{p}' for i,p in enumerate(pages)))
    if name=='lecture02':
        for term in ['状態空間','状態遷移','固有値','Blanchard','A^hB']:
            assert term not in html and term not in ''.join(pages), term
    log=(WORK/(name+'.log')).read_text(errors='replace')
    material=[line for line in log.splitlines() if re.search(r'Overfull|Missing character|undefined',line)]
    assert not material, material
    needles=['第2回の地図','1変数の線形差分','前向き変数と期待','無バブル条件','初読時に押さえる','AR(1)ショックと前向き方程式','問7[']
    locations={}
    for needle in needles:
        locations[needle]=[i+1 for i,p in enumerate(pages) if needle in p.replace(' ','')]
    results[name]={'pages':len(pages),'local_html_assets_checked':len(parser.refs),
                   'math_spans':parser.math,'material_tex_warnings':material,'locations':locations,
                   'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
(OUT/'output-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
