from copy import deepcopy
import random

from .board import Board
from .solution import Solution


class Ant:
    def __init__(self, board: Board, position: list[int]) -> None:
        random.seed(1330)
        self.board = board
        self.solution = Solution(deepcopy(self.board.puzzle))
        self.start_position = deepcopy(position)
        self.position = deepcopy(position)

    def move(self) -> None:
        if self.position[0] != self.board.size - 1:
            self.position[0] += 1
        else:
            self.position[0] = 0
            if self.position[1] != self.board.size - 1:
                self.position[1] += 1
            else:
                self.position[1] = 0

    def set_solution(self, val: int) -> None:
        self.solution.solution_matrix[self.position[1]][self.position[0]] = val
