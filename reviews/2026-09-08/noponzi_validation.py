#!/usr/bin/env python3
"""Finite checks accompanying analytic fixed-credit-limit sufficiency proof."""
import json
import math
from pathlib import Path

L=10.0
counter=[]
for K in (1.0, 10.0, 100.0):
    beta=.96
    R=1/beta
    kappa=2.0
    B=0.0
    for t in range(100):
        B=R*B+1-K*kappa**t
        if B < -L:
            counter.append(dict(K=K,first_violation_t=t,B=B,limit=-L))
            break
    else:
        raise AssertionError('Old counterexample was not excluded')

steady=[]
for alpha in (0.0,.3):
  for gamma in (.5,1.0,2.0):
    for beta in (.96,.99):
      phi=1.0
      den=phi+alpha+gamma*(1-alpha)
      N=(1-alpha)**(1/den)
      C=N**(1-alpha)
      W=(1-alpha)*N**(-alpha)
      D=alpha*C
      R=1/beta
      V=beta*D/(1-beta)
      res=[N**phi*C**gamma-W, C-(W*N+D), 1-beta*R, V-beta*(V+D)]
      assert max(map(abs,res))<1e-12
      assert V+L>0
      tail=beta**10000*V
      assert tail<1e-30
      def u(c):
          return math.log(c) if gamma==1 else (c**(1-gamma)-1)/(1-gamma)
      deviations=[]
      for sign in (-1,1):
        delta=sign*min(C/(4*R),L/4)
        C0=C+delta
        C1=C-R*delta
        B0=-delta
        B1=0.0
        assert min(C0,C1)>0 and min(B0+V,B1+V)>-L
        budget0=C0+B0+V-(V+D+W*N)
        budget1=C1+B1+V-(R*B0+V+D+W*N)
        telescope=(C0-C)+beta*(C1-C)+beta*B1
        gap=(u(C0)-u(C))+beta*(u(C1)-u(C))
        assert max(abs(budget0),abs(budget1),abs(telescope))<1e-12
        assert gap<0
        deviations.append(dict(delta=delta,utility_gap=gap,budget_residual=max(abs(budget0),abs(budget1)),telescope_residual=abs(telescope)))
      steady.append(dict(alpha=alpha,gamma=gamma,beta=beta,N=N,C=C,W=W,D=D,R=R,V=V,credit_limit_slack=V+L,max_equilibrium_residual=max(map(abs,res)),T10000_equity_terminal=tail,deviations=deviations))
result=dict(status='verified finite numerical checks; infinite limits proven analytically in accompanying note',credit_limit_L=L,counterexample_exclusions=counter,steady_equilibria=steady)
print(json.dumps(result,ensure_ascii=False,indent=2))
