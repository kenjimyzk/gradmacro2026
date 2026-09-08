"""Independent finite-state audit of lecture04's stochastic verification proof.

Only Python's standard library is used. A two-state technology chain is an
AR(1) with rho=.7 and bounded, conditional-mean-zero innovations. Fixed-point
prices are solved as 2x2 linear systems, not copied from prior check code.
Finite adapted bond/share deviations all liquidate back to the candidate at
T=4; hence their entire lifetime utility difference is exactly finite horizon.
This is a numerical check, not a replacement for the manuscript's proof.
"""
import hashlib
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_suffix('.json')
TRANS = [[.85,.15],[.15,.85]]
TECH = [-.2,.2]


def solve2(a,b):
    det=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return [(b[0]*a[1][1]-a[0][1]*b[1])/det,
            (a[0][0]*b[1]-b[0]*a[1][0])/det]


def mv(a,v):
    return [sum(a[i][j]*v[j] for j in range(2)) for i in range(2)]


def utility(c,n,gamma):
    u=math.log(c) if gamma==1 else math.expm1((1-gamma)*math.log(c))/(1-gamma)
    return u-n*n/2


res={'source_hashes':{}, 'cases':[], 'summary':{}}
for name in ('lecture03.qmd','lecture04.qmd','solution.qmd'):
    res['source_hashes'][name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
pricing_residual=0.; budget_residual=0.; tangent_residual=0.;
max_gain=-math.inf; min_c=math.inf; min_asset=math.inf; tested=0
for alpha in (0.,.3):
  for gamma in (.5,1.,2.):
    for beta in (.96,.99):
      denom=1+alpha+gamma*(1-alpha)
      n=[((1-alpha)*math.exp((1-gamma)*a))**(1/denom) for a in TECH]
      c=[math.exp(a)*nn**(1-alpha) for a,nn in zip(TECH,n)]
      w=[(1-alpha)*math.exp(a)*nn**(-alpha) for a,nn in zip(TECH,n)]
      d=[alpha*cc for cc in c]
      m=[[TRANS[i][j]*beta*(c[j]/c[i])**(-gamma) for j in range(2)] for i in range(2)]
      r=[1/sum(row) for row in m]
      eye_minus_m=[[float(i==j)-m[i][j] for j in range(2)] for i in range(2)]
      v=solve2(eye_minus_m,mv(m,d))
      u=[utility(c[i],n[i],gamma) for i in range(2)]
      val=solve2([[float(i==j)-beta*TRANS[i][j] for j in range(2)] for i in range(2)],u)
      candidate_price_err=max(abs(v[i]-sum(m[i][j]*(v[j]+d[j]) for j in range(2))) for i in range(2))
      candidate_bond_err=max(abs(sum(m[i])*r[i]-1) for i in range(2))
      pricing_residual=max(pricing_residual,candidate_price_err,candidate_bond_err)
      tails={}
      vtail=v[:];qtail=[1.,1.]
      for horizon in range(1,2001):
        vtail=mv(m,vtail);qtail=mv(m,qtail)
        if horizon in (100,500,2000):
          tails[str(horizon)]={'discounted_equity':vtail[:],'expected_sdf':qtail[:]}
      case_gains=[]
      for state0 in range(2):
        for seed in range(25):
          rng=random.Random(seed)
          # Initial candidate stocks=1, bonds=0; all future draws are adapted.
          stack=[(0,state0,1.,0.,1.,None)]
          gain=0.; tangent=0.; finbudget=0.; wealth0=v[state0]+d[state0]
          max_local_budget=0.
          while stack:
            t,i,prob,bprev,thprev,iprev=stack.pop()
            if t==4:
              anow=v[i];thnow=1.
            else:
              anow=v[i]+.001*rng.uniform(-1,1)
              thnow=1.+.001*rng.uniform(-1,1)
            bnow=anow-v[i]*thnow
            wealth=(r[iprev]*bprev if t else 0.)+(v[i]+d[i])*thprev
            cn=wealth+w[i]*n[i]-anow
            assert cn>0 and anow>=-10
            min_c=min(min_c,cn);min_asset=min(min_asset,anow)
            err=cn+anow-wealth-w[i]*n[i]
            max_local_budget=max(max_local_budget,abs(err))
            q=beta**t*(c[i]/c[state0])**(-gamma)
            gain+=prob*beta**t*(utility(cn,n[i],gamma)-u[i])
            tangent+=prob*q*(cn-c[i])
            finbudget+=prob*q*(cn-w[i]*n[i])
            if t==4:
              finbudget+=prob*q*anow
            else:
              for j in range(2):
                stack.append((t+1,j,prob*TRANS[i][j],bnow,thnow,i))
          assert gain<=1e-11
          assert abs(tangent)<1e-11
          assert abs(finbudget-wealth0)<1e-10
          max_gain=max(max_gain,gain)
          tangent_residual=max(tangent_residual,abs(tangent))
          budget_residual=max(budget_residual,abs(finbudget-wealth0),max_local_budget)
          case_gains.append(gain);tested+=1
      res['cases'].append({'alpha':alpha,'gamma':gamma,'beta':beta,'C':c,'N':n,
            'R':r,'V':v,'lifetime_utility':val,'asset_price_residual':candidate_price_err,
            'bond_euler_residual':candidate_bond_err,'tail_checks':tails,
            'max_deviation_utility_gain':max(case_gains),
            'min_deviation_utility_gain':min(case_gains)})
res['summary']={'parameter_cases':len(res['cases']),'adapted_deviations':tested,
  'max_price_residual':pricing_residual,'max_finite_budget_residual':budget_residual,
  'max_expected_tangent_term':tangent_residual,'largest_utility_gain':max_gain,
  'minimum_consumption':min_c,'minimum_net_asset':min_asset,
  'credit_floor':-10.,'technology_innovation_conditional_mean_residual':max(abs(sum(TRANS[i][j]*(TECH[j]-.7*TECH[i]) for j in range(2))) for i in range(2)),
  'scope':'Finite-state stochastic algebra and 600 finite adapted deviations; no claim of exhaustive numerical optimality proof.'}
OUT.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res['summary'],indent=2))
