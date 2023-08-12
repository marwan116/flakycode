"""Showcases how to make use of hypothesis to uncover edge cases in your code."""
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
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.pandas import column, data_frames

@given(data=data_frames(
    columns=[
        column(
            name="A",
            dtype=float,
            elements=st.floats(allow_nan=True)
        ),
        column(
            name="B",
            dtype=float,
            elements=st.floats(allow_nan=True)
        ),
    ],
))
@settings(max_examples=100) 
def test_stack_unstack_roundtrip(data):
    stacker = FrameStacker(data.dtypes)
    stacked = stacker.stack(data)
    output = stacker.unstack(stacked)
    pd.testing.assert_frame_equal(output, data)

