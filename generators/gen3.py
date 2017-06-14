import os

import random

from generators import permuter


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


def get_random_puzzle():
    index = random.randrange(len(all_puzzles))
    puzzle = all_puzzles[index]
    return puzzle


def get_permuted_puzzle():
    puzzle = get_random_puzzle()
    return permuter.permute(puzzle)


def get_random_solution():
    index = random.randrange(len(all_solutions))
    solution = all_solutions[index]
    return solution


def get_permuted_solution():
    solution = get_random_solution()
    return permuter.permute(solution)


def get_permuted_pair():
    puzzle, solution = get_random_pair()
    return permuter.permute_pair(puzzle, solution)


def get_random_pair():
    index = random.randrange(len(all_puzzles))
    puzzle = all_puzzles[index]
    solution = all_solutions[index]
    return puzzle, solution


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
