"""Inspect PDF text/bounds and rasterize every page for human visual review."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw
import pdfplumber
import hashlib, json, re, subprocess, sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
names = sys.argv[1:] or [f'lecture{i:02d}' for i in range(1,13)] + ['solution']
result_path = OUT/'pdf-checks.json'
results = json.loads(result_path.read_text()) if result_path.exists() else {}

def check(name):
    path = OUT/'pdf'/(name+'.pdf')
    dest = OUT/'visual'/name
    dest.mkdir(parents=True, exist_ok=True)
    for pattern in ['page-*.png', 'contact-*.jpg']:
        for old in dest.glob(pattern): old.unlink()
    text = subprocess.check_output(['pdftotext','-layout',str(path),'-'],text=True)
    (dest/'text.txt').write_text(text)
    log = (OUT/'logs'/(name+'.log')).read_text(errors='replace')
    box_messages = re.findall(r'(?:Overfull|Underfull)[\s\S]*?(?=\n\n)',log)
    bad = []
    metrics = []
    with pdfplumber.open(path) as doc:
        for page in doc.pages:
            chars = [c for c in page.chars if c['text'].strip()]
            outside = [c for c in chars if c['x0']<0 or c['x1']>page.width+0.1 or c['top']<0 or c['bottom']>page.height+0.1]
            near = [c for c in chars if c['x0']<35 or c['x1']>page.width-35 or c['top']<25 or c['bottom']>page.height-25]
            m = {'page':page.page_number,'chars':len(chars),'width':page.width,'height':page.height,
                 'outside_page':' '.join(c['text'] for c in outside),
                 'near_edge':' '.join(c['text'] for c in near)}
            if chars: m['bounds']=[round(min(c['x0'] for c in chars),2),round(min(c['top'] for c in chars),2),round(max(c['x1'] for c in chars),2),round(max(c['bottom'] for c in chars),2)]
            metrics.append(m)
            if outside or near or len(chars)<80: bad.append(m)
    subprocess.run(['pdftoppm','-scale-to','800','-png',str(path),str(dest/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    pages = sorted(dest.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1]))
    contacts=[]
    for start in range(0,len(pages),6):
        subset=pages[start:start+6]
        sheet=Image.new('RGB',(1160,850*((len(subset)+1)//2)),'#dddddd')
        draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(subset):
            im=Image.open(p).convert('RGB')
            x=(i%2)*580; y=(i//2)*850
            sheet.paste(im,(x+(580-im.width)//2,y+30))
            draw.text((x+12,y+8),f'{name} PDF page {start+i+1}',fill='black')
        target=dest/f'contact-{start+1:03d}-{start+len(subset):03d}.jpg'
        sheet.save(target,quality=91)
        contacts.append(str(target.relative_to(OUT)))
    result={'pages':len(pages),'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'replacement_glyphs':text.count('\ufffd'),'unresolved_refs':text.count('??'),
            'missing_character_lines':[x for x in log.splitlines() if 'Missing character:' in x],
            'box_messages':box_messages,'flagged_pages':bad,'page_metrics':metrics,'contacts':contacts,
            'visual_status':'prepared, awaiting inspection'}
    print(name,json.dumps({k:result[k] for k in ['pages','replacement_glyphs','unresolved_refs','missing_character_lines','box_messages','flagged_pages']},ensure_ascii=False),flush=True)
    return name,result

with ThreadPoolExecutor(max_workers=3) as pool:
    for f in as_completed([pool.submit(check,n) for n in names]):
        name,result=f.result(); results[name]=result
        result_path.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
