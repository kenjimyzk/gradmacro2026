"""Independent numerical checks for lectures 01--04; leaves sources unchanged."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
checks = {}

# Check the actual vector paths of the figure, using the coordinate-to-data
# mappings implied by its labelled axes (not an existing plotting function).
tree = ET.parse(ROOT / "figures/lecture02/ar1_irf_simulation.svg")
irfs = []
for polyline, rho in zip(tree.findall("{*}polyline"), (0.5, 0.8, 0.9)):
    points = [tuple(map(float, pair.split(","))) for pair in polyline.attrib["points"].split()]
    rows = []
    for xp, yp in points:
        h = (xp - 100) / 60
        expected = rho ** h
        observed = (420 - yp) / 320
        rows.append({"h": h, "plotted": observed, "formula": expected,
                     "error_pixels": yp - (420 - 320 * expected)})
    irfs.append({"rho": rho, "max_abs_error_pixels": max(abs(r["error_pixels"]) for r in rows),
                 "status": "verified" if max(abs(r["error_pixels"]) for r in rows) < 0.15 else "failed",
                 "points": rows})
checks["ar1_svg_formula_alignment"] = irfs

tree = ET.parse(ROOT / "figures/lecture03/consumption_growth_simulation.svg")
growth = []
for polyline, gamma in zip(tree.findall("{*}polyline"), (1, 2, 5)):
    rows = []
    for pair in polyline.attrib["points"].split():
        xp, yp = map(float, pair.split(","))
        rate = 1 + (xp - 110) / 12000
        expected = (0.96 * rate) ** (1/gamma)
        actual = 0.95 + (420 - yp) / 4000
        rows.append({"R": rate, "plotted": actual, "formula": expected,
                     "error_pixels": yp - (420 - 4000 * (expected-0.95))})
    growth.append({"gamma": gamma, "max_abs_error_pixels": max(abs(r["error_pixels"]) for r in rows),
                   "status": "verified" if max(abs(r["error_pixels"]) for r in rows) < 0.5 else "failed",
                   "points": rows})
checks["consumption_growth_svg_alignment_subpixel_tolerance"] = growth

checks["lecture02_exercises"] = {
    "ar1_0_through_4": [0.8**h for h in range(5)],
    "half_life": math.log(0.5)/math.log(0.8),
    "conditional_forecasts": [2+0.6**h*(5-2) for h in (1,2)],
    "first_order_output": 0.8*0.01+0.2*0.02,
    "triangular_matrix_eigenvalues": [0.8, 1.05],
}
checks["lecture03_exercises"] = {
    "discounted_asset_limits": {str(c): 1.04/0.04*(1+0.04*5-c) for c in (1.1,1.2,1.3)},
    "equity_price": 0.5*0.8*1.5+0.5*1.2*0.5,
    "riskfree_gross_return": 1/(0.5*0.8+0.5*1.2),
    "equity_expected_gross_return": (1.5+0.5)/2/0.9,
    "sdf_return_covariance": 1-((1.5+0.5)/2/0.9),
}

# Closed-form equilibrium checked against the original level equations over a
# grid that includes linear production and all three employment-response signs.
max_residual = 0
max_log_identity_error = 0
for alpha in (0.0,0.2,0.4,0.9):
    for gamma in (0.5,1.,2.,5.):
        for phi in (0.2,1.,3.):
            den = phi+alpha+gamma*(1-alpha)
            nss = (1-alpha)**(1/den)
            yss = nss**(1-alpha)
            wss = (1-alpha)*nss**(-alpha)
            for a in (-0.1,0.,0.01,0.1):
                n = ((1-alpha)*math.exp((1-gamma)*a))**(1/den)
                y = math.exp(a)*n**(1-alpha)
                w = (1-alpha)*math.exp(a)*n**(-alpha)
                max_residual = max(max_residual, abs(n**phi*y**gamma-w), abs(y-w*n-alpha*y))
                max_log_identity_error = max(max_log_identity_error,
                    abs(math.log(n/nss)-(1-gamma)*a/den),
                    abs(math.log(y/yss)-(1+phi)*a/den),
                    abs(math.log(w/wss)-(phi+gamma)*a/den))
checks["lecture04_equilibrium_grid"] = {"cases": 4*4*3*4,
    "max_level_equilibrium_residual": max_residual,
    "max_exact_log_identity_error": max_log_identity_error,
    "status": "verified" if max(max_residual,max_log_identity_error)<1e-12 else "failed"}

den = 1+0.4+2*(1-0.4)
checks["lecture04_exercise5_percent"] = [
    {"h":h,"a":0.9**h,"y":2/den*0.9**h,"n":-1/den*0.9**h,"w":3/den*0.9**h}
    for h in range(3)]
checks["lecture02_employment_counterexample"] = {
    "parameters": {"alpha":0.4,"phi":1.,"gamma":2.,"rho":0.9,"shock":0.01},
    "n_impact_percent": -1/den,
    "n_next_percent": -0.9/den,
    "implication": "Persistence prolongs an employment decrease in the course's own model."}

# Directly expand the exact resource constraint with the Rotemberg resource cost.
# Its zero-inflation steady state is efficient and C=N=1.
gamma, phi, eta = 2., 1., 10.
welfare = []
for eps in (0.01,0.005,0.0025):
    ylog = 0.7*eps
    pilog = 0.4*eps
    n = math.exp(ylog)
    c = n*(1-eta/2*math.expm1(pilog)**2)
    utility = (c**(1-gamma)-1)/(1-gamma) - (n**(1+phi)-1)/(1+phi)
    approx = -(gamma+phi)/2*ylog**2-eta/2*pilog**2
    welfare.append({"shock_scale":eps,"exact_utility_change":utility,
        "quadratic_approximation":approx,"difference":utility-approx,
        "error_divided_by_scale_cubed":(utility-approx)/eps**3,
        "exact_log_c_minus_log_n":math.log(c)-math.log(n),
        "second_order_log_c_minus_log_n":-eta/2*pilog**2})
checks["lecture02_quadratic_welfare"] = welfare
checks["lecture04_rate_scaling"] = {
    "steady_R":1.04,"R_change":0.000001,
    "exact_log_deviation":math.log((1.04+0.000001)/1.04),
    "correct_first_order":0.000001/1.04,
    "stated_approximation":0.000001}

files = ["lecture01.qmd","lecture02.qmd","lecture03.qmd","lecture04.qmd","solution.qmd",
         "includes/assumption-matrix.qmd","includes/notation-concordance.qmd",
         "figures/lecture02/ar1_irf_simulation.svg","figures/lecture03/consumption_growth_simulation.svg",
         "data/lecture02/gdpc1.csv"]
payload = {"python":sys.version,"executable":sys.executable,
    "source_sha256":{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
    "checks":checks}
(OUT/"independent_checks.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"output":str(OUT/"independent_checks.json"),
    "ar1_svg":[{k:x[k] for k in ("rho","max_abs_error_pixels","status")} for x in irfs],
    "equilibrium":checks["lecture04_equilibrium_grid"]},indent=2))
