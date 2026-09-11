"""Independent geometry check of the rendered IS-LM equilibrium marker."""
import json
import math
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
source = ROOT / "figures/lecture01/is_lm_equilibrium.svg"
doc = ET.parse(source).getroot()
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
circle = next(el for el in doc if el.tag.endswith("circle"))
cx, cy, radius = (float(circle.attrib[k]) for k in ("cx", "cy", "r"))
result = {
    "source": str(source.relative_to(ROOT)),
    "intersection": {"x": x, "y": y},
    "marker": {"x": cx, "y": cy, "radius": radius},
    "distance_marker_to_intersection": math.hypot(cx-x, cy-y),
    "intersection_is_inside_marker": math.hypot(cx-x, cy-y) <= radius,
    "IS_y_at_marker_x": y_at_x(points[0], cx),
    "LM_y_at_marker_x": y_at_x(points[1], cx),
}
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
print(out.read_text())
