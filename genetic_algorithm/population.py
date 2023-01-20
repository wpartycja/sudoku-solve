from candidate import Candidate
from global_var import DIM

import random
import numpy as np

class Population():

    def __init__(self, base_table, selection_rate, crossover_rate):
        self.candidates = []
        self.base_table = base_table
        self.legal_values = self.find_legal_values(base_table)
        self.population_quality = 0
        self.selection_rate = selection_rate
        self.crossover_rate = crossover_rate
        self.best_candindate = Candidate(base_table)

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

    def new_population(self, cand_nr):

        for _ in range(cand_nr):
            cand = Candidate(self.base_table)

            for i in range(DIM):  # new row in candidate
                while len(set(cand.table[i])) != 9:  # we want a valid row
                    for j in range(DIM):
                        if self.base_table[i][j] != 0:  # if the place is declared in base table
                            cand.table[i][j] = self.base_table[i][j]
                        else:
                            cand.table[i][j] = random.choice(self.legal_values[i][j])
                
            self.candidates.append(cand)
            self.update_candidates_quality()
            self.update_population_quality()

        
    def update_candidates_quality(self):
        for candidate in self.candidates:
            candidate.update_quality()

    def update_population_quality(self):
        self.update_candidates_quality()
        for cand in self.candidates:
            if cand.quality > self.population_quality:
                self.population_quality = cand.quality
                self.best_candindate = cand
    
    def get_elite(self, elite_size):
        elite = sorted(self.candidates, key=lambda c: c.quality, reverse=True)[:elite_size-1]
        return elite
        
    def tournament(self):
        cand1 = random.choice(self.candidates)
        cand2 = random.choice(self.candidates)

        if cand1.quality > cand2.quality:
            stronger, weaker = cand1, cand2
        else:
            stronger, weaker = cand2, cand1

        rate = random.uniform(0, 1)
        
        return stronger if rate < self.selection_rate else weaker
    
    def crossover(self, parent1, parent2):

        nr_rows_parent1 = random.randint(1, 8)
        rows1_idx = set()

        while len(rows1_idx) != nr_rows_parent1:
            rows1_idx.add(random.randint(0, 8))

        child1 = Candidate(self.base_table)
        child2 = Candidate(self.base_table)
        for row in range(9):
            if row in rows1_idx:
                child1.table[row] = parent1.table[row]
                child2.table[row] = parent2.table[row]
            else:
                child1.table[row] = parent2.table[row]
                child2.table[row] = parent1.table[row]
        
        return child1, child2


    
    
    
