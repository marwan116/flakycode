"""
This test is flaky because the chosen algorithm "the nelder-mead" optimization is not
deterministic. 

More specifically, in this example we are using the Nelder-Mead to optimize the Rosenbrock
function, also referred to as the Valley or Banana function, which is a popular
test problem for gradient-based optimization algorithms. The function is unimodal, and
the global minimum lies in a narrow, parabolic valley.

The narrow valley makes it somewhat difficult for the algorithms to converge to the
same minimum given different starting points.
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

def test_correctly_minimizes_rosenbrock():
    # Initial guess
    initial_guess = np.random.randint(0, 10, size=2)

    # Get the result of the minimization
    result = minimize_rosenbrock(initial_guess)

    # naively choose atol
    naively_chosen_atol = 1e-5

    assert np.all(
        np.isclose(
            result.x, [1, 1], atol=naively_chosen_atol)
        )

if __name__ == "__main__":
    """Running the test multiple times reveals that the test is flaky."""
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
