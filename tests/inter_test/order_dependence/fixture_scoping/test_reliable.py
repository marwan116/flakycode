"""
This test showcases how to resolve flakiness due to an implicit ordering dependence
between tests created by a fixture that is scoped to the module level - i.e. if the
fixture was properly scoped to the function level, the test would not be flaky.
"""

# ----------------------------------
# Implementation - tic_tac_toe.py
# ----------------------------------
import numpy as np

class TicTacToeSimulation:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.moves_made = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.moves_made < 9:
            self.moves_made += 1
            return self
        raise StopIteration

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"

# ----------------------------------
# test suite - test_tic_tac_toe.py
# ----------------------------------
import pytest

@pytest.fixture(scope="function")
def tic_tac_toe_simulation():
    return TicTacToeSimulation()


def test_winning_move(tic_tac_toe_simulation):
    for _ in tic_tac_toe_simulation:
        tic_tac_toe_simulation.make_move(0, 0)
        tic_tac_toe_simulation.make_move(0, 1)
        tic_tac_toe_simulation.make_move(1, 1)
        tic_tac_toe_simulation.make_move(1, 0)
        tic_tac_toe_simulation.make_move(2, 2)
    board = tic_tac_toe_simulation.board
    assert board == [["X", "O", " "], ["O", "X", " "], [" ", " ", "X"]]


if __name__ == "__main__":
    passed = 0
    n_iter = 1
    for _ in range(n_iter):
        seed = np.random.randint(0, 10000)
        out = pytest.main(
            [__file__, "--randomly-seed", str(seed), "-vvv"],
            plugins=["randomly"],
        )
        if out == pytest.ExitCode.OK:
            passed += 1
    print("passed_percent", passed / n_iter * 100, "%")
