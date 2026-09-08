"""Independently check the revised deterministic two-period lecture-10 exercise.

Periods are 0 and 1, s_1 = mc_0, d_1 = 0, and all period-2 private
expectations and continuation loss are zero. Future policy functions are
held fixed during a one-shot period-0 deviation; their state arguments move.

The proposed scalar formulas are compared with a constrained quadratic
program solved through its full KKT linear system. This script uses only
the Python standard library and also compares the baseline with the
previous two-period counterexample. It does not test an infinite-horizon
fixed point, stochastic policy functions, or equilibrium uniqueness.

Run from the repository root:
  python3 reviews/2026-09-09/check_updated_exercises.py \
    --output reviews/2026-09-09/check_updated_exercises.json
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys


def solve_linear(matrix, rhs):
    """Partial-pivot Gaussian elimination, independent of scalar formulas."""
    rows = [list(row) + [value] for row, value in zip(matrix, rhs)]
    size = len(rhs)
    for col in range(size):
        pivot = max(range(col, size), key=lambda row: abs(rows[row][col]))
        assert abs(rows[pivot][col]) > 1e-14
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [value / divisor for value in rows[col]]
        for row in range(size):
            if row != col:
                multiplier = rows[row][col]
                rows[row] = [a - multiplier * b
                             for a, b in zip(rows[row], rows[col])]
    return [row[-1] for row in rows]


def solve_constrained_loss(hessian_diagonal, constraints, rhs):
    """Minimize .5 y'Dy subject to Ay=b; y=(price,wage,x,mc)."""
    n, count = len(hessian_diagonal), len(rhs)
    matrix = [[0.0] * (n + count) for _ in range(n + count)]
    for index, value in enumerate(hessian_diagonal):
        matrix[index][index] = value
    for row, coefficients in enumerate(constraints):
        for col, value in enumerate(coefficients):
            matrix[n + row][col] = value
            matrix[col][n + row] = value
    right = [0.0] * n + list(rhs)
    solution = solve_linear(matrix, right)
    residual = max(abs(sum(a * b for a, b in zip(row, solution)) - value)
                   for row, value in zip(matrix, right))
    return solution[:n], residual


def check_case(parameters, s0, d0):
    beta, kp, kw = (parameters[key] for key in ("beta", "kp", "kw"))
    gamma, phi = (parameters[key] for key in ("gamma", "phi"))
    wp, ww = (parameters[key] for key in ("wp", "ww"))
    K = kw * (gamma + phi)
    A = 1 + kp + kw
    H = A**2 / K**2 + wp * kp**2 + ww * (1 + kp)**2
    h = (A / K**2 + ww * (1 + kp)) / H
    ap, aw, ax = kp * h, (1 + kp) * h - 1, (A * h - 1) / K
    P = ax**2 + wp * ap**2 + ww * aw**2

    # Independent terminal problem at state s=1. The RHS contains -s,
    # and the current-mc cost weight is zero at the terminal date.
    terminal_constraints = [[1, 0, 0, -kp], [0, 1, -K, kw],
                            [-1, 1, 0, -1]]
    terminal_solution, terminal_kkt = solve_constrained_loss(
        [wp, ww, 1, 0], terminal_constraints, [0, 0, -1])
    terminal_formula_error = max(abs(a - b) for a, b in
                                 zip(terminal_solution, [ap, aw, ax, h]))
    terminal_kkt_value_curvature = (wp * terminal_solution[0]**2
                                   + ww * terminal_solution[1]**2
                                   + terminal_solution[2]**2)

    # At date 0 the intercept depends on both inherited mc and the shock.
    b = d0 - s0
    kp_eff, kw_eff = kp + beta * ap, kw - beta * aw
    xp = (1 + kp_eff + kw_eff) / K
    D = xp**2 + wp * kp_eff**2 + ww * (1 + kp_eff)**2 + beta * P
    m0 = -b * (xp / K + ww * (1 + kp_eff)) / D
    p0, w0, x0 = kp_eff * m0, (1 + kp_eff) * m0 + b, xp * m0 + b / K
    first_constraints = [[1, 0, 0, -kp_eff], [0, 1, -K, kw_eff],
                         [-1, 1, 0, -1]]
    first_solution, first_kkt = solve_constrained_loss(
        [wp, ww, 1, beta * P], first_constraints, [0, 0, b])
    first_formula_error = max(abs(a - b) for a, b in
                              zip(first_solution, [p0, w0, x0, m0]))

    def allocation_and_total_loss(m):
        # Reconstruct both periods directly from the three private
        # constraints and the terminal policy. No reduced value function
        # is used in this objective evaluation.
        m1 = h * m
        p1 = kp * m1
        w1 = m1 - m + p1
        x1 = (w1 + kw * m1) / K
        p = kp * m + beta * p1
        w = m - s0 + d0 + p
        x = (w + kw * m - beta * w1) / K
        loss = 0.5 * (x*x + wp*p*p + ww*w*w)
        loss += 0.5 * beta * (x1*x1 + wp*p1*p1 + ww*w1*w1)
        return (p, w, x, m1, p1, w1, x1), loss

    allocation, optimum_loss = allocation_and_total_loss(m0)
    _, _, _, m1, p1, w1, x1 = allocation
    eps = 1e-5
    finite_difference = (allocation_and_total_loss(m0 + eps)[1]
                         - allocation_and_total_loss(m0 - eps)[1]) / (2 * eps)
    analytic_derivative = (x0 * xp + wp * p0 * kp_eff
                           + ww * w0 * (1 + kp_eff) + beta * P * m0)
    terminal_derivative = (x1 * A / K + wp * p1 * kp
                           + ww * w1 * (1 + kp))
    deviations = [-0.003, 0.003]
    deviation_identity_error = max(
        abs(allocation_and_total_loss(m0 + delta)[1] - optimum_loss
            - 0.5 * D * delta**2) for delta in deviations)
    assert D > 0 and H > 0
    assert all(allocation_and_total_loss(m0 + delta)[1] > optimum_loss
               for delta in deviations)

    # Real rates are freely chosen; natural rates are given exogenously.
    # At date 1, E x_2 = E pi^p_2 = 0 by the exercise's terminal closure.
    rf0, rf1 = 0.005, -0.002
    r0, r1 = rf0 + gamma * (x1 - x0), rf1 - gamma * x1
    nominal0, nominal1 = r0 + p1, r1
    constraints = {
        "date0_price_pc": p0 - kp * m0 - beta * p1,
        "date0_wage_pc": w0 - K * x0 + kw * m0 - beta * w1,
        "date0_wage_identity": w0 - (m0 - s0 + d0 + p0),
        "date0_is": x0 - x1 + (r0 - rf0) / gamma,
        "date0_fisher": nominal0 - r0 - p1,
        "date1_price_pc": p1 - kp * m1,
        "date1_wage_pc": w1 - K * x1 + kw * m1,
        "date1_wage_identity": w1 - (m1 - m0 + p1),
        "date1_is": x1 + (r1 - rf1) / gamma,
        "date1_fisher": nominal1 - r1,
    }
    Gamma = beta * P * m0
    l2 = -x0 / K
    l3 = ww * w0 - l2
    l1 = wp * p0 + l3
    corrected_foc = kp_eff * l1 - kw_eff * l2 + l3 + Gamma
    target = ((1 + kp_eff + kw_eff) * x0
              + K * (kp_eff * wp * p0 + (1 + kp_eff) * ww * w0 + Gamma))
    old_foc = kp * l1 - kw * l2 + l3 + Gamma
    missing = beta * (ap * l1 + aw * l2)
    metrics = {
        "terminal_coefficients_vs_kkt": terminal_formula_error,
        "terminal_value_curvature_vs_kkt": abs(P - terminal_kkt_value_curvature),
        "date0_allocation_vs_kkt": first_formula_error,
        "max_kkt_residual": max(terminal_kkt, first_kkt),
        "max_private_constraint_and_implementation_residual": max(map(abs, constraints.values())),
        "date0_analytic_objective_derivative": abs(analytic_derivative),
        "date0_centered_finite_difference_derivative": abs(finite_difference),
        "terminal_objective_derivative": abs(terminal_derivative),
        "one_shot_loss_curvature_identity": deviation_identity_error,
        "corrected_mc_foc": abs(corrected_foc),
        "corrected_target": abs(target),
        "old_foc_plus_missing_vs_corrected": abs(old_foc + missing - corrected_foc),
    }
    assert max(metrics.values()) < 1e-9, metrics
    return {
        "parameters": parameters, "initial_state": s0, "technology_change_0": d0,
        "technology_change_1": 0.0,
        "terminal_coefficients": {"H": H, "h": h, "a_p": ap, "a_w": aw, "a_x": ax, "P": P},
        "date0": {"mc": m0, "price": p0, "wage": w0, "x": x0, "Gamma": Gamma,
                  "real_rate": r0, "nominal_rate": nominal0, "natural_rate": rf0},
        "date1": {"state": m0, "mc": m1, "price": p1, "wage": w1, "x": x1,
                  "real_rate": r1, "nominal_rate": nominal1, "natural_rate": rf1},
        "private_constraint_residuals": constraints,
        "verification": metrics,
        "positive_objective_curvatures": {"terminal": H, "date0": D},
        "old_incomplete_mc_foc": old_foc,
        "missing_expectation_derivative_terms": missing,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    parameter_sets = [
        dict(beta=.99, kp=.1, kw=.1, gamma=1.0, phi=1.0, wp=30.0, ww=30.0),
        dict(beta=.96, kp=.3, kw=.2, gamma=2.0, phi=.5, wp=8.0, ww=12.0),
        dict(beta=.98, kp=.05, kw=.4, gamma=1.5, phi=1.5, wp=40.0, ww=5.0),
    ]
    # All three new scenarios have nonzero inherited state and shock;
    # d0-s0 is also nonzero, avoiding the trivial zero-allocation case.
    cases = [check_case(parameters, state, shock)
             for parameters, state, shock in zip(parameter_sets,
                [.012, -.02, .015], [.007, .01, -.01])]
    baseline = check_case(parameter_sets[0], 0.0, .01)
    legacy_script = Path(__file__).resolve().parents[1] / "2026-09-08" / "markov_counterexample.py"
    legacy = json.loads(subprocess.check_output([sys.executable, str(legacy_script)], text=True))
    mapping = {"h": "mc", "a_x": "x", "a_p": "price", "a_w": "wage", "P": "value_curvature"}
    comparison_errors = [abs(baseline["terminal_coefficients"][new]
                             - legacy["terminal_policy_slopes"][old])
                         for new, old in mapping.items()]
    for key in ("mc", "x", "price", "wage"):
        comparison_errors.append(abs(baseline["date0"][key]
                                     - legacy["true_period_0_markov_optimum"][key]))
    legacy_error = max(comparison_errors)
    assert legacy_error < 1e-12
    metric_names = cases[0]["verification"]
    maxima = {key: max(case["verification"][key] for case in cases + [baseline])
              for key in metric_names}
    result = {
        "status": "PASS",
        "scope": "Deterministic two-period discretion; d1=0; zero date-2 expectations and continuation; freely chosen real rates.",
        "method": "Proposed scalar solution versus independent full KKT solve, direct two-period loss finite differences, all private constraints, IS/Fisher implementation, and historical counterexample.",
        "limitations": "No infinite-horizon, stochastic, existence, or equilibrium-uniqueness claim.",
        "new_nonzero_state_and_shock_cases": cases,
        "legacy_baseline_comparison": {"max_difference": legacy_error, "case": baseline},
        "maxima_across_all_cases": maxima,
        "maximum_checked_residual": max(maxima.values()),
    }
    encoded = json.dumps(result, indent=2) + "\n"
    if arguments.output:
        arguments.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
