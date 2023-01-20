import numpy as np

from global_var import DIM
from population import Population
from candidate import Candidate

class Sudoku:

    def __init__(self, path, candidates_number, generations, mutation_rate, selection_rate, crossover_rate, elite_size):
        with open (path, "r") as file:
            self.base_table = np.loadtxt(file).reshape((DIM, DIM)).astype(int)
            self.candidates_number = candidates_number
            self.generations = generations
            self.mutation_rate = mutation_rate
            self.selection_rate = selection_rate
            self.crossover_rate = crossover_rate
            self.elite_size = elite_size
    
    def solve(self):
        self.population = Population(self.base_table, self.selection_rate, self.crossover_rate)
        self.population.new_population(self.candidates_number)

        prev_quality = self.population.population_quality
        get_stucked = 0

        best_quality = self.population.population_quality

        for generation in range(self.generations):
            if generation % 10 == 0:
                print(f'Generation: {generation}')
            
            if generation % 100 == 0:
                print(self.population.best_candindate.table)
                        
            next_population = []

            # select elites
            elites = self.population.get_elite(self.elite_size)

            # select rest of the candidates

            for _ in range(self.candidates_number - self.elite_size // 2):
                # tournament
                parent1 = self.population.tournament()
                parent2 = self.population.tournament()

                # crossover
                child1, child2 = self.population.crossover(parent1, parent2)

                child1.mutate(self.mutation_rate)
                child2.mutate(self.mutation_rate)

                next_population.extend([child1, child2])
            
            prev_quality = best_quality
            best_quality = self.population.population_quality

            if best_quality == prev_quality:
                get_stucked  += 1
                
            if best_quality >= 1:
                print(f' Solution found at generation {generation}! Here it comes:')
                print(self.population.best_candindate.table)
                return 
            else: 
                if generation % 10 == 0:
                    print(f'Best quality is: {self.population.population_quality}')
                    print(f'Column quality: {self.population.best_candindate.calculate_column_quality()}')
                    print(f'Block quality: {self.population.best_candindate.calculate_block_quality()}')
            
            if get_stucked > 100:
                self.population.new_population(self.candidates_number)
                prev_quality = self.population.population_quality
                get_stucked = 0

                best_quality = self.population.population_quality
                continue

            
            # at the end not to be affected by crossover / mutation
            next_population.extend(elites) if self.elite_size != 1 else next_population.append(elites)

            # Next population
            self.population.candidates = next_population
            self.population.update_candidates_quality()
            self.population.update_population_quality()

sudoku = Sudoku('./sudoku_mid.txt', candidates_number=500, generations=1000, mutation_rate=1, selection_rate=0.5, crossover_rate=0.8, elite_size=50)
sudoku.solve()
            


            

