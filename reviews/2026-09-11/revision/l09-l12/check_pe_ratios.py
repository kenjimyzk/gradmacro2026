"""Check newly stated PE ratios against original coefficient definitions exactly."""
from fractions import Fraction as F
from pathlib import Path
import json
import random

rng = random.Random(20260911)
count = positive_count = p0_count = 0
for _ in range(1000):
    beta = F(rng.randrange(1, 100), 100)
    p = F(rng.randrange(0, 100), 100)
    lam = F(rng.randrange(1, 100), 100)
    chi = F(rng.randrange(-100, 401), 100)
    gamma = F(rng.randrange(1, 501), 100)
    b = 1 - lam * chi
    if b == 0 or 1 - beta * p * b == 0:
        continue
    wr = (1 - beta) / (1 - beta * p)
    wt = (1 - beta * b) / (1 - beta * p * b)
    dr = beta / (gamma * (1 - beta * p))
    dt = (1 - lam) * beta / (gamma * (1 - beta * p * b))
    stated_direct = (1 - lam) * (1 - beta * p) / (1 - beta * p * b)
    stated_multiplier = (1 - beta * p * b) / ((1 - beta * p) * b)
    assert dt / dr == stated_direct
    assert (1 - wr) / (1 - wt) == stated_multiplier
    assert stated_direct * stated_multiplier == (1 - lam) / b
    if 0 < lam * chi < 1:
        assert 0 < stated_direct < 1
        positive_count += 1
    if p == 0:
        assert stated_direct == 1 - lam
        assert stated_multiplier == 1 / b
        p0_count += 1
    count += 1

beta, p, lam, chi = F(99, 100), F(1, 2), F(3, 10), F(2)
direct = (1 - lam) * (1 - beta * p) / (1 - beta * p * (1 - lam * chi))
multiplier = (1 - beta * p * (1 - lam * chi)) / ((1 - beta * p) * (1 - lam * chi))
assert round(float(direct), 3) == 0.441
assert round(float(multiplier), 3) == 3.970
assert direct * multiplier == F(7, 4)
result = {
    "status": "passed",
    "arithmetic": "exact fractions",
    "coefficient_definition_comparisons": count,
    "positive_feedback_direct_reduction_checks": positive_count,
    "p_zero_limit_checks": p0_count,
    "illustration": {
        "direct_ratio": float(direct),
        "multiplier_ratio": float(multiplier),
        "total_ratio": float(direct * multiplier),
    },
    "scope": "new PE ratio explanation only; primitive model equations unchanged",
}
Path(__file__).with_name("pe-ratios.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
