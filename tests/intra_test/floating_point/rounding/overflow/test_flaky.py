"""
This test module showcases examples of flaky tests due to
overflow issues - common when dealing with numeric data.
"""
# ----------------------------------
# implementation - compute_balance.py
# ----------------------------------
import numpy as np

def compute_balance(amount, includes_flag):
    total_balance = np.int32(0)
    for amount, flag in zip(amount, includes_flag):
        if flag:
            total_balance += amount
    return total_balance

# ----------------------------------
# test suite - test_compute_balance.py
# ----------------------------------
def test_eng_balance_is_correctly_computed():
    dept_expense = 1_630_000_000
    num_dept = 10
    num_eng_dept = np.random.randint(1, num_dept)
    num_non_eng_dept = num_dept - num_eng_dept

    total_expenses = np.array(
        [dept_expense] * num_dept, dtype=np.int32
    )
    is_eng_dept = np.array(
        [True] * num_eng_dept +
        [False] * num_non_eng_dept,
        dtype="bool"
    )

    computed_total_eng_spend = compute_balance(
        total_expenses, is_eng_dept
    )
    expected_total_eng_spend = (
        dept_expense * num_eng_dept
    )
    diff = (
        computed_total_eng_spend -
        expected_total_eng_spend
    )
    assert np.isclose(diff, 0)


if __name__ == "__main__":
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
