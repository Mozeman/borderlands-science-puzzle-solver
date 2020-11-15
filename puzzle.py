
import enum
import random

from colorama import init, Back, Fore, Style
from typing import List, Tuple, Union, Optional

# Colorama init
init()


class Tile(enum.Enum):
    EMPTY = -1
    TOKEN = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    PURPLE = 4

    @staticmethod
    def random() -> "Tile":
        return Tile(random.randint(1, 4))

    @staticmethod
    def random_pair() -> Tuple["Tile", "Tile"]:
        first = Tile.random()

        second = Tile.random()
        while second == first:
            second = Tile.random()

        return first, second

    def __str__(self):
        if self == Tile.RED:
            return Fore.RED + self.name + Style.RESET_ALL
        elif self == Tile.GREEN:
            return Fore.GREEN + self.name + Style.RESET_ALL
        elif self == Tile.BLUE:
            return Fore.BLUE + self.name + Style.RESET_ALL
        elif self == Tile.PURPLE:
            return Fore.MAGENTA + self.name + Style.RESET_ALL
        elif self == Tile.TOKEN:
            return Fore.YELLOW + self.name + Style.RESET_ALL
        elif self == Tile.EMPTY:
            return Fore.WHITE + "'    '" + Style.RESET_ALL
        else:
            return self.name

    def char(self) -> str:
        if self == Tile.RED:
            return Fore.RED + self.name[0] + Style.RESET_ALL
        elif self == Tile.GREEN:
            return Fore.GREEN + self.name[0] + Style.RESET_ALL
        elif self == Tile.BLUE:
            return Fore.BLUE + self.name[0] + Style.RESET_ALL
        elif self == Tile.PURPLE:
            return Fore.MAGENTA + self.name[0] + Style.RESET_ALL
        elif self == Tile.TOKEN:
            return Fore.YELLOW + self.name[0] + Style.RESET_ALL
        elif self == Tile.EMPTY:
            return Fore.WHITE + "'    '" + Style.RESET_ALL
        else:
            return self.name[0]


class RowMatches:
    def __init__(self, values: List[Tuple]):
        self.values = values
        self.height = len(values)

    def __str__(self):
        sb = ""
        for v in self.values:
            if len(v) == 1:
                tile: Tile = v[0]
                sb += ' ' + tile.char().center(11) + ' \n'
            else:
                first: Tile = v[0]
                second: Tile = v[1]

                sb += ' {} {} '.format(first.char(), second.char()).center(5) + '\n'
        return sb

    def __getitem__(self, index) -> Union[Tuple[Tile], Tuple[Tile, Tile]]:
        return self.values[index]

    @staticmethod
    def to_string(v: Union[Tuple[Tile, Tile], Tuple[Tile]]):
        x = 2
        y = x - 1
        if len(v) == 1:
            tile: Tile = v[0]
            return " " * x + tile.char() + " " * x
        else:
            first: Tile = v[0]
            second: Tile = v[1]
            return " " * y + f'{first.char()} {second.char()}' + " " * y

    @staticmethod
    def random(height: int) -> "RowMatches":
        values: List[Tuple] = []
        for _ in range(height):
            r = random.randint(1, 2)

            if r == 1:

                values.append(tuple([Tile.random()]))

            else:
                values.append(Tile.random_pair())

        return RowMatches(values)


class Column:
    def __init__(self, values: List[Tile]):
        self.values: List[Tile] = values

    def __str__(self):
        return str(self.values)

    def __getitem__(self, index) -> Tile:
        return self.values[index]

    def __setitem__(self, index, tile: Tile):
        self.values[index] = tile

    @staticmethod
    def generate_empty(height: int) -> "Column":
        values = [Tile.EMPTY for _ in range(height)]
        return Column(values)

    @staticmethod
    def generate_random_full(height: int) -> "Column":
        values = [Tile.random() for _ in range(height)]
        return Column(values)

    @staticmethod
    def generate_random(height: int, up_to: int = None) -> "Column":
        if up_to is None or not isinstance(up_to, int) or up_to < 0:
            up_to = height

        if up_to > height:
            raise Exception("up_to '{}' must be equal or less than height '{}'".format(up_to, height))

        if up_to == 0:
            column = Column.generate_empty(height)
        else:
            column = Column.generate_random_full(height)
            r = random.randint(1, up_to)

            for i in range(height):
                if i >= r:
                    column[i] = Tile.EMPTY

        return column

    def bump(self) -> "Column":
        self.values = [Tile.TOKEN] + self.values
        return self


class Puzzle:
    def __init__(self, width: int, length: int, up_to: int = None, starting_tokens: int = 5,
                 row_matches: RowMatches = None, columns: List[Column] = None):
        self.width: int = width
        self.length: int = length
        self.up_to: int = up_to or length
        self.row_matches: RowMatches = row_matches

        self.STARTING_TOKENS: int = starting_tokens
        self.used_tokens: int = 0

        self.columns: List[Column] = columns or [Column.generate_random(length, up_to) for _ in range(width)]

        if row_matches is None:
            self.row_matches = RowMatches.random(length)

    @property
    def area(self):
        return self.width * self.length

    @property
    def tokens_available(self):
        return self.STARTING_TOKENS - self.used_tokens

    @property
    def score(self) -> int:
        final = self.reorder()

        total = 0
        for i in range(self.length):
            row = final[i]
            row_match = self.row_matches[i]
            for tile in row:
                if tile in row_match:
                    total += 1

        return total

    def __str__(self):
        return "Puzzle Object : [ width : {}, length: {}, area: {}, up_to: {}, starting_tokens: {}]"\
            .format(self.width, self.length, self.area, self.up_to, self.STARTING_TOKENS)

    def __getitem__(self, index) -> Column:
        return self.columns[index]

    def duplicate(self):
        return Puzzle(self.width, self.length, self.up_to, self.STARTING_TOKENS, self.row_matches, self.columns)

    def bump_column(self, *index):
        for i in index:
            if self.tokens_available > 0:
                column = self[i]
                column.bump()
                self.used_tokens += 1

    def reorder(self) -> list[list[Tile]]:
        final = []
        for i in range(self.length):
            temp = []
            for column in self.columns:
                temp.append(column[i])
            final.append(temp)
        return final

    def display_grid(self):
        final = self.reorder()

        sb = "|"
        for j in range(self.length - 1, -1, -1):

            for tile in final[j]:
                sb += " " + str(tile).center(15) + " |"
            if j > 0:
                sb += "\n|"
        print(sb)

    def display(self):
        final = self.reorder()

        sb = "|"
        for j in range(self.length - 1, -1, -1):

            row_match = self.row_matches[j]
            sb += RowMatches.to_string(row_match) + "|"

            for tile in final[j]:
                if tile in row_match:
                    sb += " " + Back.WHITE + Style.BRIGHT + str(tile).center(15) + " " + Style.RESET_ALL + "|"
                else:
                    sb += " " + Style.DIM + str(tile).center(15) + Style.RESET_ALL + " |"
            if j > 0:
                sb += "\n|"
        print(sb)

