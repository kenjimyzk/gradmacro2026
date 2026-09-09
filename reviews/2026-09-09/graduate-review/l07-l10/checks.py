"""Independent, bounded checks for the 2026-09-09 graduate-note review.

Does not render or modify lecture sources. Run with python3 checks.py.
"""
import json
from pathlib import Path

import numpy as np

rng = np.random.default_rng(20260909)
results = {}

# Reinsert lecture08's three closed-form responses into its original linear
# household, production, resource, NKPC and policy equations.
residuals = []
for _ in range(120):
    beta = rng.uniform(.8, .999)
    gamma, varphi = rng.uniform(.2, 4, 2)
    alpha, GY = rng.uniform(0, .7, 2)
    phi = rng.uniform(1.01, 5)
    kp = rng.uniform(.005, .8)
    tg, tv = gamma / (1-GY), (varphi+alpha)/(1-alpha)
    za, zg = (tv+1)/(tg+tv), tg/(tg+tv)
    kx = kp*(tg+tv)
    for typ in ('monetary', 'technology', 'government'):
        rho = rng.uniform(0, .99)
        k = kx/(1-beta*rho)
        den = k*(phi-rho)+tg*(1-rho)
        a, g, m = [float(typ == name)*.01 for name in
                   ('technology', 'government', 'monetary')]
        rf = -tg*(1-rho)*za*a + tg*(1-rho)*(1-zg)*g
        x = (m+rf)/den
        pi = k*x
        y = x + za*a + zg*g
        c, n = (y-g)/(1-GY), (y-a)/(1-alpha)
        w = gamma*c+varphi*n
        mc = w-y+n
        rn = phi*pi-m
        r = rn-rho*pi
        residuals += [r-gamma*(rho-1)*c,
                      pi-beta*rho*pi-kp*mc,
                      mc-(tg+tv)*x,
                      y-a-(1-alpha)*n,
                      y-(1-GY)*c-g]
results['lecture08_structural_substitution'] = {
    'parameter_sets': 120, 'shock_cases': 360,
    'max_abs_residual': float(np.max(np.abs(residuals)))}

# Test the stated characteristic-root conclusions at independent draws.
root_results = {name: [] for name in ('peg', 'passive', 'active')}
for _ in range(120):
    beta, gamma, kx = rng.uniform(.8, .999), rng.uniform(.2, 6), rng.uniform(.005, 2)
    for name, phi in [('peg', 0), ('passive', .5), ('active', 1.5)]:
        A = [[1+kx/(beta*gamma), phi/gamma-1/(beta*gamma)],
             [-kx/beta, 1/beta]]
        count = int(np.sum(np.abs(np.linalg.eigvals(A))>1+1e-9))
        root_results[name].append(count)
results['lecture09_BK_root_counts'] = {
    name: sorted(set(vals)) for name, vals in root_results.items()}

# Infinite-horizon optimal history-dependent policy, checked against NKPC
# and target condition rather than a finite-horizon terminal approximation.
residuals = []
for _ in range(120):
    beta, kx = rng.uniform(.8, .999), rng.uniform(.005, .5)
    omega, rho = rng.uniform(.5, 100), rng.uniform(0, .98)
    B = 1+beta+kx*kx*omega
    q = 2/(B+np.sqrt(B*B-4*beta))
    b = -kx*omega/(B-beta*(q+rho))
    lag, u = rng.normal(size=2)*.01
    x = q*lag+b*u
    pi = -(x-lag)/(kx*omega)
    ex = q*x+b*rho*u
    epi = -(ex-x)/(kx*omega)
    residuals += [pi-beta*epi-kx*x-u, kx*omega*pi+x-lag]
results['lecture09_infinite_horizon_KKT'] = {
    'parameter_sets': 120, 'max_abs_residual': float(np.max(np.abs(residuals)))}

# Compare the general welfare coefficient with the second derivative of
# actual nonlinear utility, using the exact steady-state levels of L08.
relative_errors = []
for _ in range(40):
    gamma, varphi = rng.uniform(.3, 3, 2)
    alpha, GY = rng.uniform(0, .6, 2)
    N = ((1-alpha)*(1-GY)**(-gamma))**(1/(varphi+alpha+gamma*(1-alpha)))
    Y, G = N**(1-alpha), GY*N**(1-alpha)
    C = Y-G
    def U(y):
        cons, labor = Y*np.exp(y)-G, N*np.exp(y/(1-alpha))
        return (cons**(1-gamma)-1)/(1-gamma)-labor**(1+varphi)/(1+varphi)
    h = 1e-4
    observed = -(U(h)-2*U(0)+U(-h))/h**2 / (C**(-gamma)*Y)
    expected = gamma/(1-GY)+(varphi+alpha)/(1-alpha)
    relative_errors.append(abs(observed/expected-1))
results['lecture09_general_welfare_curvature'] = {
    'parameter_sets': 40, 'max_relative_finite_difference_error': max(relative_errors)}

# L10's individual wage objective differentiated at an arbitrary relative
# wage: income and type-specific labor disutility, not the symmetric FOC.
errors = []
for _ in range(120):
    gamma, varphi = rng.uniform(.3, 3, 2)
    psi, tau = rng.uniform(1.1, 10), rng.uniform(0, 1)
    W, C, N, s = np.exp(rng.normal(scale=.1, size=4))
    def value(s):
        nh = N*s**(-psi)
        return (1+tau)*W*s*nh-C**gamma*nh**(1+varphi)/(1+varphi)
    nh = N*s**(-psi)
    mu = W*s/(C**gamma*nh**varphi)
    formula = psi*W*nh*(1/mu-(1+tau)*(1-1/psi))
    h = 1e-6
    observed = (value(s+h)-value(s-h))/(2*h)
    errors.append(abs(observed-formula)/(1+abs(formula)))
results['lecture10_individual_wage_derivative'] = {
    'parameter_sets': 120, 'max_scaled_error': max(errors)}

# Concrete contradiction in the L09 overview figure: natural versus
# efficient gaps. This illustration uses u=.01 and kappa=.08.
kx, u, rho = .08, .01, .7
delta = u/kx
results['lecture09_svg_gap_counterexample'] = {
    'kappa_x': kx, 'u_t': u, 'natural_minus_efficient_gap': delta,
    'NKPC_extra_RHS_using_figure_natural_gap': kx*delta,
    'commitment_extra_LHS_when_u_changes_from_previous_period':
        (u-rho*u)/kx,
    'note': 'The figure uses x (natural gap), where the text requires x^e.'}

assert results['lecture08_structural_substitution']['max_abs_residual'] < 1e-10
assert results['lecture09_BK_root_counts'] == {'peg': [1], 'passive': [1], 'active': [2]}
assert results['lecture09_infinite_horizon_KKT']['max_abs_residual'] < 1e-10
assert results['lecture09_general_welfare_curvature']['max_relative_finite_difference_error'] < 1e-5
assert results['lecture10_individual_wage_derivative']['max_scaled_error'] < 1e-6

text = json.dumps(results, indent=2, ensure_ascii=False)
Path(__file__).with_name('checks.json').write_text(text+'\n')
print(text)
