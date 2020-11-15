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

    print("Score :", puzzle.score)
    # puzzle.bump_column(0, 1, 3, 3, 4)

    solver.solve()
