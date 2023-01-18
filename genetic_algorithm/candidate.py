import numpy as np
import random
from typing import Optional


from global_var import DIM


class Candidate:
    def __init__(self, base_table: np.array[np.array[int]], table: Optional[np.array] = None) -> None:
        self.base_table = base_table
        self.table = np.zeros((DIM, DIM), dtype=int) if table is None else table
        self.quality = 0

# Check numbers that already exists in row/column/block

    def is_number_in_row(self, row: int, number: int) -> bool:
        """
        method checks if given number is in particular row
        """
        for column in range(DIM):
            if self.base_table[row][column] == number:
                return True
        return False

    def is_number_in_column(self, column: int, number: int) -> bool:
        """
        method checks if given number is in particular column
        """
        for row in range(DIM):
            if self.base_table[row][column] == number:
                return True
        return False

    def is_number_in_block(self, x: int, y: int, number: int) -> bool:
        """
        method checks if the number exist in a block,
        where new number will be put
        x, y - coordinates
        """

        # coordinates of starting cells in block
        # - top-left corner
        block_x = x//3 * 3
        block_y = y//3 * 3

        values = set()
        for row in range(block_x, block_x + 3):
            for column in range(block_y, block_y + 3):
                values.add(self.base_table[row][column])

        return True if number in values else False

# Calculating quality

    def calculate_row_quality(self) -> float:
        """
        method calculates quality looking only for rows
        """
        row_quality = 0
        row_values = set()

        for row in self.table:
            for cell in row:
                row_values.add(cell)

            row_quality += len(row_values)/DIM/DIM
            row_values = set()

        return row_quality

    def calculate_column_quality(self) -> float:
        """
        method calculates quality looking only for columns
        """
        column_quality = 0
        column_values = set()

        for column in range(DIM):
            for row in range(DIM):
                column_values.add(self.table[row][column])

            column_quality += len(column_values)/DIM/DIM
            column_values = set()

        return column_quality

    def calculate_block_quality(self) -> float:
        """
        method calculates quality looking only for blocks
        """
        block_quality = 0
        block_values = set()

        for column in range(0, DIM, 3):
            for row in range(0, DIM, 3):

                for i in range(row, row + 3):
                    for j in range(column, column + 3):
                        block_values.add(self.table[i][j])

                block_quality += len(block_values)/DIM/DIM
                block_values = set()

        return block_quality

    def update_quality(self) -> None:
        """
        if there are no duplicates nowhere quality = 1
        if there are somewhere quality would be lower
        """

        row_quality = self.calculate_row_quality()
        column_quality = self.calculate_column_quality()
        block_quality = self.calculate_block_quality()

        self.quality = block_quality * column_quality * row_quality

# Mutation

    def mutate(self, mutation_rate):
        """
        performs mutation by picking random row and then 
        choosing two numbers to swap
        """

        rate = random.uniform(0, 1)

        if rate < mutation_rate:
            while True:

                row = random.randint(0, 8)

                col1 = 0
                col2 = 0
                while col1 == col2:
                    col1 = random.randint(0, 8)
                    col2 = random.randint(0, 8)
                
                # Check if we are not changing given base table
                if self.base_table[row][col1] == self.base_table[row][col2] == 0:
                    # Change if we do not duplicate values in column/block
                    # in reference to base table
                    if (not self.is_number_in_column(col1, self.table[row][col2])
                        and not self.is_number_in_column(col2, self.table[row][col1])
                        and not self.is_number_in_block(row, col1, self.table[row][col2])
                        and not self.is_number_in_block(row, col2, self.table[row][col1])):

                        # Swap values
                        temp = self.table[row][col1]
                        self.table[row][col1] = self.table[row][col2]
                        self.table[row][col2] = temp
                        break
        
        



