#!/usr/bin/env python3
"""Fresh independent checks for L9/L10. Does not edit lecture sources.
Requires numpy, scipy (present in the reviewed runtime).
"""
from pathlib import Path
import hashlib,json,math,itertools
import numpy as np
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parents[4]


def matrix_markov(eta_w=60.,rho=.7,beta=.99):
    q=2.;kp=6./60.;kw=6./eta_w;wp=60./q;ww=eta_w/q;K=kw*q
    weights=np.diag([wp,ww,1.])
    # S=[inherited mc, current a, previous a]; S'=[z,rho*a+eps,a].
    T=np.array([[0.,0.,0.],[0.,rho,0.],[0.,1.,0.]])
    v=np.array([1.,0.,0.]); delta=np.array([-1.,1.,-1.])
    G=np.zeros((3,3));P=np.zeros((3,3))
    for n in range(1,10001):
        nextG,nextP=G.copy(),P.copy()
        ep,ew,ex=nextG@v
        intercept=nextG@T
        slope=np.array([kp+beta*ep,1+kp+beta*ep,(1+kp+beta*ep+kw-beta*ew)/K])
        B=np.vstack([beta*intercept[0],delta+beta*intercept[0],
                     (delta+beta*intercept[0]-beta*intercept[1])/K])
        H=slope@weights@slope+beta*nextP[0,0]
        h=-(slope@weights@B+beta*v@nextP@T)/H
        G=np.outer(slope,h)+B
        transition=np.outer(v,h)+T
        P=G.T@weights@G+beta*transition.T@nextP@transition
        gap=max(np.max(np.abs(G-nextG)),np.max(np.abs(P-nextP)))
        if gap<1e-12:break
    else:raise RuntimeError('No convergence')
    residuals=[];targetres=[];focres=[];fdres=[];envelope=[];bellman=[];implement=[]
    rng=np.random.default_rng(90910)
    # Nonzero technology and inherited state, with future innovations.
    sigma=.002
    constant=.5*beta*sigma*sigma*P[1,1]/(1-beta)
    for S in rng.normal(0,.03,size=(20,3)):
        z=h@S;p,w,x=G@S
        Sp=v*z+T@S
        Fp,Fw,Fx=G@Sp
        gamma_cont=beta*(P@Sp)[0]
        l2=-x/K;l3=ww*w+x/K;l1=wp*p+l3
        hp=kp+beta*G[0,0];hw=kw-beta*G[1,0]
        residuals.extend([p-kp*z-beta*Fp,w-K*x+kw*z-beta*Fw,w-z+S[0]-S[1]+S[2]-p])
        target=(1+hp+hw)*x+K*(hp*wp*p+(1+hp)*ww*w+gamma_cont)
        targetres.append(target)
        focres.append(hp*l1-hw*l2+l3+gamma_cont)
        envelope.append((P@S)[0]+l3)
        def objective(zdev):
            Sprime=v*zdev+T@S
            fp,fw,fx=G@Sprime
            pd=kp*zdev+beta*fp;wd=zdev-S[0]+S[1]-S[2]+pd
            xd=(wd+kw*zdev-beta*fw)/K
            return .5*(xd*xd+wp*pd*pd+ww*wd*wd)+beta*(.5*Sprime@P@Sprime+.5*sigma*sigma*P[1,1]+constant)
        eps=1e-6
        fdres.append((objective(z+eps)-objective(z-eps))/(2*eps))
        bellman.append(.5*S@P@S+constant-objective(z))
        # q=gamma+varphi=2 with gamma=varphi=1 implies zeta_a=1.
        rf=(rho-1)*S[1];r=rf+Fx-x;rn=r+Fp
        implement.extend([x-Fx+r-rf,r-rn+Fp])
    out={'eta_w':eta_w,'rho_a':rho,'iterations':n,'policy_order':['price','wage','output'],
         'state_order':['mc_lag','a_current','a_lag'],'policy_matrix':G.tolist(),'state_choice':h.tolist(),
         'value_hessian':P.tolist(),'value_noise_constant':constant,'fixed_point_gap':float(gap),
         'spectral_radius':float(max(abs(np.linalg.eigvals(transition)))),
         'constraint_residual':max(map(abs,residuals)), 'target_residual':max(map(abs,targetres)),
         'complete_foc_residual':max(map(abs,focres)), 'envelope_residual':max(map(abs,envelope)),
         'bellman_residual':max(map(abs,bellman)), 'one_shot_fd_residual':max(map(abs,fdres)),
         'implementation_residual':max(map(abs,implement)),
         'price_only_target_max':float(np.max(np.abs(G[2]+kp*q*wp*G[0]))),
         'g_w_s':G[1,0]}
    for name in ['constraint_residual','target_residual','complete_foc_residual','envelope_residual','bellman_residual','implementation_residual']:
        assert out[name]<1e-8,(name,out[name])
    assert out['one_shot_fd_residual']<1e-8
    return out


def nonlinear_expectations():
    beta=.99;kp=.1;kw=.15;q=2.;K=kw*q;wp=30.;ww=20.
    # A smooth non-affine policy conjecture. This tests local identities, not
    # equilibrium existence: expectations and continuation value are fixed.
    Fp=lambda z:.03+.2*np.sin(z)+.04*z*z
    Fw=lambda z:-.02-.15*np.sin(2*z)+.01*z*z
    dp=lambda z:.2*np.cos(z)+.08*z
    dw=lambda z:-.3*np.cos(2*z)+.02*z
    V=lambda z:1.5*z*z+.4*z**4
    dV=lambda z:3*z+1.6*z**3
    max_derivative=0.;max_envelope=0.;points=0
    for s,d in itertools.product([-.03,0.,.04],[-.02,.01]):
        def allocations(z):
            p=kp*z+beta*Fp(z);w=z-s+d+p;x=(w+kw*z-beta*Fw(z))/K
            return p,w,x
        def objective(z):
            p,w,x=allocations(z)
            return .5*(x*x+wp*p*p+ww*w*w)+beta*V(z)
        for z in np.linspace(-.1,.1,11):
            p,w,x=allocations(z);hp=kp+beta*dp(z);hw=kw-beta*dw(z)
            target=(1+hp+hw)*x+K*(hp*wp*p+(1+hp)*ww*w+beta*dV(z))
            eps=1e-6
            fd=(objective(z+eps)-objective(z-eps))/(2*eps)
            max_derivative=max(max_derivative,abs(target/K-fd))
            points+=1
        optimum=minimize_scalar(objective,bounds=(-.3,.3),method='bounded',options={'xatol':1e-14})
        z=optimum.x;p,w,x=allocations(z);lambda3=ww*w+x/K
        # At optimum, differentiate the fixed-conjecture minimized value in s.
        def optimized_value(sdev):
            def obj(zz):
                pp=kp*zz+beta*Fp(zz);wwd=zz-sdev+d+pp
                xx=(wwd+kw*zz-beta*Fw(zz))/K
                return .5*(xx*xx+wp*pp*pp+ww*wwd*wwd)+beta*V(zz)
            return minimize_scalar(obj,bounds=(-.3,.3),method='bounded',options={'xatol':1e-14}).fun
        eps=1e-5
        fd=(optimized_value(s+eps)-optimized_value(s-eps))/(2*eps)
        max_envelope=max(max_envelope,abs(fd+lambda3))
    assert max_derivative<1e-7
    assert max_envelope<1e-7
    return {'identity_points':points,'optimized_envelope_cases':6,
            'max_target_vs_direct_derivative_error':max_derivative,
            'max_envelope_error':max_envelope,
            'scope':'fixed non-affine future-policy conjecture; not an equilibrium existence test'}


def two_period_kkt():
    max_terminal=0.;max_initial=0.;max_constraint=0.;cases=0
    for beta,kp,kw,q,wp,ww in itertools.product([.95,.99],[.03,.1],[.02,.15],[2.],[30.],[20.]):
        K=kw*q
        C=np.array([[-1.,0.,0.,kp],[0.,-1.,K,-kw],[1.,-1.,0.,1.]])
        def solve(H,C,rhs):
            mat=np.block([[H,C.T],[C,np.zeros((3,3))]])
            return np.linalg.solve(mat,np.r_[np.zeros(4),rhs])[:4]
        endpoint=solve(np.diag([wp,ww,1.,0.]),C,np.array([0.,0.,1.]))
        ap,aw,ax,h_kkt=endpoint
        H=(1+kp+kw)**2/K**2+wp*kp**2+ww*(1+kp)**2
        h_source=((1+kp+kw)/K**2+ww*(1+kp))/H
        max_terminal=max(max_terminal,abs(h_source-h_kkt))
        P=ax*ax+wp*ap*ap+ww*aw*aw
        hp=kp+beta*ap;hw=kw-beta*aw
        C0=np.array([[-1.,0.,0.,hp],[0.,-1.,K,-hw],[1.,-1.,0.,1.]])
        for s0,d0 in itertools.product([-.02,.03],[-.01,.02]):
            p0,w0,x0,z0=solve(np.diag([wp,ww,1.,beta*P]),C0,np.array([0.,0.,s0-d0]))
            target=(1+hp+hw)*x0+K*(hp*wp*p0+(1+hp)*ww*w0+beta*P*z0)
            max_initial=max(max_initial,abs(target))
            max_constraint=max(max_constraint,float(np.max(abs(C0@np.array([p0,w0,x0,z0])-np.array([0.,0.,s0-d0])))))
            cases+=1
    assert max_terminal<1e-12 and max_initial<1e-12 and max_constraint<1e-12
    return {'initial_state_technology_cases':cases,'max_terminal_policy_difference_from_full_kkt':max_terminal,
            'max_initial_target_residual_at_full_kkt_solution':max_initial,
            'max_private_constraint_residual':max_constraint}


def lecture09_finite_irf():
    beta=.99;k=.08;w=20.;rho=.7;T=40
    B=1+beta+k*k*w
    A=np.diag(np.full(T+1,B))+np.diag(np.full(T,-beta),1)+np.diag(np.full(T,-1.),-1)
    u=rho**np.arange(T+1)
    xf=np.linalg.solve(A,-k*w*u)
    pf=-(xf-np.r_[0.,xf[:-1]])/(k*w)
    stable=2/(B+math.sqrt(B*B-4*beta))
    loading=-k*w*stable/(1-beta*stable*rho)
    xs=[];ps=[];last=0.
    for t in range(2000):
        x=stable*last+loading*rho**t;p=-(x-last)/(k*w)
        xs.append(x);ps.append(p);last=x
    xs=np.array(xs);ps=np.array(ps)
    dden=1-beta*rho+k*k*w
    xd=-k*w*rho**np.arange(2000)/dden;pd=rho**np.arange(2000)/dden
    disc=beta**np.arange(2000)
    loss_c=.5*np.sum(disc*(xs*xs+w*ps*ps))
    loss_d=.5*np.sum(disc*(xd*xd+w*pd*pd))
    errx=float(np.max(abs(xf-xs[:T+1])));errp=float(np.max(abs(pf-ps[:T+1])))
    assert max(errx,errp)<1e-4
    assert loss_c<loss_d
    return {'T':T,'x_lag':0.,'stable_root':stable,
            'max_irf_output_error':errx,'max_irf_inflation_error':errp,
            'max_first20_output_error':float(np.max(abs(xf[:20]-xs[:20]))),
            'finite_matrix_residual':float(np.max(abs(A@xf+k*w*u))),
            'infinite_discretion_loss':float(loss_d),'infinite_commitment_loss':float(loss_c),
            'discounted_output_square_discretion':float(np.sum(disc*xd*xd)),
            'discounted_output_square_commitment':float(np.sum(disc*xs*xs)),
            'interpretation':'The plotted timeless solution with inherited multiplier/gap zero coincides with date-0 commitment for this IRF. Arbitrary inherited promises need not share its welfare ranking.'}


def main():
    baseline=[matrix_markov(ew,rho) for ew,rho in itertools.product([6.,60.,600.],[0.,.7,.95])]
    flex=[matrix_markov(ew,.7) for ew in [6.,.6,.06,.006,.0006]]
    out={'status':'verified','ar1_technology_markov':baseline,
         'flexible_wage_sequence':flex,'nonlinear_future_policy':nonlinear_expectations(),
         'two_period_kkt':two_period_kkt(),'lecture09_irf':lecture09_finite_irf(),
         'limits':['Finite numerical examples do not prove existence or uniqueness of all Markov equilibria.',
                   'Flexible limit checks apply to this convergent sequence; source states explicit regularity assumptions.'],
         'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['lecture09.qmd','lecture10.qmd','solution.qmd']}}
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
