from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

path = Path('output/docx/マクロ経済学B_シラバス案.docx')
doc = Document(path)
for table in doc.tables:
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(OxmlElement('w:cantSplit'))
        if i == 0 and trPr.find(qn('w:tblHeader')) is None:
            trPr.append(OxmlElement('w:tblHeader'))
doc.save(path)
print(path)
