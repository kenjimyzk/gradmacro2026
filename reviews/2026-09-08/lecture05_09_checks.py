#!/usr/bin/env python3
"""Independent stdlib-only checks for the 2026-09-08 gradmacro2026 review.

Run: python3 lecture05_09_checks.py [output.json]
Sources inspected: lecture07.qmd:598; lecture08.qmd:848-899;
lecture09.qmd:922-952; solution.qmd:917. No course files are modified.
"""

import json
import math
import sys
from pathlib import Path


TOL = 1e-12


def require_residuals(residuals):
    largest = max(abs(value) for value in residuals.values())
    assert largest < TOL, residuals
    return {"values": residuals, "max_abs": largest, "tolerance": TOL}


def lecture07_counterexample():
    # Select small monetary/technology shocks with distinct persistence.
    beta, gamma, varphi, psi, eta, phi = .99, 1., 1., 6., 80., 1.5
    rho_m, rho_a = .9, 0.
    kappa_x = psi / eta * (gamma + varphi)
    zeta_a = (1 + varphi) / (gamma + varphi)
    k_m = kappa_x / (1 - beta * rho_m)
    k_a = kappa_x / (1 - beta * rho_a)
    omega_m = 1 / (k_m * (phi - rho_m) + gamma * (1 - rho_m))
    omega_a = gamma * (1 - rho_a) / (
        k_a * (phi - rho_a) + gamma * (1 - rho_a))
    m, a = .01 / omega_m, .005 / (zeta_a * omega_a)
    x_m, x_a = omega_m * m, -zeta_a * omega_a * a
    x, expected_x = x_m + x_a, rho_m * x_m + rho_a * x_a
    pi = k_m * x_m + k_a * x_a
    expected_pi = rho_m * k_m * x_m + rho_a * k_a * x_a
    r_f = gamma * zeta_a * (rho_a - 1) * a
    r = phi * pi - expected_pi - m
    residuals = require_residuals({
        "IS": x - expected_x + (r - r_f) / gamma,
        "NKPC": pi - beta * expected_pi - kappa_x * x,
        "Taylor_Fisher": r - (phi * pi - expected_pi - m),
    })
    assert x > 0 and r - r_f > 0
    return {
        "status": "verified_counterexample",
        "claim_tested": "r_t > r_t^f implies x_t < 0",
        "parameters": dict(beta=beta, gamma=gamma, varphi=varphi,
                           psi=psi, eta=eta, phi=phi, rho_m=rho_m, rho_a=rho_a),
        "shocks": dict(m=m, a=a),
        "solution": dict(x=x, expected_x_next=expected_x, pi=pi,
                         expected_pi_next=expected_pi, r=r, r_f=r_f,
                         rate_gap=r-r_f),
        "residuals": residuals,
    }


def lecture08_impact_checks():
    # Same primitives as the actual lecture08 numerical example.
    beta, gamma, varphi, alpha, gy = .99, 1., 1., .33, .2
    psi, eta, phi, mc_ss = 6., 80., 1.5, 1.
    tg, tv = gamma / (1 - gy), (varphi + alpha) / (1 - alpha)
    za, zg = (tv + 1) / (tg + tv), tg / (tg + tv)
    kx = mc_ss * (tg + tv) * psi / eta
    results = {}
    for shock, rho in (("monetary", .5), ("technology", .8), ("government", .8)):
        a, g, m = float(shock == "technology"), float(shock == "government"), float(shock == "monetary")
        k = kx / (1 - beta * rho)
        denominator = k * (phi - rho) + tg * (1 - rho)
        omega = tg * (1 - rho) / denominator
        x = m / denominator - za * omega * a + (1 - zg) * omega * g
        pi = k * x
        r = (phi - rho) * pi - m
        yf = za * a + zg * g
        rf = -tg * (1 - rho) * za * a + tg * (1 - rho) * (1 - zg) * g
        y = yf + x
        c, n = (y - g) / (1 - gy), (y - a) / (1 - alpha)
        mc, w = (tg + tv) * x, gamma * c + varphi * n
        residuals = require_residuals({
            "IS": x - rho * x + (r - rf) / tg,
            "NKPC": pi - beta * rho * pi - kx * x,
            "Taylor_Fisher": r - (phi * pi - rho * pi - m),
            "household_Euler": r - gamma * (rho - 1) * c,
            "resource": y - (1 - gy) * c - g,
            "production": y - a - (1 - alpha) * n,
            "labor_demand": w - mc - y + n,
            "labor_supply": w - gamma * c - varphi * n,
        })
        results[shock] = {"rho": rho,
                          "unit_state_impact": dict(x=x, pi=pi, r=r, y=y, c=c, n=n, mc=mc, w=w, yf=yf, rf=rf),
                          "residuals": residuals}
    return {"status": "verified", "parameters": dict(beta=beta, gamma=gamma, varphi=varphi,
            alpha=alpha, G_Y=gy, psi=psi, eta=eta, phi=phi, MC=mc_ss), "shocks": results}


def lecture09_welfare_comparison():
    beta, kappa, weight, rho = .99, .08, 20., .7
    B = 1 + beta + kappa**2 * weight
    # Stable root of beta*lambda^2 - B*lambda + 1 = 0.
    stable = 2 / (B + math.sqrt(B*B - 4*beta))
    assert 0 < stable < 1
    b = -kappa * weight * stable / (1 - beta * rho * stable)
    denominator = 1 - beta * rho + kappa**2 * weight
    ad, bd = -kappa * weight / denominator, 1 / denominator
    nperiods = 2000
    xc, pc = [], []
    last_x = 0.
    for t in range(nperiods):
        x = stable * last_x + b * rho**t
        pi = -(x - last_x) / (kappa * weight)
        xc.append(x)
        pc.append(pi)
        last_x = x
    residuals = require_residuals({
        "characteristic_polynomial": beta * stable**2 - B * stable + 1,
        "commitment_NKPC_max": max(abs(pc[t] - beta * pc[t+1] - kappa * xc[t] - rho**t)
                                      for t in range(nperiods-1)),
        "commitment_target_max": max(abs(kappa * weight * pc[t] + xc[t] - (xc[t-1] if t else 0))
                                        for t in range(nperiods)),
        "discretion_NKPC_coefficient": bd - beta * rho * bd - kappa * ad - 1,
        "discretion_target_coefficient": ad + kappa * weight * bd,
    })
    vx_c = math.fsum(beta**t * x*x for t, x in enumerate(xc))
    vp_c = math.fsum(beta**t * p*p for t, p in enumerate(pc))
    vx_d, vp_d = ad*ad / (1-beta*rho*rho), bd*bd / (1-beta*rho*rho)
    lc, ld = .5*(vx_c+weight*vp_c), .5*(vx_d+weight*vp_d)
    assert vx_c > vx_d and vp_c < vp_d and lc < ld
    assert abs(xc[-1]) < 1e-100 and abs(pc[-1]) < 1e-100
    return {
        "status": "verified_counterexample",
        "claim_tested": "Discretion has larger output fluctuations as well as inflation fluctuations than commitment",
        "parameters": dict(beta=beta, kappa_x=kappa, omega_p=weight, rho_u=rho),
        "initial_condition": "u_0=1; x_-1=0; no subsequent innovations",
        "method": "Analytic infinite-horizon stable policy; evaluate 2000 terms (not the lecture's finite-terminal matrix approximation)",
        "policy": dict(stable_root=stable, coefficient_u=b),
        "discounted_sum_squares_and_loss": {
            "discretion": dict(x_squared=vx_d, pi_squared=vp_d, total_loss=ld),
            "commitment": dict(x_squared=vx_c, pi_squared=vp_c, total_loss=lc),
        },
        "terminal_magnitudes": dict(x=abs(xc[-1]), pi=abs(pc[-1])),
        "residuals": residuals,
    }


def main():
    result = {"all_checks_passed": True,
              "lecture07_rate_gap_counterexample": lecture07_counterexample(),
              "lecture08_impact_equations": lecture08_impact_checks(),
              "lecture09_welfare_counterexample": lecture09_welfare_comparison()}
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"All checks passed; evidence written to {output}")


if __name__ == "__main__":
    main()
