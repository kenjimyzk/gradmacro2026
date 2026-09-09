"""Independent nonlinear and finite-difference checks for graduate re-review.

No course inputs or distribution artifacts are changed.
"""
import itertools
import json
import math


def equilibrium(alpha, gamma, varphi, technology, spending, mc=1.0, tax=0.0):
    # Solve labour supply = labour demand from the level equations,
    # rather than using any coefficient given in the lecture notes.
    lower = (spending / math.exp(technology)) ** (1 / (1-alpha)) if spending else 0.0
    upper = max(1.0, 2 * lower)
    def residual(labour):
        output = math.exp(technology) * labour ** (1-alpha)
        consumption = output - spending
        wage = mc * (1-alpha) * math.exp(technology) * labour ** (-alpha)
        return labour ** varphi * consumption ** gamma - (1-tax) * wage
    while residual(upper) < 0:
        upper *= 2
    for _ in range(140):
        middle = (lower+upper)/2
        if residual(middle) > 0:
            upper = middle
        else:
            lower = middle
    labour = (lower+upper)/2
    output = math.exp(technology) * labour ** (1-alpha)
    consumption = output-spending
    wage = mc*(1-alpha)*math.exp(technology)*labour**(-alpha)
    return output, consumption, labour, wage


records = []
epsilon = 1e-5
for alpha, gamma, varphi, share in itertools.product(
        (0.0, 0.4, 0.8), (0.5, 1.0, 2.0), (0.5, 1.0, 2.0), (0.0, 0.2, 0.6)):
    denominator = varphi + alpha + gamma*(1-alpha)
    nbar = ((1-alpha)*(1-share)**(-gamma))**(1/denominator)
    ybar = nbar**(1-alpha)
    spending = share*ybar
    fiscal_denominator = (1-share)*(alpha+varphi)+gamma*(1-alpha)
    za = (1-share)*(1+varphi)/fiscal_denominator
    zg = gamma*(1-alpha)/fiscal_denominator
    expected_a = (za, za/(1-share), (za-1)/(1-alpha), (1-alpha*za)/(1-alpha))
    expected_g = (zg, (zg-1)/(1-share), zg/(1-alpha), -alpha*zg/(1-alpha))
    high = equilibrium(alpha, gamma, varphi, epsilon, spending)
    low = equilibrium(alpha, gamma, varphi, -epsilon, spending)
    actual_a = [(math.log(x)-math.log(y))/(2*epsilon) for x,y in zip(high,low)]
    # At G=0 use a forward derivative to stay within nonnegative spending.
    high = equilibrium(alpha, gamma, varphi, 0, spending+epsilon*ybar)
    low = equilibrium(alpha, gamma, varphi, 0, spending-epsilon*ybar if share else spending)
    scale = 2*epsilon if share else epsilon
    actual_g = [(math.log(x)-math.log(y))/scale for x,y in zip(high,low)]
    errors = [abs(x-y) for x,y in zip(actual_a, expected_a)] + [abs(x-y) for x,y in zip(actual_g, expected_g)]
    records.append(max(errors))

price_errors = []
for alpha, psi in itertools.product((0.0, 0.4, 0.8), (1.2, 3.0, 6.0)):
    # Profit derivative directly from the demand-substituted total cost.
    wage, aggregate_output, technology = 0.9, 1.2, 0.1
    exponent = psi/(1-alpha)
    cost_scale = wage*(aggregate_output/math.exp(technology))**(1/(1-alpha))
    for subsidy in (0.0, 1/(psi-1)):
        optimal_price = (exponent*cost_scale/((psi-1)*(1+subsidy)*aggregate_output))**(1/(exponent+1-psi))
        output = aggregate_output*optimal_price**(-psi)
        labour = (output/math.exp(technology))**(1/(1-alpha))
        marginal_cost = wage/((1-alpha)*math.exp(technology)*labour**(-alpha))
        price_errors.append(abs(optimal_price/marginal_cost - psi/((psi-1)*(1+subsidy))))

laffer_errors = []
for alpha, gamma, varphi in itertools.product((0.0, 0.4, 0.8), (0.5, 1.0, 2.0), (0.5, 1.0, 2.0)):
    denominator = varphi+alpha+gamma*(1-alpha)
    theta = (1-alpha)/denominator
    optimum = 1/(1+theta)
    def revenue(tax):
        _, _, n, wage = equilibrium(alpha, gamma, varphi, 0, 0, tax=tax)
        return tax*wage*n
    derivative = (revenue(optimum+epsilon)-revenue(optimum-epsilon))/(2*epsilon)
    laffer_errors.append(abs(derivative))

assert max(records) < 1e-5
assert max(price_errors) < 1e-12
assert max(laffer_errors) < 1e-7
result = {
    "verified": True,
    "nonlinear_equilibrium_parameter_cases": len(records),
    "maximum_log_derivative_error": max(records),
    "direct_profit_maximization_cases": len(price_errors),
    "maximum_price_markup_error": max(price_errors),
    "laffer_peak_cases": len(laffer_errors),
    "maximum_revenue_derivative_at_claimed_peak": max(laffer_errors),
    "two_state_equity_price": (0.8*1.5+1.2*0.5)/2,
    "two_state_covariance": 1-(5/3+5/9)/2,
}
print(json.dumps(result, indent=2))
