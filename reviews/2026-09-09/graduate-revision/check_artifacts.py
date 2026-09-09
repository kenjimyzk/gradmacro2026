"""Read-only audit of current course sources and saved HTML/PDF artifacts."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import hashlib, json, re, subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
NAMES = [f'lecture{i:02d}' for i in range(1, 13)] + ['solution']

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets, self.math = [], [], [], []
        self.depth = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag in ('img', 'script') and 'src' in a: self.assets.append(a['src'])
        if tag == 'link' and 'href' in a: self.assets.append(a['href'])
        if tag == 'span' and 'math' in a.get('class', '').split():
            self.depth = 1
            self.parts = []
        elif self.depth and tag == 'span': self.depth += 1
    def handle_endtag(self, tag):
        if tag == 'span' and self.depth:
            self.depth -= 1
            if not self.depth: self.math.append(''.join(self.parts))
    def handle_data(self, data):
        if self.depth: self.parts.append(data)

def absent(url):
    u = urlsplit(url)
    return not (u.scheme or u.netloc) and bool(u.path) and not (ROOT / unquote(u.path)).exists()

protected = [p for pattern in ('*.qmd', '*.html', '*.pdf', 'includes/*.qmd', 'scripts/**/*.R', 'scripts/**/*.py', 'figures/**/*', 'data/**/*') for p in ROOT.glob(pattern) if p.is_file()]
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
(OUT / 'protected-sha256.json').write_text(json.dumps(manifest, indent=2) + '\n')
results, math = {}, {}
for name in NAMES:
    source = (ROOT / f'{name}.qmd').read_text()
    html = (ROOT / f'{name}.html').read_text()
    p = Parser(); p.feed(html)
    text = subprocess.check_output(['pdftotext', '-layout', str(ROOT / f'{name}.pdf'), '-'], text=True)
    (OUT / f'{name}-text.txt').write_text(text)
    pages = [x for x in text.split('\f') if x.strip()]
    anchors = {phrase: [i + 1 for i, x in enumerate(pages) if phrase in re.sub(r'\s+', '', x)] for phrase in ('演習問題', '基本問題', '補論（発展）', '基本参考文献', '全講義共通')}
    results[name] = {
        'pages': len(pages), 'pdf_replacement_glyphs': text.count('\ufffd'),
        'pdf_unresolved_refs': text.count('??'),
        'missing_assets': [x for x in p.assets if absent(x)],
        'missing_links': [x for x in p.links if absent(x)],
        'missing_fragments': [x for x in p.links if x.startswith('#') and x != '#' and unquote(x[1:]) not in p.ids],
        'duplicate_ids': [x for x, n in Counter(p.ids).items() if n > 1],
        'unresolved_html_refs': '?@' in html or 'quarto-unresolved-ref' in html,
        'math_spans': len(p.math),
        'display_math_delimiters_even': len(re.findall(r'^\$\$\s*$', source, re.M)) % 2 == 0,
        'anchors': anchors,
    }
    math[name] = p.math
(OUT / 'artifact-checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
(OUT / 'html-math.json').write_text(json.dumps(math, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(results, ensure_ascii=False, indent=2))
