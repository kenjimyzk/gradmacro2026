"""Independent checks of Lecture 10 extension questions 5--7.

Read-only with respect to lecture sources and rendered deliverables.
"""
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(1005092026)

# Q5: under zero inflation for all periods and histories, both expected
# inflation rates vanish. Positive slopes force both markups and x to zero,
# so w_t=a_t. Test compatibility with w_t=w_{t-1}, including time zero.
q5_cases = [
    ('zero_baseline', 0., 0., [0., 0., 0.], True),
    ('unexpected_technology', 0., 0., [.01, .008, .0064], False),
    ('initial_wage_gap_only', .005, 0., [0., 0., 0.], False),
    ('later_technology_change', .01, .01, [.01, .01, .02], False),
    # The initial technology can differ from a_-1 when the inherited wage
    # is already equal to a_0: a_0=w_-1, not a_0=a_-1, is the right condition.
    ('nonzero_compatible_initial_condition', .005, -.002, [.005, .005, .005], True),
]
q5 = []
for name, wm1, am1, a, expected in q5_cases:
    a = np.asarray(a)
    required_w = a.copy()
    dw = np.diff(np.r_[wm1, required_w])
    da = np.diff(np.r_[am1, a])
    gaps = np.r_[wm1-am1, required_w-a]
    identity_residual = np.diff(gaps)-(dw-da)
    feasible = bool(np.max(abs(dw))<1e-12)
    assert feasible == expected
    assert np.max(abs(identity_residual))<1e-12
    q5.append({'case': name, 'w_minus1': wm1, 'a_minus1': am1,
               'a_path': a.tolist(), 'all_zero_inflation_compatible': feasible,
               'required_real_wage_changes': dw.tolist()})

# Q6: solve the primitive two-equation linear system and compare with the
# printed closed forms, rather than using either form to generate the other.
def primitive(kp, kw, curvature, x, dw):
    return np.linalg.solve([[1/kp, 1/kw], [-1., 1.]], [curvature*x, dw])

q6_max = 0.
for _ in range(160):
    kp, kw = np.exp(rng.uniform(-5, 1, 2))
    s, x, dw = rng.uniform(.4, 6), rng.normal(scale=.01), rng.normal(scale=.01)
    direct = primitive(kp, kw, s, x, dw)
    bar = kp*kw/(kp+kw)
    stated = np.array([bar*s*x-kp*dw/(kp+kw), bar*s*x+kw*dw/(kp+kw)])
    q6_max = max(q6_max, float(np.max(abs(direct-stated))))
assert q6_max<1e-10
q6_numeric = primitive(.1, .05, 2., .01, .002)
assert np.allclose(q6_numeric, [-1/1500, 1/750], atol=1e-14)

# Q7: directly minimize the original one-variable objective numerically.
# This search uses no derivative or closed-form optimum.
def golden_minimum(f, lo, hi):
    ratio = (np.sqrt(5)-1)/2
    c, d = hi-ratio*(hi-lo), lo+ratio*(hi-lo)
    fc, fd = f(c), f(d)
    for _ in range(150):
        if fc<fd:
            hi, d, fd = d, c, fc
            c = hi-ratio*(hi-lo)
            fc = f(c)
        else:
            lo, c, fc = c, d, fd
            d = lo+ratio*(hi-lo)
            fd = f(d)
    z = (lo+hi)/2
    return z, f(z)

q7_point_error, q7_value_error, completion_error = 0., 0., 0.
for _ in range(160):
    wp, ww = np.exp(rng.uniform(-1, 6, 2))
    delta = rng.normal(scale=.015)
    f = lambda p: .5*(wp*p*p+ww*(p+delta)**2)
    numerical_p, numerical_j = golden_minimum(f, min(0,-delta)-.1, max(0,-delta)+.1)
    stated_p = -ww*delta/(wp+ww)
    stated_min = .5*wp*ww/(wp+ww)*delta**2
    q7_point_error = max(q7_point_error, abs(numerical_p-stated_p))
    q7_value_error = max(q7_value_error, abs(numerical_j-stated_min))
    for p in rng.normal(scale=.03, size=5):
        square_form = .5*(wp+ww)*(p+ww*delta/(wp+ww))**2+stated_min
        completion_error = max(completion_error, abs(f(p)-square_form))
        assert f(p)+1e-12>=stated_min
assert q7_point_error<1e-8
assert q7_value_error<1e-10
assert completion_error<1e-10
numeric_p, numeric_j = golden_minimum(lambda p:.5*(30*p*p+60*(p+.01)**2), -.02, .02)
assert abs(numeric_p+1/150)<1e-8 and abs(numeric_j-.001)<1e-12

# The equality condition must distinguish delta=0 from a nonzero adjustment.
matching=[]
for pp,pw,ep,ew,delta in [(6,6,60,120,.01), (6,8,60,120,.01), (6,8,60,120,0.), (4,4,80,40,-.015)]:
    kp,kw,wp,ww=pp/ep,pw/ew,ep/2,ew/2
    q6_answer=primitive(kp,kw,2,0,delta)
    q7_answer=np.array([-ww*delta/(wp+ww),wp*delta/(wp+ww)])
    same=bool(np.allclose(q6_answer,q7_answer,atol=1e-13))
    assert same == (delta==0 or pp==pw)
    matching.append({'psi_p':pp,'psi_w':pw,'delta':delta,'answers_match':same,
                     'max_difference':float(np.max(abs(q6_answer-q7_answer)))})

result={
    'source_sha256': {s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest()
                      for s in ['lecture10.qmd','solution.qmd']},
    'source_and_answer_review': 'Q5--7 and every numbered answer part agree; no correction required.',
    'q5_initial_and_dynamic_conditions':q5,
    'q6':{'independent_2x2_cases':160,'max_abs_difference':q6_max,
          'printed_example_inflation':q6_numeric.tolist(),
          'printed_example_times_100':(100*q6_numeric).tolist()},
    'q7':{'direct_numerical_minimizations':160,'max_minimizer_difference':q7_point_error,
          'max_minimum_value_difference':q7_value_error,
          'max_square_completion_difference':completion_error,
          'printed_example':{'price_inflation':numeric_p,'wage_inflation':numeric_p+.01,'loss':numeric_j},
          'equality_cases':matching},
    'interpretation_checks':[
        'Q5 imposes zero inflation at all future dates and histories, not one date.',
        'Q5 requires a_0=w_-1 and an unchanged technology path thereafter.',
        'Q6 takes output gap, real wage change and future inflation expectations as given.',
        'Q6 flexible limits apply to the conditional slope at Delta w=0.',
        'Q7 is an identity-only lower bound for current nominal adjustment losses, not full dynamic welfare.',
        'Q7 nonzero-delta matching condition is kappa_p omega_p=kappa_w omega_w iff psi_p=psi_w.'
    ]
}
text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
(OUT/'independent-checks.json').write_text(text)
print(text)
