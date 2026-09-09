"""Check the added TVC example and stochastic government-budget iteration."""
from fractions import Fraction as F
import json

R = F(26, 25)
income = F(1)
initial_assets = F(5)
tvc_cases = []
for consumption in (F(11, 10), F(6, 5), F(13, 10)):
    limit = R / (R-1) * (income + (R-1)*initial_assets-consumption)
    assets = float(initial_assets)
    for _ in range(1000):
        assets = float(R)*assets + float(income-consumption)
    terminal = assets/float(R)**999
    assert abs(terminal-float(limit)) < 1e-10
    tvc_cases.append({
        "consumption": float(consumption),
        "discounted_asset_limit": float(limit),
        "sequential_budget_error_at_N_999": abs(terminal-float(limit)),
        "no_ponzi": limit >= 0,
        "tvc": limit == 0,
    })

# A two-period tree with state-dependent inflation and discount factors.
# Nominal rates are obtained from the bond Euler equation at each node.
p = (F(2, 5), F(3, 5))
q = (F(9, 10), F(11, 10))
inflation = (F(49, 50), F(51, 50))
debt0 = F(4, 5)
debt1 = (F(1, 2), F(11, 10))
rate0 = 1 / sum(p[i]*q[i]/inflation[i] for i in range(2))
surplus1 = tuple(rate0/inflation[i]*debt0-debt1[i] for i in range(2))
conditional_p = ((F(1, 3), F(2, 3)), (F(1, 2), F(1, 2)))
conditional_q = ((F(4, 5), F(6, 5)), (F(9, 10), F(11, 10)))
conditional_inflation = ((F(97, 100), F(103, 100)), (F(101, 100), F(99, 100)))
debt2 = ((F(3, 10), F(7, 10)), (F(4, 5), F(13, 10)))
surplus2_value = F(0)
terminal_value = F(0)
for i in range(2):
    rate1 = 1/sum(conditional_p[i][j]*conditional_q[i][j]/conditional_inflation[i][j] for j in range(2))
    for j in range(2):
        surplus2 = rate1/conditional_inflation[i][j]*debt1[i]-debt2[i][j]
        weight = p[i]*conditional_p[i][j]*q[i]*conditional_q[i][j]
        surplus2_value += weight*surplus2
        terminal_value += weight*debt2[i][j]
one_period = sum(p[i]*q[i]*(debt1[i]+surplus1[i]) for i in range(2))
two_period = sum(p[i]*q[i]*surplus1[i] for i in range(2)) + surplus2_value + terminal_value
assert one_period == debt0
assert two_period == debt0
print(json.dumps({
    "verified": True,
    "tvc_cases": tvc_cases,
    "government_one_period_residual_exact": str(one_period-debt0),
    "government_two_period_residual_exact": str(two_period-debt0),
}, indent=2))
