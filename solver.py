from itertools import combinations_with_replacement
from math import factorial
from puzzle import Puzzle
from typing import Optional, Tuple, List


class Solver:
    def __init__(self, puzzle: Puzzle, target_score: int = None):
        self.puzzle: Puzzle = puzzle
        self.target_score: int = target_score
        self.highest_score: int = puzzle.score
        self.highest_score_puzzle: Puzzle = Optional[None]
        self.processed_puzzles: List[Tuple[int, Puzzle]] = []

    @property
    def tokens(self):
        return self.puzzle.tokens_available

    @property
    def possibilities(self) -> list[tuple[int, ...]]:
        combinations = []
        for i in range(1, 5):
            combinations += list(combinations_with_replacement(range(self.puzzle.width), i))
        return combinations

    def total_token_combinations(self) -> int:
        total = 0
        width = self.puzzle.width
        for i in range(width):
            sample = i + 1
            combinations = factorial(width + i) // (factorial(sample) * factorial(width - 1))
            total += combinations
        return total

    def solve(self):
        i = 0
        for comb in self.possibilities:
            i += 1
            test_puzzle = self.puzzle.duplicate_original()

            if test_puzzle.tokens_available != test_puzzle.STARTING_TOKENS:
                raise Exception("Puzzle not starting")

            test_puzzle.bump_column(*comb)

            self.processed_puzzles.append((test_puzzle.score, test_puzzle))

            if test_puzzle.score > self.highest_score:
                self.highest_score = test_puzzle.score
                self.highest_score_puzzle = test_puzzle.duplicate_original()
            if i <= 5:
                print(" - - - - -" * 8)

                test_puzzle.display()

                print(f"Combinations: {comb}")
                print(f"Score {i}: {test_puzzle.score}")
