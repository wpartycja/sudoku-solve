import numpy as np
from typing import Optional


from global_var import DIM


class Candidate:
    def __init__(self, table: Optional[np.array] = None) -> None:
        self.table = np.zeros((DIM, DIM), dtype=int) if table is None else table
        self.quality = None

# Check if there will beduplicates

    def is_number_in_row(self, row: int, number: int) -> bool:
        """
        method checks if given number is in particular row
        """
        for column in range(DIM):
            if self.table[row][column] == number:
                return True
        return False

    def is_number_in_column(self, column: int, number: int) -> bool:
        """
        method checks if given number is in particular column
        """
        for row in range(DIM):
            if self.table[row][column] == number:
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
                values.add(self.table[row][column])

        return True if number in values else False
