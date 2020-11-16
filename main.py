from solver import Solver
from puzzle import *

if __name__ == "__main__":
    width = 5
    length = 10

    puzzle = Puzzle(width, length)
    solver = Solver(puzzle)

    print(puzzle)

    print(" - - - - -" * 8)

    print("Tokens available : {}".format(puzzle.tokens_available))
    puzzle.display()

    print(" - - - - -" * 8)

    print("Original Score :", puzzle.score)

    solver.solve()

    print(" - - - - -" * 8)

    print("Total Combinations:", solver.total_token_combinations())

    print("Highest Score: ", solver.highest_score)

    print(" - - - - -" * 8)

    solved_puzzle = solver.highest_score_puzzle

    solved_puzzle.display()
