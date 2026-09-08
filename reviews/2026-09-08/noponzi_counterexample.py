#!/usr/bin/env python3
"""Counterexample to the endogenous-SDF No-Ponzi restriction in lecture04.

Run: python3 noponzi_counterexample.py [output.json]

Only the Python standard library is needed. This is a unilateral household
deviation at fixed equilibrium prices, not a proposed market-clearing
equilibrium. It tests feasibility, not the Euler equation. The problem is that
lecture04.qmd defines the household's feasible set using its own candidate-path
marginal utility SDF. A candidate path can then erase its debt's discounted
value by making consumption (and debt) grow sufficiently quickly.

Parameters allowed by lecture04: alpha=0, gamma=1, phi=1, a_t=0.
At the intended steady equilibrium N=C=Y=W=1, D=V=0, R=1/beta.
Hold prices fixed and choose N_t=1, C_t=K*kappa**t, kappa>R.
Starting with B_{-1}=0, the budget is B_t=R*B_{t-1}+1-C_t.
The exact debt path is
 B_t=(R**(t+1)-1)/(R-1)
     -K*(kappa**(t+1)-R**(t+1))/(kappa-R).
Thus B_t ~ -K*kappa**(t+1)/(kappa-R).
For log utility, Q_{0,t}=beta**t*C_0/C_t=(beta/kappa)**t,
so Q_{0,t}*B_t -> 0, while B_t/R**t -> -infinity.
Every finite K has finite discounted utility, which rises without bound
as K -> infinity. Hence the stated feasibility restriction permits Ponzi
borrowing and does not define the intended household optimization problem.
"""

import json
import math
from pathlib import Path
import sys


def evaluate(scale, beta=0.96, growth=2.0, horizon=500):
    rate = 1.0 / beta
    assert 0 < beta < 1 and growth > rate
    income = 1.0
    debt = 0.0
    sample_dates = {0, 10, 50, 100, 200, horizon}
    rows = []
    max_scaled_budget_error = 0.0
    max_scaled_closed_form_error = 0.0
    for t in range(horizon + 1):
        consumption = scale * growth**t
        old_debt = debt
        debt = rate * old_debt + income - consumption
        closed_form = income * (rate**(t + 1) - 1) / (rate - 1)
        closed_form -= scale * (growth**(t + 1) - rate**(t + 1)) / (growth - rate)
        normalizer = max(1.0, abs(debt), consumption, abs(rate * old_debt))
        budget_error = abs(consumption + debt - rate * old_debt - income) / normalizer
        closed_form_error = abs(debt - closed_form) / normalizer
        max_scaled_budget_error = max(max_scaled_budget_error, budget_error)
        max_scaled_closed_form_error = max(max_scaled_closed_form_error, closed_form_error)
        if t in sample_dates:
            # Stable evaluation avoids multiplying very small Q by huge B.
            own_sdf_value = beta**t * scale * (debt / consumption)
            rows.append({
                "t": t,
                "consumption": consumption,
                "bond_position": debt,
                "own_marginal_utility_sdf": (beta / growth)**t,
                "own_sdf_discounted_bond_position": own_sdf_value,
                "market_discounted_bond_position": debt / rate**t,
            })
    assert max_scaled_budget_error < 1e-12
    assert max_scaled_closed_form_error < 1e-12
    assert rows[-1]["market_discounted_bond_position"] < -1e100
    assert abs(rows[-1]["own_sdf_discounted_bond_position"]) < 1e-6 * scale
    # phi=1, fixed labor N=1 implies period labor disutility 1/2.
    lifetime_utility = math.log(scale) / (1 - beta)
    lifetime_utility += beta * math.log(growth) / (1 - beta)**2
    lifetime_utility -= 0.5 / (1 - beta)
    return {
        "consumption_scale_K": scale,
        "discounted_lifetime_utility": lifetime_utility,
        "maximum_scaled_budget_residual": max_scaled_budget_error,
        "maximum_scaled_closed_form_residual": max_scaled_closed_form_error,
        "samples": rows,
    }


def main():
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix(".json")
    results = [evaluate(scale) for scale in (1.0, 10.0, 100.0)]
    assert results[0]["discounted_lifetime_utility"] < results[1]["discounted_lifetime_utility"]
    assert results[1]["discounted_lifetime_utility"] < results[2]["discounted_lifetime_utility"]
    report = {
        "source": "/Users/kenjimyzk/work/gradmacro2026/lecture04.qmd",
        "source_lines": [103, 126],
        "status": "verified_counterexample_to_feasibility_restriction",
        "parameters": {"alpha": 0, "gamma": 1, "phi": 1, "technology": 0,
                       "beta": 0.96, "R": 1 / 0.96, "kappa": 2.0,
                       "fixed_labor": 1, "wage": 1, "dividend_and_stock_price": 0,
                       "initial_bond_position_B_minus_1": 0},
        "interpretation": "A unilateral household deviation at fixed equilibrium prices; not a market-clearing equilibrium and not asserted to satisfy the Euler equation.",
        "analytical_limits": {
            "debt_asymptote": "B_t ~ -K*kappa^(t+1)/(kappa-R)",
            "candidate_own_sdf": "Q_0t=(beta/kappa)^t",
            "candidate_own_sdf_discounted_debt": "Q_0t*B_t ~ -K*kappa*beta^t/(kappa-R) -> 0",
            "market_discounted_debt": "B_t/R^t -> -infinity",
            "lifetime_utility": "log(K)/(1-beta)+beta*log(kappa)/(1-beta)^2-1/[2*(1-beta)]",
            "utility_supremum": "+infinity as K -> infinity; finite for every finite K",
        },
        "recommended_fix": "Define admissibility using an appropriate borrowing bound or given market state prices. Reserve the candidate marginal-utility SDF expression for an optimal-path transversality condition.",
        "cases": results,
    }
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_path.resolve()), "status": report["status"],
                      "cases_checked": len(results), "horizon": 500}, ensure_ascii=False))


if __name__ == "__main__":
    main()
