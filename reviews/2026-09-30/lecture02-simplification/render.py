"""Render the two revised sources in isolation for layout QA."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, os, shutil, subprocess, tempfile, time, sys
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
state = OUT / "render-state.json"
WORK = Path(json.loads(state.read_text())["work"]) if state.exists() else Path(tempfile.mkdtemp(prefix="gradmacro-lecture02-20260930-"))
NAMES = sys.argv[1:] or ["lecture02", "solution"]
assert set(NAMES) <= {"lecture02", "solution"}
for name in NAMES:
    shutil.copy2(ROOT / (name + ".qmd"), WORK / (name + ".qmd"))
for directory in ["figures", "includes"]:
    if (ROOT / directory).exists():
        shutil.copytree(ROOT / directory, WORK / directory, dirs_exist_ok=True)
shutil.copytree(ROOT / "scripts", WORK / "scripts", dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(".R-library", "__pycache__"))
if (ROOT / "scripts/.R-library").exists() and not (WORK / "scripts/.R-library").exists():
    (WORK / "scripts/.R-library").symlink_to(ROOT / "scripts/.R-library", target_is_directory=True)
(OUT / "render-state.json").write_text(json.dumps({"work": str(WORK)}, indent=2) + "\n")
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def render(name):
    cache = WORK / ("cache-" + name)
    (cache / "texmf").mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(TEXMFVAR=str(cache / "texmf"), TEXMFCACHE=str(cache / "texmf"),
               QUARTO_CACHE_DIR=str(cache / "quarto"), XDG_CACHE_HOME=str(cache / "xdg"))
    cmd = ["Rscript", "--vanilla", "scripts/render-lecture.R", name + ".qmd",
           "--to", "all", "-M", "latex-auto-install:false", "-M", "keep-tex:true",
           "-M", "latex-clean:false"]
    start = time.monotonic()
    print("START " + name, flush=True)
    with (OUT / (name + "-render.log")).open("w") as log:
        result = subprocess.run(cmd, cwd=WORK, env=env, stdout=log, stderr=subprocess.STDOUT)
    record = {"returncode": result.returncode, "seconds": round(time.monotonic()-start, 2),
              "command": cmd, "source_sha256": sha(WORK / (name + ".qmd")), "outputs": {}}
    if result.returncode == 0:
        for ext in ["html", "pdf"]:
            path = WORK / (name + "." + ext)
            record["outputs"][ext] = {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}
    print("END " + name + " " + str(record["returncode"]), flush=True)
    return name, record
results_path = OUT / "render-results.json"
records = json.loads(results_path.read_text()) if results_path.exists() else {}
with ThreadPoolExecutor(max_workers=2) as pool:
    records.update(dict(pool.map(render, NAMES)))
(OUT / "render-results.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(records, ensure_ascii=False, indent=2))
if any(record["returncode"] for record in records.values()):
    raise SystemExit(1)
