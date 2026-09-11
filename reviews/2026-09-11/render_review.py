"""Render unmodified source snapshots, retaining PDF/TeX evidence for this review."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, json, os, shutil, subprocess, sys, tempfile, time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
NAMES = [f'lecture{i:02d}' for i in range(1, 13)] + ['solution']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

state = OUT / 'render-state.json'
if state.exists():
    work = Path(json.loads(state.read_text())['work'])
else:
    work = Path(tempfile.mkdtemp(prefix='gradmacro-review-20260911-'))
    for p in ROOT.glob('*.qmd'): shutil.copy2(p, work / p.name)
    for folder in ['includes', 'figures', 'data', 'scripts']:
        shutil.copytree(ROOT / folder, work / folder, ignore=shutil.ignore_patterns('.R-library', '__pycache__'))
    if (ROOT / 'scripts/.R-library').exists():
        (work / 'scripts/.R-library').symlink_to(ROOT / 'scripts/.R-library', target_is_directory=True)
    protected = [p for pat in ['*.qmd', 'includes/*.qmd', 'scripts/**/*.R', 'scripts/**/*.py', 'figures/**/*', 'data/**/*'] for p in ROOT.glob(pat) if p.is_file() and '.R-library' not in str(p)]
    (OUT / 'source-before-sha256.json').write_text(json.dumps({str(p.relative_to(ROOT)): sha(p) for p in protected}, indent=2)+'\n')
    state.write_text(json.dumps({'work': str(work)}, indent=2)+'\n')

for folder in ['pdf', 'logs', 'tex']: (OUT / folder).mkdir(exist_ok=True)
result_path = OUT / 'render-results.json'
results = json.loads(result_path.read_text()) if result_path.exists() else {}

def render(name):
    cache = work / ('cache-' + name)
    (cache / 'texmf').mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(TEXMFVAR=str(cache/'texmf'), TEXMFCACHE=str(cache/'texmf'), QUARTO_CACHE_DIR=str(cache/'quarto'), XDG_CACHE_HOME=str(cache/'xdg'))
    cmd = ['Rscript', '--vanilla', 'scripts/render-lecture.R', name+'.qmd', '--to', 'pdf', '-M', 'latex-auto-install:false', '-M', 'keep-tex:true', '-M', 'latex-clean:false']
    start = time.time()
    print('START '+name, flush=True)
    with (OUT/'logs'/f'{name}-render.log').open('w') as log:
        proc = subprocess.run(cmd, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT)
    result = {'returncode': proc.returncode, 'seconds': round(time.time()-start,2), 'command': cmd, 'source_sha256': sha(work/(name+'.qmd'))}
    if proc.returncode == 0:
        shutil.copy2(work/(name+'.pdf'), OUT/'pdf'/(name+'.pdf'))
        result['pdf_sha256'] = sha(OUT/'pdf'/(name+'.pdf'))
    for ext in ['tex', 'log']:
        p = work/(name+'.'+ext)
        if p.exists(): shutil.copy2(p, OUT/('tex' if ext=='tex' else 'logs')/p.name)
    print(f'END {name} status={proc.returncode} seconds={result["seconds"]}', flush=True)
    return name, result

names = sys.argv[1:] or NAMES
with ThreadPoolExecutor(max_workers=3) as pool:
    for future in as_completed([pool.submit(render, name) for name in names]):
        name, result = future.result()
        results[name] = result
        result_path.write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
if any(results[name]['returncode'] for name in names): sys.exit(1)
