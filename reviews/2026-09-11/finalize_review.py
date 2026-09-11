"""Verify the finished review, its links, preserved sources and rendered PDFs."""
from pathlib import Path
import hashlib, json, re, subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
names = [f'lecture{i:02d}' for i in range(1,13)] + ['solution']
render = json.loads((OUT/'render-results.json').read_text())
pdf = json.loads((OUT/'pdf-checks.json').read_text())
before = json.loads((OUT/'source-before-sha256.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
changed = [p for p,h in before.items() if sha(ROOT/p)!=h]
assert not changed, changed
reports = ['l01-l04/REVIEW.md','l01-l04/VISUAL.md','l05-l08/REVIEW.md','l05-l08/VISUAL.md','l09-l12/REVIEW.md','l09-l12/VISUAL.md','VISUAL-solution.md']
assert all((OUT/p).exists() for p in reports)
for name in names:
    assert render[name]['returncode']==0
    assert render[name]['source_sha256']==sha(ROOT/(name+'.qmd'))
    assert render[name]['pdf_sha256']==pdf[name]['pdf_sha256']==sha(OUT/'pdf'/(name+'.pdf'))
    assert len(list((OUT/'visual'/name).glob('page-*.png')))==pdf[name]['pages']
    pdf[name]['visual_status']='verified with findings: all pages overviewed; selected pages enlarged; see visual reports'
(OUT/'pdf-checks.json').write_text(json.dumps(pdf,ensure_ascii=False,indent=2)+'\n')
report = ROOT/'LECTURE_REVIEW_2026-09-11.md'
links = re.findall(r'\]\((/[^)]+)\)',report.read_text())
missing = [x for x in links if not Path(re.sub(r':\d+$','',x)).exists()]
assert not missing,missing
summary = {
    'date':'2026-09-11','timezone':'Asia/Tokyo',
    'git_commit':subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'source_files_unchanged':len(before),'protected_changed':changed,
    'rendered_documents':len(names),'rendered_pages':sum(v['pages'] for v in pdf.values()),
    'all_pages_rasterized_and_overviewed':True,'whole_document_microscopic_proofread':False,
    'contact_sheets':sum(len(v['contacts']) for v in pdf.values()),
    'overfull_messages':sum(len(v['box_messages']) for v in pdf.values()),
    'missing_character_messages':sum(len(v['missing_character_lines']) for v in pdf.values()),
    'unresolved_pdf_references':sum(v['unresolved_refs'] for v in pdf.values()),
    'paper_edge_clipping':{'lecture05':[17]},
    'r_clean_execution':['lecture05','lecture08','lecture09'],
    'source_edits_applied':False,'existing_distribution_outputs_replaced':False,
    'report':str(report),'reports':reports,'local_report_links_checked':len(links),'missing_report_links':missing,
}
(OUT/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
