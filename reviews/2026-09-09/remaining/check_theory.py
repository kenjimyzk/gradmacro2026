#!/usr/bin/env python3
"""Independent numerical and source-preservation checks for the remaining fixes.
Run: python3 reviews/2026-09-09/remaining/check_theory.py
No lecture or answer source is changed by this script.
"""
from pathlib import Path
import hashlib
import itertools
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def check_protected():
    expected = json.loads((HERE / 'solution_protected_sha_before.json').read_text())
    text = (ROOT / 'solution.qmd').read_text()
    result = {}
    for title, before in expected.items():
        section = text.split(title, 1)[1].split('\n# 第', 1)[0]
        after = sha(section)
        result[title] = {'before_sha256': before, 'after_sha256': after,
                         'unchanged': after == before}
        assert after == before, title
    return result


def check_price():
    cases = 0
    max_foc = 0.
    max_cost_identity = 0.
    for alpha, Y, W, a, psi in itertools.product(
            [0., .3, .7], [.8, 1.2], [.7, 1.4], [-.2, .2], [3., 6.]):
        b = 1-alpha
        markup = psi/(psi-1)
        # Solve s = markup * TC'(Y*s**(-psi)) analytically.
        optimum = (markup*(W/b)*math.exp(-a/b)*Y**(alpha/b))**(1/(1+psi*alpha/b))
        def q(s): return Y*s**(-psi)
        def tc(qty): return W*(qty/math.exp(a))**(1/b)
        def mc(qty): return W/b*math.exp(-a/b)*qty**(alpha/b)
        def profit(s): return s*q(s)-tc(q(s))
        h = optimum*1e-5
        numerical_derivative = (profit(optimum+h)-profit(optimum-h))/(2*h)
        max_foc = max(max_foc, abs(numerical_derivative)/max(q(optimum), 1))
        assert abs(optimum-markup*mc(q(optimum))) < 1e-10
        assert profit(optimum) > profit(optimum*.99)
        assert profit(optimum) > profit(optimum*1.01)
        cost_residual = abs(tc(q(optimum))-b*mc(q(optimum))*q(optimum))
        max_cost_identity = max(max_cost_identity, cost_residual)
        assert cost_residual < 1e-10
        cases += 1
    assert max_foc < 1e-6
    return {'cases': cases, 'max_normalized_finite_difference_foc': max_foc,
            'max_total_cost_identity_residual': max_cost_identity,
            'local_maximum_comparison': 'passed at 0.99 and 1.01 times each optimum'}


def check_sdf():
    # Each one-period SDF is Z/R with E[Z]=1; the positive random Z is
    # consistent with a stochastic marginal utility via UC_next=UC*Z/(beta*R).
    # Thus risk-free rates are deterministic while the SDF is not.
    rates = [1.03, 1.04, 1.02, 1.05]
    dividends = [1., .9, 1.1, 1.2]
    sdf_values = [1.]
    max_residual = 0.
    pv = 0.
    for i, R in enumerate(rates):
        sdf_values = [q*z/R for q in sdf_values for z in [.6, 1.4]]
        expected_sdf = sum(sdf_values)/len(sdf_values)
        required = 1/math.prod(rates[:i+1])
        max_residual = max(max_residual, abs(expected_sdf-required))
        pv += dividends[i]*expected_sdf
    deterministic_pv = sum(d/math.prod(rates[:i+1]) for i, d in enumerate(dividends))
    assert max_residual < 1e-14
    assert abs(pv-deterministic_pv) < 1e-14
    return {'periods': len(rates), 'terminal_sdf_distinct_values': len(set(sdf_values)),
            'max_expected_sdf_residual': max_residual,
            'finite_dividend_pv_residual': abs(pv-deterministic_pv),
            'scope': 'finite stochastic tree checks the conditional-expectation induction; infinite PV uses the stated no-bubble and convergence conditions'}


def check_welfare():
    cases = 0
    max_output_error = 0.
    max_inflation_error = 0.
    for alpha, gy, gamma, phi, Y, a in itertools.product(
            [0., .3, .7], [0., .2, .45], [.5, 1., 2.], [.5, 1.], [.8, 1.3], [-.2, .2]):
        b = 1-alpha
        G = gy*Y
        C = Y-G
        N = (Y/math.exp(a))**(1/b)
        uc = C**(-gamma)
        # Choose nu so this arbitrary positive steady state is efficient.
        nu = b*uc*Y/N**(1+phi)
        eta = 6.
        def utility(log_output, inflation):
            output = Y*math.exp(log_output)
            consumption = output*(1-eta*inflation**2/2)-G
            labor = (output/math.exp(a))**(1/b)
            u = math.log(consumption) if gamma == 1 else (consumption**(1-gamma)-1)/(1-gamma)
            return u-nu*labor**(1+phi)/(1+phi)
        h = 1e-4
        base = utility(0., 0.)
        loss_curvature_y = -(utility(h, 0.)-2*base+utility(-h, 0.))/(h*h*uc*Y)
        loss_curvature_pi = -(utility(0., h)-2*base+utility(0., -h))/(h*h*uc*Y)
        target_y = gamma/(1-gy)+(phi+alpha)/b
        max_output_error = max(max_output_error, abs(loss_curvature_y-target_y)/target_y)
        max_inflation_error = max(max_inflation_error, abs(loss_curvature_pi-eta)/eta)
        assert abs(uc*Y-nu*N**(1+phi)/b) < 1e-12
        cases += 1
    assert max_output_error < 1e-6
    assert max_inflation_error < 1e-6
    return {'cases': cases, 'max_relative_output_curvature_error': max_output_error,
            'max_relative_inflation_curvature_error': max_inflation_error,
            'scope': 'curvature at efficient steady states with fixed contemporaneous technology and government spending; analytic completion of the square supplies x_e under shocks'}


def check_polynomial():
    cases = 0
    max_residual = 0.
    for beta, kappa, gamma in itertools.product([.9, .99], [.03, .08, .2], [1., 2., 3.]):
        trace = 1+1/beta+kappa/(beta*gamma)
        determinant = 1/beta
        q1 = 1-trace+determinant
        max_residual = max(max_residual, abs(q1+kappa/(beta*gamma)))
        disc = trace**2-4*determinant
        roots = ((trace-math.sqrt(disc))/2, (trace+math.sqrt(disc))/2)
        assert 0 < roots[0] < 1 < roots[1]
        cases += 1
    text = (ROOT / 'lecture09.qmd').read_text()
    assert r'\kappa_x\omega_p\pi_1+x_1^e-x_0^e=0' in text
    assert r'\kappa_x\omega_p\pi_1+x_1^e=0' in text
    assert r'q_0(\lambda)' in text and r'q_0(1)' in text and r'q_0(0)' in text
    assert r'x_0^e(\lambda)' not in text
    return {'peg_cases': cases, 'max_q_at_one_residual': max_residual,
            'one_root_in_0_1_and_one_above_1': True,
            'welfare_gap_superscripts_and_polynomial_notation': 'verified in source'}


def main():
    output = {
        'status': 'verified',
        'protected_solution_sections': check_protected(),
        'price_setting': check_price(),
        'is_positive_gap_example_residual': .005-(.009-.004),
        'deterministic_rates_stochastic_sdf': check_sdf(),
        'welfare_normalization': check_welfare(),
        'time_consistency_and_peg_polynomial': check_polynomial(),
        'source_sha256': {name: sha((ROOT/name).read_text()) for name in
                          ['solution.qmd', 'lecture07.qmd', 'lecture03.qmd', 'lecture09.qmd']},
        'render_check': 'not run by this validator; parent agent performs rendering and visual checks'
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
