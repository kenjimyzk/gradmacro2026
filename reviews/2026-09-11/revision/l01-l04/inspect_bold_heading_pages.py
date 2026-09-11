"""Locate all standalone bold headings in rendered L01 and rasterize their pages."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REVISION = HERE.parent
ROOT = HERE.parents[3]
PDF = REVISION / 'pdf' / 'lecture01.pdf'
DEST = HERE / 'expanded-final-headings'
DEST.mkdir(exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm(s):
    return re.sub(r'\s', '', s).replace('（', '(').replace('）', ')').replace('：', ':')

source = (ROOT / 'lecture01.qmd').read_text()
headings = re.findall(r'^\*\*([^\n]+)\*\*$', source, flags=re.M)
lookup = {norm(heading) for heading in headings}
text = subprocess.check_output(['pdftotext', '-layout', str(PDF), '-']).decode()
rows = []
for page_number, page in enumerate(text.split('\f'), 1):
    lines = page.splitlines()
    for i, line in enumerate(lines):
        if norm(line) in lookup:
            following = [x.strip() for x in lines[i+1:] if x.strip()]
            rows.append({'page': page_number, 'heading': line.strip(), 'following_lines': following[:3]})
assert len(rows) == len(headings) == 33
assert all(r['following_lines'] and r['following_lines'][0] != str(r['page']) for r in rows)
pages = sorted({r['page'] for r in rows})
changed = []
for page in pages:
    image = DEST / f'page{page:02}.png'
    previous_sha = sha(image) if image.exists() else None
    subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', '100', '-png', '-singlefile',
                    str(PDF), str(image.with_suffix(''))], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if previous_sha != sha(image):
        changed.append(page)
result = {'pdf_sha256': sha(PDF), 'source_sha256': sha(ROOT / 'lecture01.qmd'),
          'headings': len(rows), 'heading_pages': pages,
          'pages_changed_since_previous_images': changed,
          'all_headings_have_following_text_on_same_page': True,
          'visual_status': 'requires human viewing of changed page images', 'rows': rows}
(HERE / 'bold_heading_pdf_locations.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, ensure_ascii=False, indent=2))
