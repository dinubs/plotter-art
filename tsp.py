import mlrose

# Create list of city coordinates
coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3)]

# Initialize fitness function object using coords_list
fitness_coords = mlrose.TravellingSales(coords=coords_list)

problem_fit = mlrose.TSPOpt(
    length=8, fitness_fn=fitness_coords, maximize=False)

best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)
print(best_state)
