"""
This shows a gnarly issue with datetime arithmetic, timezones and
different tz libraries.
"""
import numpy as np
import pytest
import pytz
from dateutil import tz
from datetime import datetime, timedelta


class ThirdPartyDateOffseter:
    def __init__(self, date_str: str, timezone: str = "America/New_York"):
        self.tz = tz.gettz(timezone)
        self.dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").astimezone(self.tz)

    def offset(self, num_days: int):
        utc = (self.dt.astimezone(tz.UTC) + timedelta(days=num_days))
        return utc.astimezone(self.tz)


class MyDateOffseter:
    def __init__(self, date_str: str, timezone: str = "America/New_York"):
        self.dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").astimezone(
            pytz.timezone(timezone)
        )

    def offset(self, num_days: int):
        return self.dt + timedelta(days=num_days)


def test_my_date_offseter_consistent_with_thirdparty_offseter():
    start_dt = "2018-02-14 12:00:00"
    offset = np.random.randint(0, 100)
    my_new_dt = MyDateOffseter(start_dt).offset(offset).strftime("%Y-%m-%d %H:%M:%S%z")
    third_party_dt = (
        ThirdPartyDateOffseter(start_dt).offset(offset).strftime("%Y-%m-%d %H:%M:%S%z")
    )

    # this assertion will be True as long as the offset doesn't cross a DST boundary
    assert my_new_dt == third_party_dt


if __name__ == "__main__":
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
