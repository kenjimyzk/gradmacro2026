from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.oxml.ns import qn
from pathlib import Path

path = Path('output/docx/マクロ経済学B_シラバス案.docx')
doc = Document(path)

# A4 page geometry with readable margins.
for section in doc.sections:
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(17)
    section.bottom_margin = Mm(17)
    section.left_margin = Mm(20)
    section.right_margin = Mm(20)

font_name = 'Noto Sans JP'
size_map = {
    'Normal': 10.5,
    'Body Text': 10.5,
    'List Paragraph': 10.5,
    'Title': 22,
    'Subtitle': 12,
    'Author': 10.5,
    'Heading 1': 15,
    'Heading 2': 12.5,
    'Heading 3': 11.5,
}


def set_rfonts(rpr):
    if rpr is None:
        return
    rfonts = rpr.rFonts
    if rfonts is None:
        from docx.oxml import OxmlElement
        rfonts = OxmlElement('w:rFonts')
        rpr.insert(0, rfonts)
    for attr in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
        rfonts.set(qn(f'w:{attr}'), font_name)

for style in doc.styles:
    if not hasattr(style, 'font'):
        continue
    style.font.name = font_name
    set_rfonts(style._element.get_or_add_rPr())
    if style.name in size_map:
        style.font.size = Pt(size_map[style.name])
    if style.name in {'Title','Subtitle','Author','Heading 1','Heading 2','Heading 3'}:
        style.font.color.rgb = RGBColor(0, 0, 0)

# Make any table text inherit the body size while preserving emphasis and links.
def patch_runs(paragraph):
    for run in paragraph.runs:
        run.font.name = font_name
        set_rfonts(run._element.get_or_add_rPr())

for p in doc.paragraphs:
    patch_runs(p)
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                patch_runs(p)

# Replace the stale default eastAsia language font marker if present.
styles_root = doc.styles._element
for rpr in styles_root.xpath('.//w:rPr'):
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is not None and rfonts.get(qn('w:eastAsia')) == 'ja':
        rfonts.set(qn('w:eastAsia'), font_name)

doc.save(path)
print(path)
