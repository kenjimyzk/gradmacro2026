"""Render the authorized reference revisions and retain per-document evidence."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
names = sys.argv[1:] or [f"lecture{i:02d}" for i in range(1, 13)] + ["マクロ経済学B_シラバス案"]
cache = Path(tempfile.mkdtemp(prefix="gradmacro-references-20260909-"))
env = os.environ.copy()
env.update(TEXMFVAR=str(cache / "texmf-var"), TEXMFCACHE=str(cache / "texmf-var"))
(cache / "texmf-var").mkdir()
result_path = OUT / "render-results.json"
results = json.loads(result_path.read_text())["results"] if result_path.exists() else {}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for name in names:
    command = ["Rscript", "--vanilla", "scripts/render-lecture.R", f"{name}.qmd", "--to", "all", "-M", "latex-auto-install:false"]
    print(f"START {name}", flush=True)
    started = time.time()
    source_before = sha(ROOT / f"{name}.qmd")
    with (OUT / f"{name}-render.log").open("w") as log:
        process = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    results[name] = {
        "command": command, "returncode": process.returncode,
        "seconds": round(time.time() - started, 2),
        "source_before_sha256": source_before,
        "source_sha256": sha(ROOT / f"{name}.qmd"),
        "outputs": {ext: {"bytes": (ROOT / f"{name}.{ext}").stat().st_size,
                          "sha256": sha(ROOT / f"{name}.{ext}")}
                    for ext in ("html", "pdf") if (ROOT / f"{name}.{ext}").exists()},
    }
    result_path.write_text(json.dumps({"cache": str(cache), "results": results}, ensure_ascii=False, indent=2) + "\n")
    print(f"END {name} status={process.returncode} {results[name]['seconds']}s", flush=True)
    if process.returncode:
        print((OUT / f"{name}-render.log").read_text()[-4000:], flush=True)
        raise SystemExit(process.returncode)
