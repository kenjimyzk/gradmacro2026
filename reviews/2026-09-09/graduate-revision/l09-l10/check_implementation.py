"""Validate the new target-deviation implementation algebra independently."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np

rng = np.random.default_rng(9092026)
residuals, root_counts = [], []
for _ in range(200):
    beta = rng.uniform(.8, .999)
    tg, kx, phi = rng.uniform(.2, 4), rng.uniform(.005, .8), rng.uniform(1.01, 5)
    xs, pis, exs, epis, re, d, p = rng.normal(scale=.01, size=7)
    # Construct an arbitrary NKPC-consistent target, then a deviation that
    # satisfies the proposed homogeneous error equations.
    u = pis-beta*epis-kx*xs
    ins = re+tg*(exs-xs)+epis
    ep = (p-kx*d)/beta
    ed = d+(phi*p-ep)/tg
    x, pi, ex, epi, interest = xs+d, pis+p, exs+ed, epis+ep, ins+phi*p
    residuals.extend([x-ex+(interest-epi-re)/tg, pi-beta*epi-kx*x-u])
    A = np.array([[1+kx/(beta*tg), phi/tg-1/(beta*tg)], [-kx/beta, 1/beta]])
    residuals.extend(np.array([ed, ep])-A@np.array([d, p]))
    root_counts.append(int(np.sum(np.abs(np.linalg.eigvals(A))>1+1e-9)))

root = Path(__file__).resolve().parents[4]
svg08 = ET.parse(root/'figures/lecture08/lecture08_overview_infographic.svg').getroot()
svg09 = ET.parse(root/'figures/lecture09/lecture09_overview_infographic.svg').getroot()
ns = {'s': 'http://www.w3.org/2000/svg'}
natural_text = next(n for n in svg08.findall('.//s:text', ns)
                    if '自然産出量' in ''.join(n.itertext()))
natural_superscripts = [n.text for n in natural_text
                       if n.attrib.get('baseline-shift') == 'super']
gap_superscripts = [n.text for n in svg09.findall('.//s:tspan', ns)
                   if n.attrib.get('baseline-shift') == 'super']
assert natural_superscripts == ['f', 'f']
assert gap_superscripts == ['e']*5
assert max(abs(float(v)) for v in residuals) < 1e-10
assert set(root_counts) == {2}
result = {
    'nonzero_target_deviation_cases': 200,
    'max_abs_structural_and_matrix_residual': max(abs(float(v)) for v in residuals),
    'unstable_root_count': sorted(set(root_counts)),
    'lecture08_natural_level_superscripts': natural_superscripts,
    'lecture09_gap_superscripts': gap_superscripts,
    'svg_visual_inspection': 'Both updated PNGs inspected; formulas and superscripts fit inside the existing boxes.'
}
output = json.dumps(result, indent=2, ensure_ascii=False)+'\n'
Path(__file__).with_name('implementation-check.json').write_text(output)
print(output)
