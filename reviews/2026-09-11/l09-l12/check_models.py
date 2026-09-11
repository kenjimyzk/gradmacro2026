"""Independent numerical checks of the live Lectures 9--12 (2026-09-11)."""
from pathlib import Path
import csv,json,sys
import numpy as np
out=Path(__file__).resolve().parent
rng=np.random.default_rng(20260911)
results={'python':sys.version,'numpy':np.__version__}
# L9: infinite-horizon solution versus exact extracted R finite-horizon code.
data=np.genfromtxt(out/'r-clean/lecture09-irf.csv',delimiter=',',names=True)
beta,k,omega,rho=.99,.08,20.,.7
B=1+beta+k*k*omega
lam=(B-np.sqrt(B*B-4*beta))/(2*beta)
eta=-k*omega/(1/lam-beta*rho)
prev=0.; xs=[]; ps=[]
for u in data['u']:
    x=lam*prev+eta*u; xs.append(x); ps.append(-(x-prev)/(k*omega)); prev=x
results['l09']={'max_finite_infinite_x_error':float(np.max(np.abs(data['x_C']-xs))),'first_21_x_error':float(np.max(np.abs(data['x_C'][:21]-xs[:21]))),'first_21_pi_error':float(np.max(np.abs(data['pi_C'][:21]-ps[:21]))),'finite_horizon_T':40,'stable_root':float(lam)}
assert results['l09']['first_21_x_error']<1e-6
# L10: identities, static inflation solution, and adjustment-loss lower bound.
max10=0
for i in range(600):
    g,v=rng.uniform(.2,5,2); kp,kw=rng.uniform(.005,.8,2)
    x,dw=rng.normal(0,.03,2)
    pp,pw=np.linalg.solve([[1/kp,1/kw],[-1,1]],[(g+v)*x,dw])
    pp_formula=kp*kw/(kp+kw)*(g+v)*x-kp/(kp+kw)*dw
    pw_formula=kp*kw/(kp+kw)*(g+v)*x+kw/(kp+kw)*dw
    max10=max(max10,abs(pp-pp_formula),abs(pw-pw_formula))
results['l10']={'cases':600,'max_static_formula_error':float(max10),'exercise6_pi_p':-1/1500,'exercise6_pi_w':1/750,'exercise7_min_loss':.001}
assert max10<1e-12
# L11: solve the primitive household, market-clearing, price, Euler and policy system.
# Vector: x, pi, cH, cS, nH, nS, w, d, r. Type S budget is checked separately.
max11=0; maxS=0; samples=[]
for i in range(600):
    g,v=rng.uniform(.3,4,2); l=rng.uniform(.03,.8); b=rng.uniform(.9,.999)
    phi=rng.uniform(1.05,2.5); rho=rng.uniform(0,.95); kx=rng.uniform(.01,.4)
    a,m,z=rng.normal(0,.01,3)
    zeta=(1+v)/(g+v); theta=1-l*v/(1-l)
    def residual(s):
        x,pi,ch,cs,nh,ns,w,d,r=s
        y=x+zeta*a; n=y-a
        return np.array([ch-w-nh-z,l*ch+(1-l)*cs-y,l*nh+(1-l)*ns-n,w-g*ch-v*nh,w-g*cs-v*ns,d-y+w+n,(1-b*rho)*pi-kx*x,r-(phi-rho)*pi+m,r-g*(rho-1)*cs])
    zero=residual(np.zeros(9)); mat=np.column_stack([residual(np.eye(9)[j])-zero for j in range(9)])
    s=np.linalg.solve(mat,-zero); x,pi,ch,cs,nh,ns,w,d,r=s
    rf=g*zeta*(rho-1)*a+g*l*v/((g+v)*(1-l))*(1-rho)*z
    den=kx/(1-b*rho)*(phi-rho)+g*theta*(1-rho)
    target=(m+rf)/den
    max11=max(max11,abs(x-target),np.max(np.abs(residual(s))))
    maxS=max(maxS,abs(cs-w-ns-d/(1-l)+l*z/(1-l)))
    if i<5: samples.append({'theta':theta,'x_primitive':x,'x_closed':target})
results['l11']={'cases':600,'max_formula_or_primitive_residual':float(max11),'max_redundant_typeS_budget_residual':float(maxS),'samples':samples}
assert max11<1e-10 and maxS<1e-10
# L12: distribution, PE intersection, multiplier and direct-effect decomposition.
max12=0
for i in range(400):
    b=rng.uniform(.9,.999);g,v=rng.uniform(.3,4,2);l=rng.uniform(.03,.8);p=rng.uniform(0,.95);tau=rng.uniform(0,.8)
    chi=1+v*(1-tau/l);theta=(1-l*chi)/(1-l)
    if abs(1-l*chi)<.01 or abs(1-b*p*(1-l*chi))<.01:continue
    wr=(1-b)/(1-b*p); wt=(1-b*(1-l*chi))/(1-b*p*(1-l*chi))
    dr=b/(g*(1-b*p));dt=(1-l)*b/(g*(1-b*p*(1-l*chi)))
    y=dt/(1-wt)*.01;ch=chi*y;cs=theta*y
    max12=max(max12,abs(y-(l*ch+(1-l)*cs)),abs(y-.01/(g*(1-p)*theta)),abs((dt/(1-wt))/(dr/(1-wr))-1/theta))
results['l12']={'draws':400,'max_identity_error':float(max12)}
assert max12<1e-9
b,p,l,chi=.99,.5,.3,2
results['l12']['direct_effect_counterexample']={'beta':b,'p':p,'lambda':l,'chi':chi,'actual_direct_ratio':(1-l)*(1-b*p)/(1-b*p*(1-l*chi)),'population_share':1-l,'actual_multiplier_ratio':(1-b*p*(1-l*chi))/((1-b*p)*(1-l*chi)),'total_ratio':(1-l)/(1-l*chi)}
(out/'model-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
