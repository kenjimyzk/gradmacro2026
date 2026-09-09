"""Rasterize selected current PDF pages for a sampled visual review."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
import json, subprocess
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
selected = {'lecture01': [5,27], 'lecture02': [4,22], 'lecture03': [24],
 'lecture04': [5], 'lecture05': [18], 'lecture06': [8], 'lecture07': [12],
 'lecture08': [17], 'lecture09': [5,22], 'lecture10': [24,25],
 'lecture11': [22], 'lecture12': [23,36,40], 'solution': [29]}
jobs = [(name, p) for name, pages in selected.items() for p in pages]
def render(job):
 name, p = job
 prefix = OUT / f'{name}-p{p:02d}'
 subprocess.run(['pdftoppm','-f',str(p),'-l',str(p),'-singlefile','-r','100','-png',str(ROOT / f'{name}.pdf'),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 return prefix.with_suffix('.png')
with ThreadPoolExecutor(max_workers=4) as pool: paths=list(pool.map(render,jobs))
for start in range(0,len(paths),4):
 subset=paths[start:start+4]
 canvas=Image.new('RGB',(1100,820*((len(subset)+1)//2)),'#dddddd')
 d=ImageDraw.Draw(canvas)
 for i,path in enumerate(subset):
  img=Image.open(path).convert('RGB'); img.thumbnail((540,780))
  x=(i%2)*550; y=(i//2)*820
  canvas.paste(img,(x+(550-img.width)//2,y+30))
  d.text((x+12,y+8),path.stem,fill='black')
 canvas.save(OUT/f'contact-{start//4+1}.jpg',quality=90)
(OUT/'visual-pages.json').write_text(json.dumps(selected,indent=2)+'\n')
print(f'Prepared {len(paths)} pages from {len(selected)} PDFs; not a full visual audit.')
