from pathlib import Path
import hashlib, json, os, subprocess, tempfile, time, sys
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
names=sys.argv[1:] or ['lecture10','solution']
cache=Path(tempfile.mkdtemp(prefix='gradmacro-revision-20260909-'))
env=os.environ.copy()
env.update(TEXMFVAR=str(cache/'texmf-var'),TEXMFCACHE=str(cache/'texmf-var'))
(cache/'texmf-var').mkdir()
results=json.loads((OUT/'render-results.json').read_text())['results'] if sys.argv[1:] and (OUT/'render-results.json').exists() else {}
for name in names:
    cmd=['Rscript','--vanilla','scripts/render-lecture.R',f'{name}.qmd','--to','all','-M','latex-auto-install:false']
    print(f'START {name}',flush=True)
    start=time.time()
    before_hash=hashlib.sha256((ROOT/f'{name}.qmd').read_bytes()).hexdigest()
    with (OUT/f'{name}-render.log').open('w') as f:
        p=subprocess.run(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
    results[name]={'command':cmd,'returncode':p.returncode,'seconds':round(time.time()-start,2),'source_before_sha256':before_hash,'source_sha256':hashlib.sha256((ROOT/f'{name}.qmd').read_bytes()).hexdigest(),'outputs':{ext:{'bytes':(ROOT/f'{name}.{ext}').stat().st_size,'sha256':hashlib.sha256((ROOT/f'{name}.{ext}').read_bytes()).hexdigest()} for ext in ['html','pdf'] if (ROOT/f'{name}.{ext}').exists()}}
    (OUT/'render-results.json').write_text(json.dumps({'cache':str(cache),'results':results},indent=2)+'\n')
    print(f'END {name} status={p.returncode} {results[name]["seconds"]}s',flush=True)
    if p.returncode:
        print((OUT/f'{name}-render.log').read_text()[-4000:],flush=True)
        raise SystemExit(p.returncode)
