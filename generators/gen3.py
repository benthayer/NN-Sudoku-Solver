import os

import random


def str_to_array(grid_str):
    grid = list(map(lambda x: -1 if x is '.' else int(x) - 1, grid_str))
    return grid


def array_to_str(grid):
    grid_str = ''
    for item in grid:
        grid_str += str(item+1) if item != -1 else '.'
    return grid_str


def array_to_vec(grid):
    vec = []
    for num in grid:
        one_hot = [0]*9
        one_hot[num] = 1
        vec.extend(one_hot)
    return vec


def vec_to_array(vec):
    grid = []
    for i, num in enumerate(vec):
        if num:
            grid.append(i % 9)
    return grid


# List of sudoku puzzles "puzzles.txt" downloaded from magictour.free.fr/sudoku.htm as "top2365.txt",
# Training solutions "solutions.txt" was generated using gen3_solutions.py and sudoku-solver
def load_puzzles():
    puzzles = []
    with open(os.path.join(os.path.dirname(__file__), 'data/puzzles.txt')) as puzzle_file:
        for puzzle in puzzle_file:
            puzzle = str_to_array(puzzle.strip())
            puzzles.append(puzzle)
    return puzzles


def load_solutions():
    solutions = []
    with open(os.path.join(os.path.dirname(__file__), 'data/solutions.txt')) as solution_file:
        for solution in solution_file:
            solution = str_to_array(solution.strip())
            solutions.append(solution)
    return solutions


all_puzzles = load_puzzles()
all_solutions = load_solutions()


def get_permutation():
    mapping = list(range(9))
    random.shuffle(mapping)
    return mapping


def get_constrained_permutation():
    mapping = [0]*9
    large_mapping = list(range(3))
    random.shuffle(large_mapping)
    for i in range(3):
        small_mapping = list(range(3))
        random.shuffle(small_mapping)
        for j in range(3):
            mapping[i*3 + j] = large_mapping[i]*3 + small_mapping[j]
    return mapping


def get_grid_permutations(permutations=(None, None, None)):
    new_permutations = [get_constrained_permutation(),
                        get_constrained_permutation(),
                        get_permutation()]

    for i in range(3):
        if permutations[i] is not None:
            new_permutations[i] = permutations[i]

    return tuple(new_permutations)


def permute_rows(grid, permutation=None):
    if permutation is None:
        permutation = get_constrained_permutation()
    new_grid = []
    for row in range(9):
        for col in range(9):
            new_grid.append(grid[permutation[row] * 9 + col])
    return new_grid


def permute_columns(grid, permutation=None):
    if permutation is None:
        permutation = get_constrained_permutation()
    new_grid = []
    for row in range(9):
        for col in range(9):
            new_grid.append(grid[row * 9 + permutation[col]])
    return new_grid


def permute_numbers(grid, permutation=None):
    if permutation is None:
        permutation = get_permutation()
    new_grid = [0]*9**2
    for i in range(9**2):
        new_grid[i] = permutation[grid[i]] if grid[i] != -1 else -1
    return new_grid


def permute(grid, permutations=(None, None, None)):
    grid = permute_rows(grid, permutations[0])
    grid = permute_columns(grid, permutations[1])
    grid = permute_numbers(grid, permutations[2])
    return grid


def get_random_puzzle():
    index = random.randrange(len(all_puzzles))
    puzzle = all_puzzles[index]
    return puzzle


def get_permuted_puzzle():
    puzzle = get_random_puzzle()
    return permute(puzzle)


def get_random_solution():
    index = random.randrange(len(all_solutions))
    solution = all_solutions[index]
    return solution


def get_permuted_solution():
    solution = get_random_solution()
    return permute(solution)


def get_random_pair():
    index = random.randrange(len(all_puzzles))
    puzzle = all_puzzles[index]
    solution = all_solutions[index]
    return puzzle, solution


def permute_pair(puzzle, solution, permutations=(None, None, None)):
    permutations = get_grid_permutations(permutations)
    puzzle = permute(puzzle, permutations)
    solution = permute(solution, permutations)
    return puzzle, solution


def get_permuted_pair():
    puzzle, solution = get_random_pair()
    return permute_pair(puzzle, solution)


def get_batch(batch_size=1000):
    puzzle_batch = []
    solution_batch = []
    for i in range(batch_size):
        puzzle, solution = get_permuted_pair()

        puzzle_batch.append(puzzle)
        solution_batch.append(solution)

    return puzzle_batch, solution_batch


def get_vector_batch(batch_size=1000):
    # TODO I should probably put this into GameBoard
    puzzles, solutions = get_batch(batch_size)
    vec_puzzles = []
    vec_solutions = []
    for i in range(batch_size):
        vec_puzzles.append(array_to_vec(puzzles[i]))
        vec_solutions.append(array_to_vec(solutions[i]))
    return vec_puzzles, vec_puzzles
