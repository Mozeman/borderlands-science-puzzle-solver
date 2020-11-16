from solver import Solver
from puzzle import *

R = Tile.RED
G = Tile.GREEN
B = Tile.BLUE
P = Tile.PURPLE
T = Tile.TOKEN
E = Tile.EMPTY

if __name__ == "__main__":
    width, length = 5, 5

    columns = [
        Column([G, B, B, E, E]),
        Column([R, P, E, E, E]),
        Column([G, P, E, E, E]),
        Column([R, G, B, E, E]),
        Column([P, P, B, E, E])
        ]

    puzzle = Puzzle(width, length, up_to=3, starting_tokens=2, row_matches=RowMatches.random(length), columns=columns)

    print(puzzle)

    print(" - - - - -" * 8)

    puzzle.display()
    print("Original Score :", puzzle.score)

    print(" - - - - -" * 8)

    print("Bumping Column 2")
    puzzle.bump_column(2)

    puzzle.display()
    print("New Score :", puzzle.score)

    print(" - - - - -" * 8)

    print("Bumping Column 4")
    puzzle.bump_column(4)

    puzzle.display()
    print("New Score :", puzzle.score)

    print(" - - - - -" * 8)

    new_puzzle = Puzzle(width, length, up_to=3, starting_tokens=2, columns=columns)

    print("- - - New Puzzle - - -".center(80))
    print(new_puzzle)

    print(" - - - - -" * 8)

    new_puzzle.display()
    print("Original Score :", new_puzzle.score)

    print(" - - - - -" * 8)

    print("Bumping Columns 1 & 3")
    new_puzzle.bump_column(1, 3)

    new_puzzle.display()
    print("New Score :", new_puzzle.score)