"""Independent check of generated SVG geometry; does not import the generator."""
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
results={}
for model,expected in [('rank',(.01,.99,.01,1.0)),('tank',(.604,.693,1.057,1.75))]:
    path=ROOT/'figures/lecture12'/f'{model}_nk_cross.svg'
    root=ET.parse(path).getroot()
    paths={el.attrib['class']:list(map(float,re.findall(r'-?\d+(?:\.\d+)?',el.attrib['d'])))
           for el in root.iter() if el.tag.endswith('path') and 'class' in el.attrib}
    diagonal=paths['line45']
    def slope(p):
        return (p[3]-p[1])/(p[2]-p[0])
    # The labels mark a common 0 to 3 percent range; c=y fixes the ratio of scales.
    vertical_unit=(diagonal[1]-diagonal[3])/3
    horizontal_unit=(diagonal[2]-diagonal[0])/3
    omega=slope(paths['pe'])/slope(diagonal)
    direct=paths['direct']
    feedback=paths['feedback']
    direct_delta=(direct[1]-direct[3])/vertical_unit
    feedback_delta=(feedback[1]-feedback[3])/vertical_unit
    total_delta=(feedback[2]-feedback[0])/horizontal_unit
    observed=(omega,direct_delta,feedback_delta,total_delta)
    errors=[abs(a-b) for a,b in zip(observed,expected)]
    assert max(errors)<1e-8,(model,observed,expected)
    assert abs(direct[0]-direct[2])<1e-8
    assert max(abs(direct[j+2]-feedback[j]) for j in [0,1])<1e-8
    def residual(x,y,line):
        return abs(y-(line[1]+slope(line)*(x-line[0])))
    old=direct[:2]
    bridge=direct[2:]
    new=feedback[2:]
    intersection_error=max(residual(*old,paths['pe']),residual(*old,diagonal),
                           residual(*bridge,paths['pe2']),residual(*new,paths['pe2']),residual(*new,diagonal))
    assert intersection_error<1e-5
    text=' '.join(''.join(el.itertext()) for el in root.iter() if el.tag.endswith('text'))
    for value in [f'{omega:.3f}',f'{direct_delta:.3f}%',f'{feedback_delta:.3f}%',f'{total_delta:.3f}%']:
        assert value in text,value
    results[model]={'omega':omega,'direct_percent':direct_delta,'feedback_percent':feedback_delta,
                    'total_percent':total_delta,'max_coefficient_error':max(errors),
                    'max_intersection_error_pixels':intersection_error,
                    'axis_endpoints':diagonal,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assert results['rank']['axis_endpoints']==results['tank']['axis_endpoints']
direct_ratio=results['tank']['direct_percent']/results['rank']['direct_percent']
total_ratio=results['tank']['total_percent']/results['rank']['total_percent']
assert abs(direct_ratio-.7)<1e-8
assert abs(total_ratio-1.75)<1e-8
summary={'verified':True,'figures':results,'direct_ratio':direct_ratio,'total_ratio':total_ratio,
         'rank_feedback_share':results['rank']['feedback_percent']/results['rank']['total_percent']}
(OUT/'svg-checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
