"""Verify the reference revision against sources, rendered artifacts, and backups."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import hashlib
import json
import re
import subprocess
import unicodedata
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
NAMES = [f"lecture{i:02d}" for i in range(1, 13)] + ["マクロ経済学B_シラバス案"]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm(value):
    return ''.join(c.lower() for c in unicodedata.normalize('NFKD', value) if c.isalnum())

def plain(value):
    return re.sub(r'\[([^\]]+)\]\((https?://[^\s]+)\)', r'\1', value).replace('*', '').replace('`', '')

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets, self.entries = [], [], [], []
        self.refdepth = 0
        self.item = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag in ('img', 'script') and 'src' in a: self.assets.append(a['src'])
        if tag == 'link' and 'href' in a: self.assets.append(a['href'])
        if tag == 'section':
            if a.get('id') in ('参考文献', '教材基本参考文献'): self.refdepth = 1
            elif self.refdepth: self.refdepth += 1
        if tag == 'li' and self.refdepth: self.item = []
    def handle_endtag(self, tag):
        if tag == 'li' and self.item is not None:
            self.entries.append(''.join(self.item)); self.item = None
        if tag == 'section' and self.refdepth: self.refdepth -= 1
    def handle_data(self, data):
        if self.item is not None: self.item.append(data)

pages = {}
for name in NAMES:
    page = Page(); page.feed((ROOT / f'{name}.html').read_text()); pages[name] = page

renders = json.loads((OUT / 'render-results.json').read_text())['results']
results = {}
for name in NAMES:
    source_path = ROOT / f'{name}.qmd'
    source = source_path.read_text()
    old = (OUT / 'source-before' / f'{name}.qmd').read_text()
    p = pages[name]
    section = re.search(r'^#+ (?:参考文献|教材・基本参考文献)\s*\n(.*?)(?=^#+ |\Z)', source, re.M | re.S).group(1)
    entries = re.findall(r'^- (.+)$', section, re.M)
    urls = re.findall(r'\]\((https?://[^\s]+)\)', section)
    pdf = PdfReader(ROOT / f'{name}.pdf')
    pdf_urls = [str(a.get_object().get('/A', {}).get('/URI')) for page in pdf.pages for a in page.get('/Annots', []) if a.get_object().get('/A', {}).get('/URI')]
    text = subprocess.check_output(['pdftotext', '-layout', str(ROOT / f'{name}.pdf'), '-'], text=True)
    (OUT / f'{name}-text.txt').write_text(text)
    titles = []
    for entry in entries:
        match = re.search(r'"([^"]+)"|\*([^*]+)\*|『([^』]+)』', plain(entry) if '*' not in entry else entry)
        if match: titles.append(next(x for x in match.groups() if x is not None))
    missing_local = []
    missing_fragments = []
    for url in p.links + p.assets:
        u = urlsplit(url)
        if u.scheme or u.netloc: continue
        target = ROOT / unquote(u.path) if u.path else ROOT / f'{name}.html'
        if not target.exists(): missing_local.append(url); continue
        if u.fragment and target.suffix == '.html':
            target_page = pages.get(target.stem)
            if target_page is None:
                target_page = Page(); target_page.feed(target.read_text())
            if unquote(u.fragment) not in target_page.ids: missing_fragments.append(url)
    code = lambda s: [(tag, body) for tag,body in re.findall(r'^```([^\n]*)\n(.*?)^```\s*$', s, re.M | re.S) if tag != '{=latex}']
    display = lambda s: re.findall(r'^\$\$\s*\n(.*?)^\$\$\s*$', s, re.M | re.S)
    inline = lambda s: re.findall(r'(?<!\$)\$(?!\$)([^$\n]+)\$(?!\$)', s)
    suffix = lambda s: s.split('# 演習問題', 1)[1] if '# 演習問題' in s else None
    render = renders[name]
    html = (ROOT / f'{name}.html').read_text()
    results[name] = {
        'reference_entries': len(entries), 'html_reference_entries': len(p.entries),
        'reference_text_mismatches': [i + 1 for i, (a,b) in enumerate(zip(entries,p.entries)) if norm(plain(a)) != norm(b)],
        'reference_counts_match': len(entries) == len(p.entries),
        'missing_html_reference_urls': [x for x in urls if x not in p.links],
        'missing_pdf_reference_urls': [x for x in urls if unquote(x) not in [unquote(y) for y in pdf_urls]],
        'pdf_titles_checked': len(titles), 'pdf_missing_titles': [x for x in titles if norm(plain(x)) not in norm(text)],
        'pages': len(pdf.pages), 'pdf_replacement_glyphs': text.count('\ufffd'), 'pdf_unresolved_refs': text.count('??'),
        'missing_local_links_or_assets': missing_local, 'missing_fragments': missing_fragments,
        'duplicate_ids': [x for x,n in Counter(p.ids).items() if n > 1],
        'unresolved_html_refs': '?@' in html or 'quarto-unresolved-ref' in html,
        'display_math_unchanged': display(source) == display(old), 'display_equations': len(display(source)),
        'inline_math_unchanged': inline(source) == inline(old), 'code_blocks_unchanged': code(source) == code(old),
        'exercises_and_appendices_unchanged': suffix(source) == suffix(old),
        'render_succeeded': render['returncode'] == 0,
        'render_source_current': render['source_before_sha256'] == render['source_sha256'] == sha(source_path),
        'render_outputs_current': all(render['outputs'][ext]['sha256'] == sha(ROOT / f'{name}.{ext}') for ext in ('html','pdf')),
    }
protected = json.loads((OUT / 'protected-before.json').read_text())
changed = [p for p,h in protected.items() if not (ROOT / p).exists() or sha(ROOT / p) != h]
syllabus = (ROOT / 'マクロ経済学B_シラバス案.qmd').read_text().split('---', 2)[2].lstrip('\n')
md = (ROOT / 'マクロ経済学B_シラバス案.md').read_text()
summary = {'results': results, 'protected_files': len(protected), 'protected_changed': changed,
           'syllabus_md_synchronized': md == '# マクロ経済学B シラバス案\n\n' + syllabus}
required_true = ('reference_counts_match', 'display_math_unchanged', 'inline_math_unchanged',
                 'code_blocks_unchanged', 'exercises_and_appendices_unchanged',
                 'render_succeeded', 'render_source_current', 'render_outputs_current')
summary['passed'] = (not changed and summary['syllabus_md_synchronized'] and
    all(all(r[k] for k in required_true) and not r['unresolved_html_refs'] and
        not r['pdf_replacement_glyphs'] and not r['pdf_unresolved_refs'] and
        not any(v for v in r.values() if isinstance(v, list)) for r in results.values()))
summary['total_reference_entries'] = sum(r['reference_entries'] for r in results.values())
summary['total_display_equations'] = sum(r['display_equations'] for r in results.values())
(OUT / 'verification.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(summary, ensure_ascii=False, indent=2))
raise SystemExit(0 if summary['passed'] else 1)
