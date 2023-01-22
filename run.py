from ant_colony.aco import ACO


if __name__ == '__main__':
    ant_solver = ACO(size=9, ants=1)
    ant_solver.solve('./ant_colony/sudoku_mid.txt')
