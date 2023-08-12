"""
This is an example of a flaky test where one test modifies the filesystem
and does not clean up after itself. This causes the second test to fail
if executed in the wrong order.
"""
import pytest
import time
from pathlib import Path


@pytest.fixture
def temp_file():
    # we use a local Path object to avoid the cloud costs and setup
    s3_filepath = Path("s3://my-bucket/my-file.txt")
    s3_filepath.parent.mkdir(parents=True, exist_ok=True)

    # mimic a write to S3
    with open(s3_filepath, "w") as f:
        f.write("Hello, world!")
        time.sleep(1)

    yield s3_filepath

    # mimic a delete from S3
    s3_filepath.unlink()
    s3_filepath.parent.rmdir()
    s3_filepath.parent.parent.rmdir()


def test_file_contents(temp_file):
    with open(temp_file, "r") as f:
        contents = f.read()
    assert contents == "Hello, world!"


if __name__ == "__main__":
    # use multiple processes to demonstrate the flakiness
    from concurrent.futures import ProcessPoolExecutor

    num_concurrent_processes = 4
    with ProcessPoolExecutor(max_workers=10) as executor:
        outputs = [
            executor.submit(
                pytest.main,
                [__file__],
                plugins=[],
            )
            for _ in range(num_concurrent_processes)
        ]

    passed = 0
    for i, out in enumerate(outputs, start=1):
        if out.result() == pytest.ExitCode.OK:
            passed += 1

    print(f"{passed}/{num_concurrent_processes} passed")