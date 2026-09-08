"""Independent numerical checks of the current lecture 11/12 linear systems.

No manuscript or existing evidence is changed. Run from the repository root.
"""
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(20260909)


def l11_direct(beta, gamma, varphi, lam, kp, phi, rho, a, m, z):
    # Unknowns: y, cH, cS, nH, nS, w, d, pi, r.
    # Use the original household/firm equations, not the reduced IS curve.
    rows = []
    rhs = []

    def eq(coefficients, value=0):
        row = np.zeros(9)
        for index, coefficient in coefficients.items():
            row[index] = coefficient
        rows.append(row)
        rhs.append(value)

    eq({0: -1, 1: lam, 2: 1 - lam})  # Goods/consumption aggregation
    eq({0: -1, 3: lam, 4: 1 - lam}, -a)  # Production
    eq({5: 1, 1: -gamma, 3: -varphi})  # H labor supply
    eq({5: 1, 2: -gamma, 4: -varphi})  # S labor supply
    eq({1: 1, 5: -1, 3: -1}, z)  # H disposable income
    eq({6: 1, 0: -1, 5: 1, 3: lam, 4: 1 - lam})  # Dividend accounting
    eq({7: 1 - beta * rho, 5: -kp}, -kp * a)  # Price setting
    eq({8: 1, 7: -(phi - rho)}, -m)  # Monetary rule + Fisher equation
    eq({8: 1, 2: -gamma * (rho - 1)})  # S Euler equation
    solution = np.linalg.solve(rows, rhs)
    # S disposable income is omitted from solve because Walras' law makes it redundant.
    y, cH, cS, nH, nS, w, d, pi, r = solution
    saver_budget = cS - w - nS - d / (1 - lam) + lam * z / (1 - lam)
    return solution, max(np.max(np.abs(np.asarray(rows) @ solution - rhs)), abs(saver_budget))


max_l11_error = 0.0
max_l11_residual = 0.0
l11_cases = 0
for _ in range(200):
    beta = rng.uniform(.9, .999)
    gamma = rng.uniform(.5, 3)
    varphi = rng.uniform(.25, 3)
    lam = rng.uniform(.02, min(.7, .9 / (1 + varphi)))
    kp = rng.uniform(.01, .4)
    phi = rng.uniform(1.02, 3)
    rho = rng.uniform(0, .95)
    theta = 1 - lam * varphi / (1 - lam)
    krho = kp * (gamma + varphi) / (1 - beta * rho)
    denominator = krho * (phi - rho) + gamma * theta * (1 - rho)
    for a, m, z in [(0.01, 0, 0), (0, .01, 0), (0, 0, .01)]:
        actual, residual = l11_direct(beta, gamma, varphi, lam, kp, phi, rho, a, m, z)
        yf = (1 + varphi) / (gamma + varphi) * a
        rfR = gamma * (rho - 1) * yf
        rfT = rfR - gamma * lam * varphi / ((gamma + varphi) * (1 - lam)) * (rho - 1) * z
        x = (m + rfT) / denominator
        gap = -varphi / (1 - lam) * x - varphi / ((gamma + varphi) * (1 - lam)) * z
        predicted = np.array([yf + x, yf + x - (1 - lam) * gap, yf + x + lam * gap,
                              krho * x, rfT - gamma * theta * (1 - rho) * x])
        observed = actual[[0, 1, 2, 7, 8]]
        max_l11_error = max(max_l11_error, float(np.max(np.abs(observed - predicted))))
        max_l11_residual = max(max_l11_residual, float(residual))
        l11_cases += 1


max_distribution_error = 0.0
max_euler_pe_error = 0.0
max_ratio_error = 0.0
max_recursive_error = 0.0
for _ in range(400):
    beta = rng.uniform(.9, .999)
    gamma = rng.uniform(.5, 3)
    varphi = rng.uniform(.25, 3)
    lam = rng.uniform(.05, .6)
    # Cover suppression, amplification, and negative chi, avoiding singularities.
    chi = rng.uniform(-1, .95 / lam)
    tau = lam * (1 - (chi - 1) / varphi)
    theta = (1 - lam * chi) / (1 - lam)
    y = .01
    # Unknowns cH,cS,nH,nS,w,d: household labor/income equations + aggregation.
    matrix = np.array([[lam, 1-lam, 0, 0, 0, 0],
                       [0, 0, lam, 1-lam, 0, 0],
                       [-gamma, 0, -varphi, 0, 1, 0],
                       [0, -gamma, 0, -varphi, 1, 0],
                       [1, 0, -1, 0, -1, -tau/lam],
                       [0, 0, 0, 0, 1, 1]])
    result = np.linalg.solve(matrix, [y, y, 0, 0, 0, 0])
    expected = np.array([chi*y, theta*y, (gamma+varphi)*y, -(gamma+varphi)*y])
    max_distribution_error = max(max_distribution_error, float(np.max(np.abs(result[[0,1,4,5]]-expected))))
    p = rng.uniform(0, .95)
    r = -.01
    den = 1-beta*p*(1-lam*chi)
    if abs(den) < 1e-5:
        continue
    omegaT = (1-beta*(1-lam*chi))/den
    directT = (1-lam)*beta/(gamma*den)
    pe = directT/(1-omegaT)
    euler = 1/(gamma*theta*(1-p))
    rank = 1/(gamma*(1-p))
    max_euler_pe_error = max(max_euler_pe_error, abs(pe-euler))
    max_ratio_error = max(max_ratio_error, abs(pe/rank-(1-lam)/(1-lam*chi)))
    # For a geometrically decaying equilibrium path, compare the PV and recursive forms.
    cS = theta*(-r)*euler
    pv = (1-beta)*cS/(1-beta*p) - beta/gamma*r/(1-beta*p)
    recursive = (1-beta)*cS - beta/gamma*r + beta*p*cS
    max_recursive_error = max(max_recursive_error, abs(pv-cS), abs(recursive-cS))


assert max_l11_error < 1e-10
assert max_l11_residual < 1e-10
assert max_distribution_error < 1e-10
assert max_euler_pe_error < 1e-8
assert max_ratio_error < 1e-8
assert max_recursive_error < 1e-10

# Published calibrations (L11 uses a policy-rule shock, L12 a given real-rate gap).
l11_table = {}
for label, lam, m, z in [('RANK monetary',0,.01,0),('TANK monetary',.3,.01,0),('TANK transfer',.3,0,.01)]:
    s, _ = l11_direct(.99,1,1,lam,.05,1.5,.5,0,m,z)
    l11_table[label] = dict(zip(['x_percent','pi_pp','r_pp'], (s[[0,7,8]]*100).tolist()))
l12_table=[]
for tau in [0,.3,.45]:
    chi=1+(1-tau/.3)
    theta=(1-.3*chi)/.7
    l12_table.append({'tau':tau,'chi':chi,'theta':theta,'ratio':1/theta})

findings = {
    'l11_marginal_disutility': {
        'gamma':1,'varphi':1,'W':1,'CH':1,'CS':1.01,
        'NH':1,'NS':1/1.01,
        'marginal_disutility_H':1,'marginal_disutility_S':1/1.01,
        'conclusion':'At a common wage, higher consumption implies LOWER marginal labor disutility.'
    },
    'l12_capital_normalization': {
        'delta':.1,'Kbar':10,'Ibar':1,'log_investment_change':.01,
        'correct_first_order_k_next':.001,'printed_formula_k_next':.01,
        'exact_k_next':float(np.log((.9*10+np.exp(.01))/10)),
        'consumption_share':.8,'investment_share':.2,
        'correct_first_order_y_with_c_zero':.002,'printed_formula_y_with_c_zero':.01,
        'exact_y':float(np.log(.8+.2*np.exp(.01)))
    }
}
summary = {'l11_cases':l11_cases,'l12_cases':400,
           'max_l11_closed_vs_primitive_error':max_l11_error,
           'max_l11_primitive_residual':max_l11_residual,
           'max_l12_distribution_error':max_distribution_error,
           'max_l12_euler_vs_PE_error':max_euler_pe_error,
           'max_l12_amplification_ratio_error':max_ratio_error,
           'max_recursive_PV_equilibrium_error':max_recursive_error,
           'l11_published_calibration':l11_table,'l12_published_calibration':l12_table,
           'minimal_counterexamples':findings,
           'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                            for name in ['lecture11.qmd','lecture12.qmd','solution.qmd']}}
(OUT/'coefficient-checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
