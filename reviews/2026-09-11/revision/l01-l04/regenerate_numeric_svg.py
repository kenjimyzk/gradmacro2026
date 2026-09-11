"""Regenerate AR(1) points and IS-LM annotations from their model geometry."""
import json
import math
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

ar1 = ROOT / "figures/lecture02/ar1_irf_simulation.svg"
source = ar1.read_text()
colors = {"#2f6fbe": 0.5, "#379b55": 0.8, "#d9792f": 0.9}
def regenerate_polyline(match):
    tag = match.group(0)
    rho = colors[ET.fromstring(tag).attrib["stroke"]]
    points = " ".join(f"{100+60*h},{420-320*rho**h:.6f}" for h in range(13))
    return re.sub(r'points="[^"]*"', f'points="{points}"', tag)
source, count = re.subn(r"<polyline\b[^>]*/>", regenerate_polyline, source)
assert count == 3
ar1.write_text(source)

islm = ROOT / "figures/lecture01/is_lm_equilibrium.svg"
source = islm.read_text()
doc = ET.fromstring(source)
paths = [el for el in doc if el.tag.endswith("path") and el.get("stroke") in {"#2f6fbe", "#d45d48"}]
points = [list(map(float, re.findall(r"[-+]?\d*\.?\d+", el.attrib["d"]))) for el in paths]

def point(p, t):
    b = [(1-t)**3, 3*(1-t)**2*t, 3*(1-t)*t*t, t**3]
    return tuple(sum(b[i]*p[2*i+k] for i in range(4)) for k in (0, 1))

def y_at_x(p, x):
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo+hi)/2
        if point(p, mid)[0] < x:
            lo = mid
        else:
            hi = mid
    return point(p, (lo+hi)/2)[1]

lo, hi = max(p[0] for p in points), min(p[-2] for p in points)
for _ in range(80):
    mid = (lo+hi)/2
    if y_at_x(points[0], mid) < y_at_x(points[1], mid):
        lo = mid
    else:
        hi = mid
x = (lo+hi)/2
y = y_at_x(points[0], x)

def replace_attrs(tag, **attrs):
    for key, value in attrs.items():
        value = f"{value:.6f}" if isinstance(value, float) else str(value)
        key = key.replace("_", "-")
        if re.search(rf'\b{key}="[^"]*"', tag):
            tag = re.sub(rf'\b{key}="[^"]*"', f'{key}="{value}"', tag)
        else:
            tag = tag.replace(">", f' {key}="{value}">', 1)
    return tag

source = re.sub(r"<circle\b[^>]*/>", lambda m: replace_attrs(m.group(), cx=x, cy=y), source)
lines = source.splitlines()
for i, line in enumerate(lines):
    if '<line ' in line and 'stroke-dasharray="7 6"' in line:
        el = ET.fromstring(line.strip())
        if el.attrib["x1"] == el.attrib["x2"]:
            lines[i] = replace_attrs(line, x1=x, y1=y, x2=x)
        else:
            lines[i] = replace_attrs(line, y1=y, x2=x, y2=y)
    if ">均衡点</text>" in line:
        lines[i] = replace_attrs(line, x=x, y=y-37, text_anchor="middle")
    if ">Y*</text>" in line:
        lines[i] = replace_attrs(line, x=x, text_anchor="middle")
    if ">r*</text>" in line:
        lines[i] = replace_attrs(line, y=y+6)
islm.write_text("\n".join(lines)+"\n")

result = {"ar1": {"curves": 3, "points_per_curve": 13, "decimal_places": 6},
          "is_lm": {"intersection": [x, y], "annotations_generated_from_intersection": True}}
(OUT / "numeric_svg_regeneration.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
