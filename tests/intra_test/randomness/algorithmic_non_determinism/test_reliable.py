"""
To make sure the test is reliable, we assess the variance of the results of running the
nelder-mead algorithm multiple times. Then assuming the results are normally distributed,
we can choose the tolerance to be 3 standard deviations from the mean. This way, we can
be 99.7% confident that the test will pass (not too permissive, not too strict)
"""
# ----------------------------------
# implementation - minimze_rosenbrock.py
# ----------------------------------
import numpy as np
from scipy.optimize import minimize

def rosenbrock(x):
    a = 1.0
    b = 100.0
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

def minimize_rosenbrock(initial_guess):
    return minimize(
        rosenbrock,
        initial_guess,
        method='Nelder-Mead'
    )

# ----------------------------------
# test suite - test_minimize_rosenbrock.py
# ----------------------------------
def estimate_tolerance(num_runs=50):
    results = []

    for _ in range(num_runs):
        initial_guess = np.random.randint(
            0, 10, size=2
        )
        result = minimize_rosenbrock(initial_guess)
        results.append(result.x)

    results = np.array(results)
    std_dev = np.std(results)
    return 3 * std_dev

def test_correctly_minimizes_rosenbrock():
    # Initial guess
    initial_guess = np.random.randint(0, 10, size=2)

    # Get the result of the minimization
    result = minimize_rosenbrock(initial_guess)

    # tolerance is estimated from results of
    # running minimization multiple times
    tolerance = estimate_tolerance()

    assert np.all(
        np.isclose(
            result.x, [1, 1], atol=tolerance
        )
    )

if __name__ == '__main__':
    import pytest

    passed = 0
    n_iter = 100
    for _ in range(n_iter):
        seed = np.random.randint(0, 10000)
        out = pytest.main(
            [__file__, "--randomly-seed", str(seed), "-vvv"],
            plugins=["randomly"],
        )
        if out == pytest.ExitCode.OK:
            passed += 1
    print("passed_percent", passed / n_iter * 100, "%")
