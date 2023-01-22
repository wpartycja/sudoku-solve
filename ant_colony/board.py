import numpy as np


class Board:
    def __init__(self, size: int, puzzle: list[list[int]]) -> None:
        self.size = size
        self.puzzle = puzzle
        self.pheromones = np.ones((size, size, 9)) / size
        self.values = np.zeros((size, size))
        self.possible_moves = [[[] for _ in range(size)] for _ in range(size)]

    def reset(self) -> None:
        self.pheromones = np.ones((self.size, self.size, 9)) / self.size**2

    def set_possible_values(self) -> None:
        self.possible_moves = [
            [[] for _ in range(self.size)] for _ in range(self.size)
        ]
        for row in range(self.size):
            for column in range(self.size):
                possible_moves = list()
                if self.puzzle[column][row]:
                    possible_moves.append(self.puzzle[column][row])
                else:
                    for value in range(10):
                        if (
                            self.check_row(column, value) and
                            self.check_column(row, value) and
                            self.check_box(column, row, value)
                        ):
                            possible_moves.append(value)

                self.possible_moves[column][row] += (possible_moves)

    def check_row(self, row: int, value: int) -> bool:
        return False if value in self.puzzle[row][:] else True

    def check_column(self, column: int, value: int) -> bool:
        return False if value in [row[column] for row in self.puzzle] else True

    def check_box(self, row: int, column: int, value: int) -> bool:
        block_start = (row // 3 * 3, column // 3 * 3)
        block_end = (block_start[0] + 3, block_start[1] + 3)

        return False if value in [
            x for row in self.puzzle[block_start[0]:block_end[0]]
            for x in row[block_start[1]:block_end[1]]
        ] else True
