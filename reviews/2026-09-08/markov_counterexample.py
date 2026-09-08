"""Two-period Markov-discretion check of lecture10.qmd 1964-1981.

There are two periods, 0 and 1. Period 1 is terminal: all period-2
expectations and continuation losses are zero. The period-0 government
takes the terminal policy FUNCTIONS as given and internalizes their
dependence on mc_0, the next endogenous state. All constraints and loss
weights are those in lecture10, with no extra shocks after period 0.

No third-party packages are required. Run: python3 markov_counterexample.py
"""

import json


beta = 0.99
kappa_p = kappa_w = 0.1
gamma_plus_varphi = 2.0
omega_p = omega_w = 30.0  # psi_p=psi_w=6, eta_p=eta_w=60
technology_change_0 = 0.01
technology_change_1 = 0.0
initial_mc = 0.0
assert technology_change_1 == initial_mc == 0.0

Kx = kappa_w * gamma_plus_varphi

# Terminal constraints, where s=mc_0 and m=mc_1:
# pi_p = kappa_p*m; pi_w = (1+kappa_p)*m-s;
# x = [(1+kappa_p+kappa_w)*m-s]/Kx.
# Substitute into the quadratic terminal loss and solve d(loss)/dm=0.
A = 1 + kappa_p + kappa_w
terminal_quadratic_m = (
    A**2 / Kx**2 + omega_p * kappa_p**2 + omega_w * (1 + kappa_p)**2
)
mc_state_slope = (
    A / Kx**2 + omega_w * (1 + kappa_p)
) / terminal_quadratic_m
x_state_slope = (A * mc_state_slope - 1) / Kx
price_state_slope = kappa_p * mc_state_slope
wage_state_slope = (1 + kappa_p) * mc_state_slope - 1
value_curvature = (
    x_state_slope**2
    + omega_p * price_state_slope**2
    + omega_w * wage_state_slope**2
)

# Period 0: substitute the known terminal policy functions into BOTH
# Phillips constraints. This reduces the true Markov best-response
# objective to one quadratic in mc_0.
price_mc_slope_0 = kappa_p + beta * price_state_slope
x_mc_slope_0 = (
    1 + price_mc_slope_0 + kappa_w - beta * wage_state_slope
) / Kx
mc_0 = -(
    x_mc_slope_0 * technology_change_0 / Kx
    + omega_w * (1 + price_mc_slope_0) * technology_change_0
) / (
    x_mc_slope_0**2
    + omega_p * price_mc_slope_0**2
    + omega_w * (1 + price_mc_slope_0)**2
    + beta * value_curvature
)
x_0 = x_mc_slope_0 * mc_0 + technology_change_0 / Kx
price_0 = price_mc_slope_0 * mc_0
wage_0 = (1 + price_mc_slope_0) * mc_0 + technology_change_0
Gamma_mc = beta * value_curvature * mc_0  # exactly beta*V_s, as in notes

lambda_2 = -x_0 / Kx
lambda_3 = omega_w * wage_0 - lambda_2
lambda_1 = omega_p * price_0 + lambda_3
lecture_mc_foc = (
    kappa_p * lambda_1 - kappa_w * lambda_2 + lambda_3 + Gamma_mc
)
missing_expectation_derivatives = beta * (
    price_state_slope * lambda_1 + wage_state_slope * lambda_2
)
correct_mc_foc = lecture_mc_foc + missing_expectation_derivatives
lecture_target_residual = (
    (1 + kappa_p + kappa_w) * x_0
    + Kx * (
        kappa_p * omega_p * price_0
        + (1 + kappa_p) * omega_w * wage_0
        + Gamma_mc
    )
)

def actual_loss(m):
    p = price_mc_slope_0 * m
    w = (1 + price_mc_slope_0) * m + technology_change_0
    x = x_mc_slope_0 * m + technology_change_0 / Kx
    return 0.5 * (
        x*x + omega_p*p*p + omega_w*w*w + beta*value_curvature*m*m
    )

eps = 1e-7
finite_difference_derivative = (actual_loss(mc_0 + eps) - actual_loss(mc_0 - eps)) / (2 * eps)
constraint_residuals = [
    price_0 - kappa_p*mc_0 - beta*price_state_slope*mc_0,
    wage_0 - Kx*x_0 + kappa_w*mc_0 - beta*wage_state_slope*mc_0,
    wage_0 - mc_0 - technology_change_0 - price_0,
]
assert max(abs(x) for x in constraint_residuals) < 1e-12
assert abs(correct_mc_foc) < 1e-12
assert abs(finite_difference_derivative) < 1e-9
assert abs(lecture_mc_foc) > 1e-3

results = {
    "parameters": {
        "beta": beta, "kappa_p": kappa_p, "kappa_w": kappa_w,
        "gamma_plus_varphi": gamma_plus_varphi,
        "omega_p": omega_p, "omega_w": omega_w,
        "initial_mc": initial_mc, "technology_change_0": technology_change_0,
        "technology_change_1": technology_change_1,
    },
    "terminal_policy_slopes": {
        "mc": mc_state_slope, "x": x_state_slope,
        "price": price_state_slope, "wage": wage_state_slope,
        "value_curvature": value_curvature,
    },
    "true_period_0_markov_optimum": {
        "mc": mc_0, "x": x_0, "price": price_0,
        "wage": wage_0, "Gamma_mc_beta_Vs": Gamma_mc,
    },
    "verification": {
        "max_constraint_residual": max(abs(x) for x in constraint_residuals),
        "lecture_mc_foc_residual": lecture_mc_foc,
        "missing_expectation_derivatives": missing_expectation_derivatives,
        "correct_mc_foc_residual": correct_mc_foc,
        "lecture_target_condition_residual": lecture_target_residual,
        "actual_loss_finite_difference_derivative": finite_difference_derivative,
    },
}
print(json.dumps(results, indent=2))
