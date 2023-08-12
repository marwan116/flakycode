from functools import lru_cache
import joblib
import pytest
import numpy as np
import pandas as pd
import psutil
from pathlib import Path


class MyData:
    def __init__(self, df) -> None:
        self.df = df

    def __hash__(self):
        hex_hash = joblib.hash(self.df)
        return int(hex_hash, 16)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.df.equals(other.df)
        return NotImplemented


def generate_data():
    return MyData(
        df=pd.DataFrame(
            # 64 bit float is 8 bytes x 2 columns x 1M rows ~ 16 million bytes ~ 16 MB
            np.random.normal(size=(1_000_000, 2)),
        )
    )

file_path = Path(__file__).parent / "memory_usage_reliable.csv"

def log_memory_usage_to_file():
    with open(file_path, "a") as f:
        f.write(f"{psutil.Process().memory_info().rss / 1024**2}\n")

def setup_memory_log_file():
    if file_path.exists():
        file_path.unlink()
    else:
        file_path.touch()
    log_memory_usage_to_file()

@lru_cache
def process_data(data):
    data.df.clip(0, 3, inplace=True)


def test_data_is_positive_after_processing():
    for _ in range(128):
        data = generate_data()
        try:
            process_data(data)
            assert (data.df < 0).sum().sum() == 0
        finally:
            process_data.cache_clear()
            log_memory_usage_to_file()



def test_data_is_clipped_at_three_after_processing():
    data = generate_data()
    try:
        process_data(data)
        assert (data.df > 3).sum().sum() == 0
    finally:
        process_data.cache_clear()
        log_memory_usage_to_file()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    setup_memory_log_file()
    pytest.main([__file__])
    df = pd.read_csv(
        file_path, header=None
    ).reset_index()
    fig, ax = plt.subplots(figsize=(12, 8))
    df.plot(x="index", y=0, ax=ax, color="blue", legend=False)
    ax.set_xlabel("Test Step")
    ax.set_ylim(0, 3_000)
    ax.set_ylabel("Memory Consumption (MB)", color="blue")
    ax.set_title("Memory Consumption vs Test Step")
    plt.show()
    plt.savefig(
        Path(__file__).parent / "memory_usage_reliable.png",
        bbox_inches="tight",
    )
