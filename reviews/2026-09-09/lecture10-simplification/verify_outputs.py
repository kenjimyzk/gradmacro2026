#!/usr/bin/env python3
"""Static checks for the four documents rebuilt after simplifying Lectures 01 and 10; no browser is used."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from collections import Counter
import hashlib
import json
import re
import shutil
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
NAMES = ['lecture01', 'lecture09', 'lecture10', 'solution']


class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.assets = [], [], []
        self.math = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and 'href' in a:
            self.refs.append(a['href'])
        if tag in ['img', 'script'] and 'src' in a:
            self.assets.append(a['src'])
        if tag == 'link' and 'href' in a:
            self.assets.append(a['href'])
        self.math += 'math' in a.get('class', '').split()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def absent_local(url):
    u = urlsplit(url)
    return not (u.scheme or u.netloc) and bool(u.path) and not (ROOT / unquote(u.path)).exists()


html_results, pdf_results, sources = {}, {}, {}
for name in NAMES:
    h = ROOT / (name + '.html')
    s = h.read_text()
    parser = Audit()
    parser.feed(s)
    checks = {
        'math_spans': parser.math,
        'missing_local_assets': [x for x in parser.assets if absent_local(x)],
        'missing_local_links': [x for x in parser.refs if absent_local(x)],
        'missing_fragment_targets': [x for x in parser.refs if x.startswith('#') and x != '#' and unquote(x[1:]) not in parser.ids],
        'duplicate_ids': [x for x, n in Counter(parser.ids).items() if n > 1],
        'unresolved_crossref_markers': '?@' in s or 'quarto-unresolved-ref' in s,
        'html_sha256': sha(h),
        'browser_layout': 'not run in this revision; static checks do not establish browser layout',
    }
    for key in ['missing_local_assets', 'missing_local_links', 'missing_fragment_targets', 'duplicate_ids', 'unresolved_crossref_markers']:
        assert not checks[key], (name, key, checks[key])
    html_results[name] = checks
    pdf = ROOT / (name + '.pdf')
    text = subprocess.check_output([shutil.which('pdftotext'), '-layout', str(pdf), '-'], text=True)
    (OUT / (name + '-text.txt')).write_text(text)
    pdf_results[name] = {
        'pages': len([p for p in text.split('\f') if p.strip()]),
        'replacement_glyphs': text.count('\ufffd'),
        'unresolved_references': text.count('??'),
        'pdf_sha256': sha(pdf),
    }
    assert not (pdf_results[name]['replacement_glyphs'] or pdf_results[name]['unresolved_references'])
    source = ROOT / (name + '.qmd')
    q = source.read_text()
    # Include the actual dependent notation source for lecture01.
    if name == 'lecture01':
        q += '\n' + (ROOT / 'includes/notation-concordance.qmd').read_text()
    sources[name] = {
        'display_delimiters_even': len(re.findall(r'^\$\$(?:[ \t]*\{[^\n]*\})?[ \t]*$', q, re.M)) % 2 == 0,
        'source_sha256': sha(source),
    }
    assert sources[name]['display_delimiters_even'], name

for filename, data in [('html-static-verification.json', html_results), ('pdf-text-verification.json', pdf_results), ('source-verification.json', sources)]:
    (OUT / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Verified static HTML references/assets, PDF text, and display-math delimiters for four rebuilt documents.')
