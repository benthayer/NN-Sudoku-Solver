import unittest

from sudokulib.grid import StringGrid, InvalidGrid
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

    def test_permutations_valid(self):
        # Make sure permuted solutions are valid boards
        for _ in range(10):
            solution = gen3.get_permuted_solution()
            solution = gen3.array_to_str(solution)
            grid = StringGrid(solution)
            try:
                self.assertTrue(grid.validate())
            except InvalidGrid:
                self.fail()

    def test_permuted_row_pair(self):
        # Make sure a pair that has been permuted still corresponds to the correct answer
        puzzle, solution = gen3.get_random_pair()
        permutation = gen3.get_constrained_permutation()
        puzzle = gen3.permute_rows(puzzle, permutation)
        solution = gen3.permute_rows(solution, permutation)

        self.solve_pair(puzzle, solution)

    def test_permuted_column_pair(self):
        # Make sure a pair that has been permuted still corresponds to the correct answer
        puzzle, solution = gen3.get_random_pair()
        permutation = gen3.get_constrained_permutation()
        puzzle = gen3.permute_columns(puzzle, permutation)
        solution = gen3.permute_columns(solution, permutation)

        self.solve_pair(puzzle, solution)

    def test_permuted_number_pair(self):
        # Make sure a pair that has been permuted still corresponds to the correct answer
        puzzle, solution = gen3.get_random_pair()
        permutation = gen3.get_permutation()
        puzzle = gen3.permute_numbers(puzzle, permutation)
        solution = gen3.permute_numbers(solution, permutation)

        self.solve_pair(puzzle, solution)

    def test_permuted_pair(self):
        # Make sure a pair that has been permuted still corresponds to the correct answer
        puzzle, solution = gen3.get_permuted_pair()

        self.solve_pair(puzzle, solution)

    def test_rows(self):
        # Make sure you can find all the rows in a permutation of the original
        puzzle = gen3.get_random_puzzle()
        rows = set()

        for i in range(9):
            rows.add(tuple(puzzle[i*9:i*9+9]))
        permuted_puzzle = gen3.permute_rows(puzzle)

        for i in range(9):
            row = tuple(permuted_puzzle[i*9:i*9+9])
            self.assertIn(row, rows)
            rows.difference_update({row})

    def test_columns(self):
        # Make sure you can find all the columns in a permutation of the original
        puzzle = gen3.get_random_puzzle()
        cols = set()

        for i in range(9):
            cols.add(tuple(puzzle[i:8*9+i:9]))
        permuted_puzzle = gen3.permute_columns(puzzle)

        for i in range(9):
            col = tuple(permuted_puzzle[i:8*9+i:9])
            self.assertIn(col, cols)
            cols.difference_update({col})

    def test_numbers(self):
        # Make sure all numbers are mapped correctly
        puzzle = gen3.get_random_puzzle()
        permutation = gen3.get_permutation()
        permuted_puzzle = gen3.permute_numbers(puzzle, permutation)
        for i in range(81):
            num = puzzle[i]
            if num == -1:
                self.assertEqual(permuted_puzzle[i], -1)
            else:
                self.assertEqual(permuted_puzzle[i], permutation[num])
