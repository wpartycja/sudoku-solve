from random import randint, uniform, choices
from copy import deepcopy

import numpy as np

from .board import Board
from .solution import Solution
from .ant import Ant


class ACO:
    def __init__(
            self,
            size: int,
            ants: int,
            greediness: float = 0.1,
            evaporation: float = 0.8
    ) -> None:
        self.size = size
        self.ants = ants
        self.greediness = greediness
        self.evaporation = evaporation
        self.puzzle: list[list[int]]
        self.solution: Solution
        self.board: Board
        self.colony: list[Ant]

    def load_puzzle_from_txt(self, path: str) -> None:
        with open(path, "r", -1, 'utf-8') as file:
            self.puzzle = np.loadtxt(file)
        self.puzzle = self.puzzle.reshape((self.size, self.size)).astype(int)

    @staticmethod
    def is_solved(solution: Solution) -> bool:
        return True if solution.evaluate() >= 3 else False

    def create_colony(self) -> None:
        self.colony = [
            Ant(self.board,
                [randint(0, self.size-1), randint(0, self.size-1)])
            for _ in range(self.ants)
        ]

    def is_fixed(self, position: list[int]) -> bool:
        return True if len(
            self.board.possible_moves[position[1]][position[0]]
        ) == 1 else False

    def get_fixed_value(self, position: list[int]) -> int:
        return self.get_field_values(position)[0]

    def get_field_values(self, position: list[int]) -> list[int]:
        return self.board.possible_moves[position[1]][position[0]]

    def get_field_pheromones(self, position: list[int]) -> list[float]:
        return self.board.pheromones[position[1]][position[0]]

    def choose_selection(self) -> callable:
        return self.greedy_selection if uniform(0, 1) < self.greediness\
          else self.roulette_selection

    def roulette_selection(self, ant: Ant) -> int:
        values = [x for x in range(1, 10)]
        possible_values = self.get_field_values(ant.position)
        pheromones = self.get_field_pheromones(ant.position)

        value = 0
        while value not in possible_values:
            value = choices(values, pheromones)[0]

        idx = 0
        if not self.is_fixed(ant.position):
            while value in ant.solution.solution_matrix[ant.position[1]][:]:
                value = values[idx]
                idx += 1
        return value

    def greedy_selection(self, ant: Ant) -> int:
        possible_values = self.get_field_values(ant.position)
        pheromones = self.get_field_pheromones(ant.position)
        for value in range(1, 10):
            if (
                pheromones[value-1] == np.max(pheromones) and
                value in possible_values
            ):
                return value
        return possible_values[0]

    def update_pheromones(self, ant: Ant) -> None:
        for row in range(self.size):
            for column in range(self.size):
                value = int(ant.solution.solution_matrix[row][column])
                delta = ant.solution.evaluate()
                self.board.pheromones[row][column][value-1] += delta

    def evaporate_pheromones(self) -> None:
        for row in range(self.size):
            for column in range(self.size):
                for value in range(9):
                    curr_value = self.board.pheromones[row][column][value]
                    base_value = 1 / self.size
                    new_value = (1-self.evaporation) * curr_value\
                        + self.evaporation * base_value
                    self.board.pheromones[row][column][value] = new_value

    def find_best_ant(self) -> Ant:
        best_ant = self.colony[0]
        for ant in self.colony:
            if ant.solution.evaluate() > best_ant.solution.evaluate():
                best_ant = ant
        return ant

    def reset_solutions(self) -> None:
        for ant in self.colony:
            ant.solution = Solution(deepcopy(self.puzzle))

    def solve(self, path: str) -> None:
        self.load_puzzle_from_txt(path)

        self.board = Board(self.size, self.puzzle)
        self.board.reset()
        self.board.set_possible_values()

        self.create_colony()
        best_solution = Solution(self.puzzle)
        best_ant = self.colony[0]

        while not ACO.is_solved(best_solution):
            for _ in range(81):
                for ant in self.colony:
                    if self.is_fixed(ant.position):
                        ant.set_solution(self.get_fixed_value(ant.position))
                    else:
                        ant.set_solution(self.choose_selection()(ant))
                    ant.move()
            curr_best_ant = self.find_best_ant()
            if curr_best_ant.solution.evaluate() > best_solution.evaluate():
                best_ant = deepcopy(curr_best_ant)
                best_solution = deepcopy(best_ant.solution)
            self.update_pheromones(best_ant)
            self.evaporate_pheromones()
            self.reset_solutions()
            print(best_solution.evaluate()/3)

        print(best_solution.solution_matrix)
