"""
This exhibits test flakiness due to asynchronous code. The problem is that the
test does not wait for the background task to finish before asserting a
result that depends on the background task.
"""
# ----------------------------------
# implementation - record_keeper.py
# ----------------------------------
import asyncio
import aiofiles
import random

class RecordKeeper:
    def __init__(self, filepath):
        self.filepath = filepath

    async def update_file(self, contents):
        # mimic slow update
        await asyncio.sleep(random.randint(1, 3))
        
        async with aiofiles.open(self.filepath, "w") as f:
            print("writing to file")
            await f.write(contents)
            print("done writing to file")

# ----------------------------------
# test suite - test_record_keeper.py
# ----------------------------------
import pytest

@pytest.mark.asyncio
async def test_record_keeper(tmpdir):
    filepath = tmpdir / "test.txt"
    keeper = RecordKeeper(filepath)
    # update is performed in the background
    asyncio.create_task(keeper.update_file("hello world"))

    # wait for a fixed amount of time
    await asyncio.sleep(2)

    async with aiofiles.open(filepath, "r") as f:
        contents = await f.read()
        assert contents == "hello world"

if __name__ == "__main__":
    import pytest
    import numpy as np

    passed = 0
    n_iter = 10
    for _ in range(n_iter):
        seed = np.random.randint(0, 10000)
        out = pytest.main(
            [__file__, "--randomly-seed", str(seed), "-vvv"],
            plugins=["randomly", "asyncio"],
        )
        if out == pytest.ExitCode.OK:
            passed += 1
    print("passed_percent", passed / n_iter * 100, "%")
