"""
This test module shows a flaky test due to an enforced test timeout that is usually
good enough when the optimization problem is well-behaved, but fails when convergence
is slow.
"""
# ----------------------------------
# implementation - find_discount_rate.py
# ----------------------------------
import numpy as np
from scipy.optimize import newton


def calculate_present_value(discount_rate, cashflows):
    t = np.arange(1, len(cashflows) + 1)
    return np.sum(cashflows / (1 + discount_rate) ** t)


def optimization_problem(discount_rate, present_value, cashflows):
    return calculate_present_value(discount_rate, cashflows) - present_value


def find_discount_rate(present_value, cashflows):
    try:
        return newton(
            optimization_problem, x0=0.1, args=(present_value, cashflows), maxiter=1000
        )
    except RuntimeError:
        # failed to converge
        return np.nan


# ----------------------------------
# test suite - test_find_discount_rate.py
# ----------------------------------
import pytest


@pytest.mark.timeout(2)
def test_find_discount_rate():
    h = 360_000
    cashflows = np.random.randint(50, 300, size=h)
    present_value = np.random.randint(1000, 100_000)
    find_discount_rate(present_value, cashflows)


if __name__ == "__main__":
    passed = 0
    n_iter = 100
    for _ in range(n_iter):
        seed = np.random.randint(0, 10000)
        out = pytest.main(
            [__file__, "--randomly-seed", str(seed), "-vvv"],
            plugins=["timeout", "randomly"],
        )
        if out == pytest.ExitCode.OK:
            passed += 1
    print("passed_percent", passed / n_iter * 100, "%")
