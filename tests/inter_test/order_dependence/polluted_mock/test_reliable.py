# ----------------------------------
# implementation - my_service.py
# ----------------------------------
import datetime

class MyService:
    def get_current_time(self):
        return datetime.date.today()


class NewDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(1990, 1, 1)

# ----------------------------------
# test suite - test_my_service.py
# ----------------------------------
from unittest import mock

def test_we_are_back_in_the_90s_unitest_mock():
    with mock.patch("datetime.date", NewDate):
        service = MyService()
        result = service.get_current_time()
        assert result.year == 1990

def test_we_are_back_in_the_90s_pytest_monkeypatch(monkeypatch):
    monkeypatch.setattr("datetime.date", NewDate)
    service = MyService()
    result = service.get_current_time()
    assert result.year == 1990


def test_we_are_in_the_21st_century():
    assert datetime.date.today().year >= 2000

if __name__ == "__main__":
    import pytest
    import numpy as np

    passed = 0
    n_iter = 100
    for _ in range(n_iter):
        seed = np.random.randint(0, 10000)
        out = pytest.main(
            [__file__, "--randomly-seed", str(seed)],
            plugins=["randomly"],
        )
        if out == pytest.ExitCode.OK:
            passed += 1
    print("passed_percent", passed / n_iter * 100, "%")
