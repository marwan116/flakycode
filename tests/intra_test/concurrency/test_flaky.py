"""Canonical example of a flaky test due to concurrency issues.

Multiple threads concurrently call the concurrent_transactions function, which includes
both deposits and withdrawals.

Threads may interleave in a way that one thread deposits while another thread withdraws
at the same time.

Due to the non-atomic nature of the deposit and withdrawal operations, the interleaved
execution can lead to race conditions where the balance is not correctly maintained.

The GIL only protects the execution of individual Python bytecode instructions. It does
not provide atomicity or synchronization guarantees for complex operations involving
multiple bytecode instructions. To ensure thread safety in scenarios like this, you
would need to use proper synchronization mechanisms like locks to protect critical
sections of code, ensuring that only one thread can modify shared data at a time.
"""
# ----------------------------------
# implementation - bank_account.py
# ----------------------------------
class BankAccount:
    def __init__(self, balance=100):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


class Merchant:
    def charge_and_refund(
        self,
        account,
        test_fee=0.01,
        num_transactions=400
    ):
        for _ in range(num_transactions):
            account.withdraw(test_fee)
            account.deposit(test_fee)

# ----------------------------------
# test suite - test_bank_account.py
# ----------------------------------
import threading

def test_charge_and_refund_keeps_balance_the_same():
    # initialize bank account with $100 balance
    account = BankAccount(balance=100)
    original_balance = account.balance

    threads = []

    # "smartly" parallelize call to charge_and_refund
    merchants = [Merchant() for _ in range(10)]
    for merchant in merchants:
        thread = threading.Thread(
            target=merchant.charge_and_refund,
            args=(account,),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    assert account.balance == original_balance


if __name__ == "__main__":
    """
    A common trick to uncover concurrency issues is to lower the switch interval of the
    interpreter. This will cause the interpreter to switch between threads more often,
    increasing the likelihood of a concurrency issue occurring.
    """
    import sys
    import pytest

    original_switch_interval = sys.getswitchinterval()
    try:
        sys.setswitchinterval(0.0001)
        passed = 0
        n_iter = 100
        for _ in range(n_iter):
            out = pytest.main([__file__])
            if out == pytest.ExitCode.OK:
                passed += 1
        print("passed_percent", passed / n_iter * 100, "%")
    finally:
        sys.setswitchinterval(original_switch_interval)
