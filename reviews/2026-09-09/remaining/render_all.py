#!/usr/bin/env python3
"""Render the six documents affected by the remaining review fixes."""
from pathlib import Path
import subprocess, os, json, time, sys
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
env=os.environ.copy()
env['TEXMFVAR']='/tmp/gradmacro-review-20260908-8d5laqlu/audit/texmf-var'
env['TEXMFCACHE']=env['TEXMFVAR']
names=sys.argv[1:] or ['lecture01','lecture03','lecture05','lecture07','lecture09','solution']
assert all(name in ['lecture01','lecture03','lecture05','lecture07','lecture09','solution'] for name in names)
status_path=out/'render-status.json'
results=json.loads(status_path.read_text()) if status_path.exists() else []
for name in names:
    start=time.time()
    cmd=['/usr/local/bin/quarto','render',name+'.qmd','--to','all','-M','latex-auto-install:false']
    print('Rendering '+name,flush=True)
    with (out/(name+'-render.log')).open('a') as log:
        proc=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
    results.append(dict(document=name,exit_code=proc.returncode,seconds=round(time.time()-start,2),command=cmd))
    (out/'render-status.json').write_text(json.dumps(results,indent=2)+'\n')
    print(name+' exit='+str(proc.returncode),flush=True)
    if proc.returncode: raise SystemExit(proc.returncode)
