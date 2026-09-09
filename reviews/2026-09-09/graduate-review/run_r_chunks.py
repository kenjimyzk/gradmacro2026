"""Execute current R chunks in isolated vanilla processes, writing audit output only."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, re, subprocess
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
def run(name):
    source = (ROOT / f'{name}.qmd').read_text()
    chunks = re.findall(r'^```\{r[^\n]*\}\n(.*?)^```\s*$', source, re.M | re.S)
    script = 'source("scripts/japanese-graphics.R")\ninfo <- course_japanese_graphics()\n'
    script += f'grDevices::cairo_pdf({json.dumps(str(OUT / (name + "-r.pdf")))}, width=8, height=4.8, family=info$family)\n'
    script += '\n\n'.join(chunks)
    script += '\ngrDevices::dev.off()\nprint(sessionInfo())\n'
    path = OUT / f'{name}-chunks.R'; path.write_text(script)
    p = subprocess.run(['Rscript','--vanilla',str(path)], cwd=ROOT, text=True, capture_output=True)
    (OUT / f'{name}-r.log').write_text(p.stdout + p.stderr)
    return name, {'chunks':len(chunks),'exit_code':p.returncode,'log':str((OUT / f'{name}-r.log').relative_to(ROOT)),'warnings':'Warning' in p.stderr or '警告' in p.stderr}
with ThreadPoolExecutor(max_workers=3) as pool:
    results=dict(pool.map(run,['lecture05','lecture08','lecture09']))
(OUT/'r-execution.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
