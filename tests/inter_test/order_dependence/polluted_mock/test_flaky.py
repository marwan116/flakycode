# ----------------------------------
# implementation - my_service.py
# ----------------------------------
import datetime

class MyService:
    def get_current_time(self):
        return datetime.date.today()

# ----------------------------------
# test suite - test_my_service.py
# ----------------------------------
import datetime

class NewDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(1990, 1, 1)


def test_we_are_back_in_the_90s():
    # let's monkey-patch datetime.date
    # what could go wrong?
    datetime.date = NewDate
    service = MyService()
    result = service.get_current_time()
    assert result.year == 1990

def test_we_are_in_the_21st_century():
    assert datetime.date.today().year >= 2000


if __name__ == "__main__":
    import numpy as np
    import pytest
    
    passed = 0
    n_iter = 100
    orig_val = datetime.date
    for _ in range(n_iter):
        seed = np.random.randint(0, 10000)
        out = pytest.main(
            [__file__, "--randomly-seed", str(seed), "-vvv"],
            plugins=["randomly"],
        )
        if out == pytest.ExitCode.OK:
            passed += 1
        # give back original value to un-pollute global state
        datetime.date = orig_val
    print("passed_percent", passed / n_iter * 100, "%")
