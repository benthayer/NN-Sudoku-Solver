import unittest

from sudokulib.grid import StringGrid
from sudokulib.solver import SudokuSolver

from generators import gen3


class TestGen3(unittest.TestCase):
    def test_array_to_string(self):
        grid = [5, 3, 8, 6, 4, 2, 9, 1, 7,
                4, 5, 2, 8, 7, 3, 1, 6, 9,
                7, 8, 3, 1, 9, 4, 6, 2, 5,
                3, 6, 9, 5, 1, 8, 2, 7, 4,
                1, 7, 6, 9, 2, 5, 4, 8, 3,
                6, 2, 4, 7, 5, 9, 8, 3, 1,
                2, 4, 7, 3, 8, 1, 5, 9, 6,
                8, 9, 1, 4, 6, 7, 3, 5, 2,
                9, 1, 5, 2, 3, 6, 7, 4, 8]
        # Grid is stored with classes starting at 0
        grid = list(map(lambda x: x-1, grid))
        grid_str = '538642917452873169783194625369518274176925483624759831247381596891467352915236748'
        self.assertEqual(gen3.array_to_str(grid), grid_str)

    def test_string_to_array(self):
        grid = [5, 3, 8, 6, 4, 2, 9, 1, 7,
                4, 5, 2, 8, 7, 3, 1, 6, 9,
                7, 8, 3, 1, 9, 4, 6, 2, 5,
                3, 6, 9, 5, 1, 8, 2, 7, 4,
                1, 7, 6, 9, 2, 5, 4, 8, 3,
                6, 2, 4, 7, 5, 9, 8, 3, 1,
                2, 4, 7, 3, 8, 1, 5, 9, 6,
                8, 9, 1, 4, 6, 7, 3, 5, 2,
                9, 1, 5, 2, 3, 6, 7, 4, 8]
        # Grid is stored with classes starting at 0
        grid = list(map(lambda x: x-1, grid))
        grid_str = '538642917452873169783194625369518274176925483624759831247381596891467352915236748'
        self.assertEqual(gen3.str_to_array(grid_str), grid)

    def test_array_to_vec(self):
        grid = [5, 3, 8, 6, 4, 2, 9, 1, 7,
                4, 5, 2, 8, 7, 3, 1, 6, 9,
                7, 8, 3, 1, 9, 4, 6, 2, 5,
                3, 6, 9, 5, 1, 8, 2, 7, 4,
                1, 7, 6, 9, 2, 5, 4, 8, 3,
                6, 2, 4, 7, 5, 9, 8, 3, 1,
                2, 4, 7, 3, 8, 1, 5, 9, 6,
                8, 9, 1, 4, 6, 7, 3, 5, 2,
                9, 1, 5, 2, 3, 6, 7, 4, 8]
        # Grid is stored with classes starting at 0
        grid = list(map(lambda x: x-1, grid))

        vec = gen3.array_to_vec(grid)

        new_grid = gen3.vec_to_array(vec)

        self.assertEqual(new_grid, grid)

    def test_lengths(self):
        # Make sure the lengths of all_puzzles and all_solutions are the same and == 2365
        self.assertEqual(len(gen3.all_puzzles), len(gen3.all_solutions))
        self.assertNotEqual(len(gen3.all_puzzles), 0)

    def solve_pair(self, puzzle, solution):
        puzzle_str = gen3.array_to_str(puzzle)
        solver = SudokuSolver(puzzle_str, grid_class=StringGrid)
        solver.run()
        computed_solution = str(solver.grid.layer)
        solution_str = gen3.array_to_str(solution)
        self.assertEqual(computed_solution, solution_str)

    def test_pair(self):
        # Make sure the computed solution of a puzzle matches the given solution
        puzzle, solution = gen3.get_random_pair()

        self.solve_pair(puzzle, solution)