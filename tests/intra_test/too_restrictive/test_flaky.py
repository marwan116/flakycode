"""A test that is too restrictive and as such is flaky

More specifically, we show a naive implementation of stack/unstack that
avoids handling a number of corner cases. This test is flaky because
it is possible to generate data that triggers these corner cases.
"""
# ----------------------------------
# implementation - frame_stacker.py
# ----------------------------------
import pandas as pd

class FrameStacker:
    def stack(self, data):
        return data.stack()

    def unstack(self, data):
        return data.unstack()


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
