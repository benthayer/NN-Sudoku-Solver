import unittest

from backtracker import Backtracker
from generators.gen3 import get_permuted_pair


class TestBacktracker(unittest.TestCase):
    def setUp(self):
        self.solver = Backtracker()

    def test_3x3(self):
        puzzle, solution = get_permuted_pair()
        puzzle = [set(range(9)) if x == -1 else {x} for x in puzzle]
        solved_puzzle = self.solver.search(puzzle)
        self.assertNotEqual(solved_puzzle, False)
        solved_puzzle = list(map(lambda x: x.pop(), solved_puzzle))
        self.assertEqual(solved_puzzle, solution)
        pass

    def test_4x4(self):
        dims = (4, 4)
        # dims = (4, 5)  # 26s
        # dims = (5, 5)  # Not solved
        size = dims[0] * dims[1]
        puzzle = [set(range(size)) for _ in range(size**2)]
        solver = Backtracker(dims)
        solution = solver.search(puzzle)
        print(solution)
        pass
