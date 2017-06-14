import unittest

from sudokulib.grid import StringGrid, InvalidGrid
from sudokulib.solver import SudokuSolver

from generators import permuter, gen3
import backtracker


class TestPermuter(unittest.TestCase):
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

    def solve_pair(self, puzzle, solution):
        puzzle_str = gen3.array_to_str(puzzle)
        solver = SudokuSolver(puzzle_str, grid_class=StringGrid)
        solver.run()
        computed_solution = str(solver.grid.layer)
        solution_str = gen3.array_to_str(solution)
        self.assertEqual(computed_solution, solution_str)

    def test_permuted_row_pair(self):
        # Make sure a pair that has been permuted still corresponds to the correct answer
        puzzle, solution = gen3.get_random_pair()
        permutation = permuter.get_constrained_permutation()
        puzzle = permuter.permute_rows(puzzle, permutation)
        solution = permuter.permute_rows(solution, permutation)

        self.solve_pair(puzzle, solution)

    def test_permuted_column_pair(self):
        # Make sure a pair that has been permuted still corresponds to the correct answer
        puzzle, solution = gen3.get_random_pair()
        permutation = permuter.get_constrained_permutation()
        puzzle = permuter.permute_columns(puzzle, permutation)
        solution = permuter.permute_columns(solution, permutation)

        self.solve_pair(puzzle, solution)

    def test_permuted_number_pair(self):
        # Make sure a pair that has been permuted still corresponds to the correct answer
        puzzle, solution = gen3.get_random_pair()
        permutation = permuter.get_number_permutation()
        puzzle = permuter.permute_numbers(puzzle, permutation)
        solution = permuter.permute_numbers(solution, permutation)

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
            rows.add(tuple(puzzle[i*9: i*9 + 9]))
        permuted_puzzle = permuter.permute_rows(puzzle)

        for i in range(9):
            row = tuple(permuted_puzzle[i*9: i*9 + 9])
            self.assertIn(row, rows)
            rows.difference_update({row})

    def test_columns(self):
        # Make sure you can find all the columns in a permutation of the original
        puzzle = gen3.get_random_puzzle()
        cols = set()

        for i in range(9):
            cols.add(tuple(puzzle[i:8*9 + i:9]))
        permuted_puzzle = permuter.permute_columns(puzzle)

        for i in range(9):
            col = tuple(permuted_puzzle[i:8*9 + i:9])
            self.assertIn(col, cols)
            cols.difference_update({col})

    def test_numbers(self):
        # Make sure all numbers are mapped correctly
        puzzle = gen3.get_random_puzzle()
        permutation = permuter.get_number_permutation()
        permuted_puzzle = permuter.permute_numbers(puzzle, permutation)
        for i in range(81):
            num = puzzle[i]
            if num == -1:
                self.assertEqual(permuted_puzzle[i], -1)
            else:
                self.assertEqual(permuted_puzzle[i], permutation[num])

    def test_constrained_permutation(self):
        # TODO Test permute_rows and permute_columns with a 2x3
        # TODO is_legal function would be useful
        dims = (2, 3)
        solver = backtracker.Backtracker(dims)
        size = dims[0] * dims[1]
        puzzle = [set(range(size)) for _ in range(size ** 2)]
        solution = solver.search(puzzle)
        permuter.permute_columns(solution, dims=dims)
        pass
