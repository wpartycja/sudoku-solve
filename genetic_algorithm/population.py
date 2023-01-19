from candidate import Candidate
from global_var import DIM

import random
import numpy as np

class Population():

    def __init__(self, base_table):
        self.candidates = []
        self.legal_values = self.find_legal_values(base_table)
        self.population_quality = 0

    def find_legal_values(self, base_table):

        legal_table = [[[] for j in range(DIM)] for i in range(DIM)]
        legal_solutions = Candidate(base_table, legal_table)

        for row in range(DIM):
            for column in range(DIM):
                for value in range(10):
                    # Check for legal value in every cell
                    if (base_table[row][column] == 0) and not (
                        legal_solutions.is_number_in_column(column, value)
                    ) and not (legal_solutions.is_number_in_row(row, value)
                    ) and not (legal_solutions.is_number_in_block(row, column, value)):
                        legal_solutions.table[row][column].append(value)

                    # if value is already known (given at the begging)
                    elif base_table[row][column] != 0:
                        legal_solutions.table[row][column].append(base_table[row][column])
                        break

        return legal_solutions.table

    def new_population(self, base_table, cand_nr):

        for _ in range(cand_nr):
            cand = Candidate(base_table)

            for i in range(DIM):  # new row in candidate
                while len(set(cand.table[i])) != 9:  # we want a valid row
                    for j in range(DIM):
                        if base_table[i][j] != 0:  # if the place is declared in base table
                            cand.table[i][j] = base_table[i][j]
                        else:
                            cand.table[i][j] = random.choice(self.legal_values[i][j])
                
            self.candidates.append(cand)
        
    def update_candidates_quality(self):
        for candidate in self.candidates:
            candidate.update_quality()

    def update_populaiton_quality(self):
        self.update_candidates_quality()
        for cand in self.candidates:
            if cand.quality > self.population_quality:
                self.population_quality = cand.quality
        
    
    
