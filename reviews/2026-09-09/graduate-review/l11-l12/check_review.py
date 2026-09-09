"""Recheck current TANK equations and compare claimed calibrations with SVG geometry."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
rng = np.random.default_rng(120926)
max_error = dict(l11_closed_vs_primitive=0.0, l12_closed_vs_primitive=0.0,
                 l12_PE_vs_euler=0.0, l12_slope_difference_identity=0.0)

def solve(beta, gamma, varphi, lam, kp, policy, persistence, a, m, z, tau=None, r_given=None):
    # y,cH,cS,nH,nS,w,d,pi,r. No reduced IS/distribution equation is used.
    rows, rhs = [], []
    def eq(coefs, value=0):
        row = np.zeros(9)
        for j, c in coefs.items():
            row[j] = c
        rows.append(row)
        rhs.append(value)
    eq({0:-1,1:lam,2:1-lam})
    eq({0:-1,3:lam,4:1-lam},-a)
    eq({5:1,1:-gamma,3:-varphi})
    eq({5:1,2:-gamma,4:-varphi})
    hbudget={1:1,5:-1,3:-1}
    if tau is not None:
        hbudget[6]=-tau/lam
    eq(hbudget,z)
    eq({6:1,0:-1,5:1,3:lam,4:1-lam})
    eq({7:1-beta*persistence,5:-kp},-kp*a)
    if r_given is None:
        eq({8:1,7:-(policy-persistence)},-m)
    else:
        eq({8:1},r_given)
    eq({8:1,2:gamma*(1-persistence)})
    ans=np.linalg.solve(rows,rhs)
    transfer=z if tau is None else tau/lam*ans[6]
    sbudget=ans[2]-ans[5]-ans[4]-ans[6]/(1-lam)+lam*transfer/(1-lam)
    assert abs(sbudget)<1e-9
    return ans

for i in range(300):
    beta=rng.uniform(.9,.999)
    gamma=rng.uniform(.5,3)
    varphi=rng.uniform(.3,3)
    lam=rng.uniform(.02,.9/(1+varphi))
    kp=rng.uniform(.01,.4)
    policy=rng.uniform(1.02,3)
    rho=rng.uniform(0,.95)
    a,m,z=rng.uniform(-.01,.01,3)
    ans=solve(beta,gamma,varphi,lam,kp,policy,rho,a,m,z)
    theta=1-lam*varphi/(1-lam)
    yf=(1+varphi)/(gamma+varphi)*a
    rfR=gamma*(rho-1)*yf
    rfT=rfR-gamma*lam*varphi/((gamma+varphi)*(1-lam))*(rho-1)*z
    krho=kp*(gamma+varphi)/(1-beta*rho)
    x=(m+rfT)/(krho*(policy-rho)+gamma*theta*(1-rho))
    max_error['l11_closed_vs_primitive']=max(max_error['l11_closed_vs_primitive'],abs(ans[0]-yf-x))

    chi=rng.uniform(.1,.9/lam)
    tau=lam*(1-(chi-1)/varphi)
    thetaD=(1-lam*chi)/(1-lam)
    r=-.01
    ans=solve(beta,gamma,varphi,lam,kp,policy,rho,0,0,0,tau=tau,r_given=r)
    demand=-r/(gamma*thetaD*(1-rho))
    max_error['l12_closed_vs_primitive']=max(max_error['l12_closed_vs_primitive'],abs(ans[0]-demand))
    den=1-beta*rho*(1-lam*chi)
    omegaT=(1-beta*(1-lam*chi))/den
    directT=(1-lam)*beta/(gamma*den)
    omegaR=(1-beta)/(1-beta*rho)
    directR=beta/(gamma*(1-beta*rho))
    max_error['l12_PE_vs_euler']=max(max_error['l12_PE_vs_euler'],abs(-r*directT/(1-omegaT)-demand))
    difference=beta*(1-rho)*lam*chi/((1-beta*rho)*den)
    max_error['l12_slope_difference_identity']=max(max_error['l12_slope_difference_identity'],abs(omegaT-omegaR-difference))
    assert omegaT>omegaR and directT<directR

def geometry(name):
    svg=ET.parse(ROOT/'figures/lecture12'/name).getroot()
    paths={el.attrib.get('class'):list(map(float,re.findall(r'-?\d+(?:\.\d+)?',el.attrib['d'])))
           for el in svg.iter() if el.tag.endswith('path') and 'class' in el.attrib}
    def slope(coords):
        x1,y1,x2,y2=coords
        return (y2-y1)/(x2-x1)
    scale=slope(paths['line45'])
    pe=paths['pe'] if 'pe' in paths else paths['peT']
    direct=paths['direct']
    feedback=paths.get('feedback',paths.get('total'))
    return dict(implied_omega=slope(pe)/scale,
                direct_shift_pixels=abs(direct[3]-direct[1]),
                feedback_vertical_pixels=abs(feedback[3]-feedback[1]),
                total_income_change_pixels=abs(feedback[2]-feedback[0]))

rank=geometry('rank_nk_cross.svg')
tank=geometry('tank_nk_cross.svg')
expected=dict(beta=.99,p=0,lam=.3,chi=2,omega_R=.01,omega_T=.604,
              direct_ratio=.7,total_ratio=1.75)
summary={
    'scope':'300 joint technology/monetary/transfer draws for L11; 300 conditional-interest-rate draws for L12; source equations and SVG geometry only, not layout QA.',
    'numpy_version':np.__version__,
    'max_errors':max_error,
    'all_equation_checks_pass':all(v<1e-9 for v in max_error.values()),
    'PE_calibration_expected':expected,
    'rank_SVG_geometry':rank,
    'tank_SVG_geometry':tank,
    'SVG_implied_direct_ratio':tank['direct_shift_pixels']/rank['direct_shift_pixels'],
    'SVG_implied_total_ratio':tank['total_income_change_pixels']/rank['total_income_change_pixels'],
    'finding':'SVG lines have correct intersections but do not reproduce the beta=.99,p=0 calibration claimed by lecture12.qmd:348 and :682. Rank PE implies omega=.2 rather than .01.',
    'sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['lecture11.qmd','lecture12.qmd','solution.qmd','figures/lecture12/rank_nk_cross.svg','figures/lecture12/tank_nk_cross.svg']},
}
(OUT/'checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
