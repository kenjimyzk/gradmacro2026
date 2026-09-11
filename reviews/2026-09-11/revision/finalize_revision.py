"""Promote reviewed artifacts only after their source and visual checks pass."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
WORK=Path(json.loads((OUT/'render-state.json').read_text())['work'])
NAMES=[f'lecture{i:02d}' for i in range(1,13)]+['solution']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
render=json.loads((OUT/'render-results.json').read_text())
pdf=json.loads((OUT/'pdf-checks.json').read_text())
artifacts=json.loads((OUT/'artifact-checks.json').read_text())
katex=json.loads((OUT/'katex-checks.json').read_text())
assert not artifacts['errors'] and not katex['errors']
before=json.loads((OUT/'before-sha256.json').read_text())
inputs={}
for rel,old in before.items():
    p=ROOT/rel
    assert p.exists(), rel
    assert sha(p)==sha(WORK/rel), ('live/work input mismatch',rel)
    inputs[rel]={'before':old,'after':sha(p),'changed':old!=sha(p)}
for name in NAMES:
    assert render[name]['returncode']==0
    assert render[name]['source_sha256']==sha(ROOT/(name+'.qmd'))
    assert pdf[name]['pdf_sha256']==sha(OUT/'pdf'/(name+'.pdf'))
    assert pdf[name]['visual_status']=='verified: all pages overview and targeted expanded inspection'
    for key in ['replacement_glyphs','unresolved_refs','missing_character_lines','box_messages','flagged_pages']:
        assert not pdf[name][key], (name,key,pdf[name][key])
    for ext in ['pdf','html']:
        assert sha(OUT/ext/(name+'.'+ext))==render[name]['outputs'][ext]['sha256']
        assert sha(WORK/(name+'.'+ext))==render[name]['outputs'][ext]['sha256']

delivered={}
for name in NAMES:
    delivered[name]={'pages':pdf[name]['pages'],'files':{}}
    for ext in ['pdf','html']:
        target=ROOT/(name+'.'+ext)
        shutil.copy2(OUT/ext/target.name,target)
        assert sha(target)==render[name]['outputs'][ext]['sha256']
        delivered[name]['files'][target.name]=sha(target)
    support=WORK/(name+'_files')
    if support.exists():
        shutil.copytree(support,ROOT/support.name,dirs_exist_ok=True)
        for p in sorted(support.rglob('*')):
            if p.is_file():
                rel=p.relative_to(WORK)
                assert sha(ROOT/rel)==sha(p)
                delivered[name]['files'][str(rel)]=sha(p)
subprocess.run(['git','-c','core.fsmonitor=false','diff','--check'],cwd=ROOT,check=True)
result={'status':'complete','documents':len(NAMES),'pdf_pages':sum(p['pages'] for p in pdf.values()),
        'pdf_layout':'all pages overview and targeted expanded inspection',
        'pdf_missing_glyphs':0,'pdf_overfull':0,'pdf_outside_or_near_edge':0,
        'html_math_spans':katex['total'],'html_math_syntax_errors':0,
        'html_browser_layout':'not run','inputs':inputs,'delivered':delivered}
(OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
rows=['| 文書 | ページ数 | 最終PDF |','|---|---:|---|']
for name in NAMES:
    title='解答集' if name=='solution' else f'第{int(name[-2:])}回'
    rows.append(f'| {title} | {pdf[name]["pages"]} | [{name}.pdf]({ROOT}/{name}.pdf) |')
report=(OUT/'final-report-template.md').read_text().replace('{{PAGES}}',str(result['pdf_pages'])).replace('{{PDF_TABLE}}','\n'.join(rows))
for target in re.findall(r'\]\((/[^)]+)\)',report):
    assert Path(target).exists(), ('missing report link',target)
(ROOT/'LECTURE_FIXES_2026-09-11.md').write_text(report)
review=ROOT/'LECTURE_REVIEW_2026-09-11.md'
old=review.read_text()
note='> 修正対応完了：この文書は修正前のレビュー記録です。全指摘への対応と配布用PDF・HTMLの再検証は [修正報告]('+str(ROOT)+'/LECTURE_FIXES_2026-09-11.md) を参照してください。\n\n'
if note not in old:
    title,body=old.split('\n',1)
    review.write_text(title+'\n\n'+note+body.lstrip('\n'))
print(json.dumps({k:v for k,v in result.items() if k not in ['inputs','delivered']},ensure_ascii=False,indent=2))
