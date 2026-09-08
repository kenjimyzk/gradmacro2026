"""Independent finite-horizon to stationary scalar Markov-discretion validation.
No stochastic shocks after the initial state. Structural parameters satisfy
kappa_j=psi_j/eta_j and omega_j=eta_j/(gamma+varphi).
Only the Python standard library is required.
"""
import json


def backward_step(next_policy, beta, kp, kw, wp, ww, g):
    # The next policymaker takes its inherited real marginal cost s'=m.
    # These are slopes of the given next-period policy functions and value.
    hp, xp, pp, wp_next, value_next = next_policy
    K = kw*g
    A = kp+beta*pp
    C = 1+A+kw-beta*wp_next
    B = C/K
    # Current constraints imply p=A*m, w=(1+A)*m-s, x=B*m-s/K.
    # Continuation value is 0.5*value_next*m^2.
    denominator = B*B+wp*A*A+ww*(1+A)**2+beta*value_next
    h = (B/K+ww*(1+A))/denominator
    x = B*h-1/K
    p = A*h
    w = (1+A)*h-1
    value = x*x+wp*p*p+ww*w*w+beta*value_next*h*h
    return (h,x,p,w,value)


def solve(eta_w=60.0, tolerance=2e-14):
    beta=.99; psi=6.; eta_p=60.; g=2.
    kp=psi/eta_p; kw=psi/eta_w; wp=eta_p/g; ww=eta_w/g
    policy=(0.,0.,0.,0.,0.)
    for steps in range(1,100001):
        updated=backward_step(policy,beta,kp,kw,wp,ww,g)
        gap=max(abs(a-b) for a,b in zip(updated,policy))
        policy=updated
        if gap<tolerance:
            break
    else:
        raise RuntimeError('No stationary convergence')
    h,x,p,w,P=policy
    K=kw*g; A=kp+beta*p; C=1+A+kw-beta*w; B=C/K
    s=.01; m=h*s; xcur=x*s; pcur=p*s; wcur=w*s
    lam2=-xcur/K
    lam3=ww*wcur-lam2
    lam1=wp*pcur+lam3
    Gamma=beta*P*m
    old_foc=kp*lam1-kw*lam2+lam3+Gamma
    extra=beta*(p*lam1+w*lam2)
    corrected_foc=old_foc+extra
    corrected_target=C*xcur+K*(A*wp*pcur+(1+A)*ww*wcur+Gamma)
    old_target=(1+kp+kw)*xcur+K*(kp*wp*pcur+(1+kp)*ww*wcur+Gamma)
    constraints=[pcur-kp*m-beta*p*m,wcur-K*xcur+kw*m-beta*w*m,wcur-m+s-pcur]
    def objective(mdev):
        pp=A*mdev; wwcur=(1+A)*mdev-s; xx=B*mdev-s/K
        return .5*(xx*xx+wp*pp*pp+ww*wwcur*wwcur+beta*P*mdev*mdev)
    eps=1e-6
    fd=(objective(m+eps)-objective(m-eps))/(2*eps)
    convexity=B*B+wp*A*A+ww*(1+A)**2+beta*P
    curvature_fd=(objective(m+eps)-2*objective(m)+objective(m-eps))/eps**2
    value_bellman=P-(x*x+wp*p*p+ww*w*w+beta*P*h*h)
    assert abs(h)<1
    assert max(abs(r) for r in constraints)<1e-12
    assert abs(corrected_foc)<1e-11
    assert abs(corrected_target)<1e-8
    assert abs(fd)<1e-10
    assert abs(curvature_fd/convexity-1)<1e-7
    assert abs(value_bellman)<1e-11
    assert objective(m+eps)>objective(m)
    assert objective(m-eps)>objective(m)
    return {'eta_w':eta_w,'kappa_w':kw,'omega_w':ww,'steps':steps,
            'slopes':dict(zip(('mc','x','price','wage','value_curvature'),policy)),
            'fixed_point_residual':gap,'initial_state':s,
            'Gamma':Gamma,'expectation_price_derivative':p,'expectation_wage_derivative':w,
            'old_foc':old_foc,'corrected_foc':corrected_foc,'missing_derivative_term':extra,
            'old_target':old_target,'corrected_target':corrected_target,
            'one_shot_deviation_fd':fd,'one_shot_deviation_curvature':convexity,
            'constraint_residual':max(abs(r) for r in constraints),
            'bellman_residual':value_bellman,
            'price_only_target':xcur+kp*g*wp*pcur,
            'normalized_target_x_coefficient':C/kw,
            'current_optimal_loss':objective(m)}

base=solve()
assert abs(base['old_foc'])>1e-4
out={'base_stationary_equilibrium':base,
     'flexible_wage_limit':[solve(x) for x in [6, .6,.06,.006,.0006,.00006]]}
print(json.dumps(out,indent=2))
