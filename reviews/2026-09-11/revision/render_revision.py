"""Render the revised live inputs to an isolated workspace; promote after QA."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, json, os, shutil, subprocess, sys, tempfile, time

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
NAMES = [f'lecture{i:02d}' for i in range(1,13)]+['solution']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
state=OUT/'render-state.json'
if state.exists(): work=Path(json.loads(state.read_text())['work'])
else:
    work=Path(tempfile.mkdtemp(prefix='gradmacro-fixed-20260911-'))
    state.write_text(json.dumps({'work':str(work)},indent=2)+'\n')
for p in ROOT.glob('*.qmd'): shutil.copy2(p,work/p.name)
for folder in ['includes','figures','data','scripts']:
    shutil.copytree(ROOT/folder,work/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.R-library','__pycache__'))
if (ROOT/'scripts/.R-library').exists() and not (work/'scripts/.R-library').exists():
    (work/'scripts/.R-library').symlink_to(ROOT/'scripts/.R-library',target_is_directory=True)
for folder in ['pdf','html','logs','tex']: (OUT/folder).mkdir(exist_ok=True)
result_path=OUT/'render-results.json'
results=json.loads(result_path.read_text()) if result_path.exists() else {}

def render(name):
    cache=work/('cache-'+name); (cache/'texmf').mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    env.update(TEXMFVAR=str(cache/'texmf'),TEXMFCACHE=str(cache/'texmf'),QUARTO_CACHE_DIR=str(cache/'quarto'),XDG_CACHE_HOME=str(cache/'xdg'))
    command=['Rscript','--vanilla','scripts/render-lecture.R',name+'.qmd','--to','all','-M','latex-auto-install:false','-M','keep-tex:true','-M','latex-clean:false']
    started=time.time(); print('START '+name,flush=True)
    with (OUT/'logs'/(name+'-render.log')).open('w') as log:
        proc=subprocess.run(command,cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
    result={'returncode':proc.returncode,'seconds':round(time.time()-started,2),'command':command,'source_sha256':sha(work/(name+'.qmd')),'outputs':{}}
    if proc.returncode==0:
        for ext in ['pdf','html']:
            target=OUT/ext/(name+'.'+ext); shutil.copy2(work/(name+'.'+ext),target)
            result['outputs'][ext]={'sha256':sha(target),'bytes':target.stat().st_size}
    for ext in ['tex','log']:
        p=work/(name+'.'+ext)
        if p.exists(): shutil.copy2(p,OUT/('tex' if ext=='tex' else 'logs')/p.name)
    print(f'END {name} status={proc.returncode} seconds={result["seconds"]}',flush=True)
    return name,result

names=sys.argv[1:] or NAMES
with ThreadPoolExecutor(max_workers=3) as pool:
    for f in as_completed([pool.submit(render,n) for n in names]):
        name,result=f.result(); results[name]=result
        result_path.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
if any(results[n]['returncode'] for n in names): sys.exit(1)
