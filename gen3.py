import os

import numpy as np
import random

all_puzzles = None
all_solutions = None


def str_to_array(grid_str):
    grid = np.zeros([9, 9], np.int8)
    for i in range(9):
        grid[i] = list(map(lambda x: 0 if x is '.' else int(x), grid_str[i*9:i*9 + 9]))
    grid.shape = [9**2]
    return grid


def array_to_str(grid):
    grid.shape = [9, 9]
    grid_str = ''
    for row in grid:
        grid_str += ''.join([str(i) for i in row])
    return grid_str


# List of sudoku puzzles "puzzles.txt" downloaded from magictour.free.fr/sudoku.htm as "top2365.txt",
# Training solutions "solutions.txt" was generated using gen3_solutions.py and sudoku-solver
def load_puzzles():
    global all_puzzles
    all_puzzles = []
    with open(os.path.join(os.path.dirname(__file__), 'data/puzzles.txt')) as puzzle_file:
        for puzzle in puzzle_file:
            puzzle = str_to_array(puzzle)
            all_puzzles.append(puzzle)
        all_puzzles = np.array(all_puzzles)


def load_solutions():
    global all_solutions
    all_solutions = []
    with open(os.path.join(os.path.dirname(__file__), 'data/solutions.txt')) as solution_file:
        for solution in solution_file:
            solution = str_to_array(solution)
            all_solutions.append(solution)
    all_solutions = np.array(all_solutions)

load_puzzles()
load_solutions()


def get_permutation():
    mapping = np.array(range(9))
    np.random.shuffle(mapping)
    return mapping


def get_constrained_permutation():
    mapping = np.zeros(9, np.int8)
    large_mapping = np.array(range(3))
    np.random.shuffle(large_mapping)
    for i in range(3):
        small_mapping = np.array(range(3))
        np.random.shuffle(small_mapping)
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
    shape = grid.shape
    grid.shape = [9, 9]
    new_grid = np.zeros([9, 9], np.int8)
    for i in range(9):
        new_grid[i] = grid[permutation[i]]
    grid.shape = shape
    new_grid.shape = shape
    return new_grid


def permute_columns(grid, permutation=None):
    if permutation is None:
        permutation = get_constrained_permutation()
    shape = grid.shape
    grid.shape = [9, 9]
    new_grid = np.zeros([9, 9], np.int8)
    for i in range(9):
        new_grid[:, i] = grid[:, permutation[i]]
    grid.shape = shape
    new_grid.shape = shape
    return new_grid


def permute_numbers(grid, permutation=None):
    if permutation is None:
        permutation = get_permutation()
    shape = grid.shape
    grid.shape = [9**2]
    new_grid = np.zeros([9**2], np.int8)
    # Zero indicates a blank spot, it should always map to itself.
    # Other numbers are also offset by 1, so this also allows for the index to match
    permutation = np.append(np.array([0]), permutation + 1)
    for i in range(9**2):
        new_grid[i] = permutation[grid[i]]
    grid.shape = shape
    new_grid.shape = shape
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

        puzzle.shape = [9**2]
        solution.shape = [9**2]

        puzzle_batch.append(puzzle)
        solution_batch.append(solution)

    return np.array(puzzle_batch), np.array(solution_batch)
