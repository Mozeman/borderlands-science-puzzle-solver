import random
from puzzle import Puzzle


class Solver:
    def __init__(self, puzzle: Puzzle, target_score: int = None):
        self.puzzle: Puzzle = puzzle
        self.target_score: int = target_score

    @property
    def tokens(self):
        return self.puzzle.tokens_available

    def solve(self):
        test_puzzle = self.puzzle.duplicate()
        for i in range(self.tokens):
            x = random.randint(0, test_puzzle.width - 1)
            test_puzzle.bump_column(x)

            print(" - - - - -" * 8)

            print("TEST PUZZLE {} FROM SOLVER. BUMPED COLUMN {}".format(i, x + 1).center(80))

            print(" - - - - -" * 8)

            test_puzzle.display()

            print(" - - - - -" * 8)

            print("Score :", test_puzzle.score)
