"""Rebuild only the five lectures changed by the September 9 rereview fixes."""
from pathlib import Path
import json
import os
import subprocess
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
env = os.environ.copy()
env['TEXMFVAR'] = '/tmp/gradmacro-review-20260908-8d5laqlu/audit/texmf-var'
env['TEXMFCACHE'] = env['TEXMFVAR']
results = []
for name in ['lecture03', 'lecture05', 'lecture10', 'lecture11', 'lecture12']:
    command = ['Rscript', '--vanilla', 'scripts/render-lecture.R', name + '.qmd',
               '--to', 'all', '-M', 'latex-auto-install:false']
    print('Rendering ' + name, flush=True)
    start = time.monotonic()
    with (OUT / (name + '-render.log')).open('w') as log:
        process = subprocess.run(command, cwd=ROOT, env=env, stdout=log,
                                 stderr=subprocess.STDOUT)
    result = dict(document=name, exit_code=process.returncode, command=command,
                  seconds=round(time.monotonic() - start, 2), TEXMFVAR=env['TEXMFVAR'])
    results.append(result)
    (OUT / 'render-status.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(result), flush=True)
    if process.returncode:
        print((OUT / (name + '-render.log')).read_text()[-7000:])
        raise SystemExit(process.returncode)
