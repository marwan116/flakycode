"""A test that is too restrictive and as such is flaky

More specifically, we show a naive implementation of stack/unstack that
avoids handling a number of corner cases. This test is flaky because
it is possible to generate data that triggers these corner cases.
"""
# ----------------------------------
# implementation - frame_stacker.py
# ----------------------------------
import pandas as pd

sentinel_val = object()

class FrameStacker:

    def __init__(self):
        self._dtypes = None

    def stack(self, data):
        # store dtypes
        self._dtypes = data.dtypes
        
        # handle case where data is empty
        if data.empty:
            return data

        # handle case where data contains nan values
        data = data.fillna(sentinel_val)

        # perform the stack
        return data.stack()

    def unstack(self, data):
        # handle case where data is empty
        if data.empty:
            return data
        # perform the unstack
        data = data.unstack()
        # replace sentinel values with nan
        data[data == sentinel_val] = np.nan
        # convert to original dtypes
        return data.astype(self._dtypes)


# ----------------------------------
# test suite - test_frame_stacker.py
# ----------------------------------
import pytest
import numpy as np

@pytest.fixture
def data():
    """A way to mimick randomly generated data."""
    nrows = np.random.randint(0, 10)
    return pd.DataFrame({
        "A": np.random.choice(
            [1.0, 2.0, 3.0, np.nan], size=nrows
        ),
        "B": np.random.choice(
            [1.0, 2.0, 3.0, np.nan], size=nrows
        ),
    })

def test_stack_unstack_roundtrip(data):
    stacker = FrameStacker()
    stacked = stacker.stack(data)
    output = stacker.unstack(stacked)
    pd.testing.assert_frame_equal(output, data)


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
