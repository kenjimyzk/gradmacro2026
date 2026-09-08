"""Exact rational checks of lecture03 time indices and expectation treatment."""
from fractions import Fraction as F
import json
import math
from pathlib import Path

r0,r1=F(11,10),F(6,5)
# Conditional means equal one. Future innovation support depends on first state.
e1=[F(1,2),F(3,2)]
e2=[[F(3,10),F(17,10)],[F(4,5),F(6,5)]]
q01=[e/r0 for e in e1]
q12=[[e/r1 for e in row] for row in e2]
q02=[q01[i]*q12[i][j] for i in range(2) for j in range(2)]
assert sum(q01)/2==1/r0
assert all(sum(row)/2==1/r1 for row in q12)
assert sum(q02)/4==1/(r0*r1)
# Deterministic D1=D2=1 with post-D2 price zero.
v1=1/r1
v0_euler=sum(q*(1+v1) for q in q01)/2
v0_pv=1/r0+1/(r0*r1)
assert v0_euler==v0_pv
# Exercise 5.
q=[F(4,5),F(6,5)];payoff=[F(3,2),F(1,2)]
price=sum(q[i]*payoff[i] for i in range(2))/2
returns=[v/price for v in payoff]
rf=1/(sum(q)/2);ere=sum(returns)/2
cov=sum(q[i]*returns[i] for i in range(2))/2-(sum(q)/2)*ere
assert price==F(9,10) and ere==F(10,9) and cov==F(-1,9)
assert ere-rf==-rf*cov
# The literal sequential-budget-only problem admits Ponzi plans; the earlier
# NPG rule excludes them. This illustrates why recursive admissibility must
# be inherited; it is not a counterexample to the correctly restricted problem.
beta=.96;r=1/beta;k=2.
b=0.;budget_err=0.
for t in range(20):
    bnew=r*b+1-k
    budget_err=max(budget_err,abs(k+bnew-r*b-1))
    b=bnew
result={
  'deterministic_rate_random_sdf':{
    'R0':str(r0),'R1':str(r1),'Q02_possible_values':list(map(str,q02)),
    'EQ02':str(sum(q02)/4),'discount_product_inverse':str(1/(r0*r1)),
    'stock_price_from_one_step':str(v0_euler),'stock_price_from_PV':str(v0_pv)},
  'l03_exercise5':{'stock_price':str(price),'riskfree_gross_return':str(rf),
    'expected_stock_return':str(ere),'covariance':str(cov)},
  'recursive_admissibility_illustration':{'scope':'Clarification only: respects sequential budget, violates inherited NPG.',
    'constant_consumption':k,'beta':beta,'R':r,'constant_income':1,
    'lifetime_log_utility':math.log(k)/(1-beta),
    'discounted_debt_limit':(1-k)*r/(r-1),'budget_residual':budget_err}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
