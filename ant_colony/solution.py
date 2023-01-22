
class Solution:
    def __init__(self, solution: list[list[int]]) -> None:
        self.solution_matrix = solution
        self.size = len(self.solution_matrix)

    @staticmethod
    def evaluate_line(line: list[int]) -> float:
        return len(set(line)) / len(line)**2

    def evaluate_rows(self) -> float:
        return sum(
            [Solution.evaluate_line(row) for row in self.solution_matrix]
        )

    def evaluate_columns(self) -> float:
        return sum(
            [Solution.evaluate_line(
                [row[column] for row in self.solution_matrix]
            ) for column in range(self.size)]
        )

    def evaluate_boxes(self) -> float:
        return sum(
            [Solution.evaluate_line(
                [x for row in self.solution_matrix[row:row+3]
                 for x in row[column:column+3]]
            ) for row in range(0, self.size, 3)
              for column in range(0, self.size, 3)]
        )

    def evaluate(self) -> float:
        return sum([
            self.evaluate_rows(),
            self.evaluate_columns(),
            self.evaluate_boxes()
        ])
