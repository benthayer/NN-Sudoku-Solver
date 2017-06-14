import unittest

from game_board import BoardUtils


class TestBoardUtils(unittest.TestCase):
    def setUp(self):
        self.utils3x3 = BoardUtils()
        self.utils4x3 = BoardUtils((4, 3))

    def test_cross(self):
        self.assertEqual(list(range(81)), self.utils3x3.cross(list(range(9)), list(range(9))))

    def test_boxes(self):
        self.assertEqual(list(range(81)), self.utils3x3.boxes)

    def test_row_sets(self):
        self.assertEqual(self.utils3x3.row_sets, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        self.assertEqual(self.utils4x3.row_sets, [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])

    def test_col_sets(self):
        self.assertEqual(self.utils3x3.col_sets, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        self.assertEqual(self.utils4x3.col_sets, [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])

    def test_row_units(self):
        units = []
        for row in range(9):
            unit = []
            for col in range(9):
                unit.append(9*row+col)
            units.append(unit)
        self.assertEqual(self.utils3x3.row_units, units)

    def test_col_units(self):
        units = []
        for col in range(9):
            unit = []
            for row in range(9):
                unit.append(row*9 + col)
            units.append(unit)
        self.assertEqual(self.utils3x3.column_units, units)

    def test_square_units(self):
        units = []
        for big_row in range(3):
            for big_col in range(3):
                unit = []
                for row in range(3):
                    for col in range(3):
                        unit.append(big_row*27 + big_col*3 + row*9 + col)
                units.append(unit)
        self.assertEqual(self.utils3x3.square_units, units)

    def test_units(self):
        units = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 9, 18, 27, 36, 45, 54, 63, 72], [0, 1, 2, 9, 10, 11, 18, 19, 20]]
        self.assertEqual(self.utils3x3.units[0], units)

    def test_peers(self):
        peers = set([1, 2, 3, 4, 5, 6, 7, 8] + [9, 18, 27, 36, 45, 54, 63, 72] + [1, 2, 9, 10, 11, 18, 19, 20])
        self.assertEqual(self.utils3x3.peers[0], peers)

    def test_eliminate(self):
        puzzle = [0]+[-1]*80
        puzzle = [set(range(9)) if x is -1 else {x} for x in puzzle]
        new_puzzle = self.utils3x3.eliminate(puzzle)
        # 0 should be eliminated from 20 sets, 8 each from row, col, square and -4 for overlap
        new_notes = set(range(1, 9))  # 1 through 8
        self.assertEqual(new_puzzle.count(new_notes), 20)

        new_puzzle = self.utils3x3.eliminate(puzzle)
        self.assertEqual(new_puzzle.count(new_notes), 20)

    def test_reduce(self):
        """This is an easy puzzle generated through an app. Reduce should be
        able to solve this completely."""
        puzzle = [1, 4, 3, 0, 9, 0, 8, 7, 2,
                  2, 8, 9, 1, 0, 3, 5, 4, 6,
                  5, 7, 6, 8, 4, 2, 9, 3, 1,
                  0, 3, 0, 7, 0, 9, 0, 1, 0,
                  0, 0, 2, 4, 0, 8, 3, 0, 0,
                  0, 1, 0, 2, 0, 5, 0, 6, 0,
                  3, 2, 8, 6, 5, 4, 1, 9, 7,
                  6, 5, 7, 9, 0, 1, 4, 2, 3,
                  4, 9, 1, 0, 2, 0, 6, 8, 5]
        solution = [1, 4, 3, 5, 9, 6, 8, 7, 2,
                    2, 8, 9, 1, 7, 3, 5, 4, 6,
                    5, 7, 6, 8, 4, 2, 9, 3, 1,
                    8, 3, 5, 7, 6, 9, 2, 1, 4,
                    7, 6, 2, 4, 1, 8, 3, 5, 9,
                    9, 1, 4, 2, 3, 5, 7, 6, 8,
                    3, 2, 8, 6, 5, 4, 1, 9, 7,
                    6, 5, 7, 9, 8, 1, 4, 2, 3,
                    4, 9, 1, 3, 2, 7, 6, 8, 5]

        puzzle = [set(range(9)) if x is 0 else {x - 1} for x in puzzle]
        new_puzzle = self.utils3x3.reduce_puzzle(puzzle)
        new_puzzle = [x.pop() + 1 for x in new_puzzle]
        self.assertEqual(new_puzzle, solution)

    def test_reduce2(self):
        """This puzzle is intentionally incorrect. I took the solution from the previous test
        and replaced the top left corner with a 9 and removed conflicting instances of 9s such
        that unsolved, the board has no conflicts, but when trying to fill a blank, it is
        immediately apparent that there is no solution and reduce returns False"""
        puzzle = [9, 4, 3, 5, 0, 6, 8, 7, 2,
                  2, 8, 0, 1, 7, 3, 5, 4, 6,
                  5, 7, 6, 8, 4, 2, 9, 3, 1,
                  8, 3, 5, 7, 6, 9, 2, 1, 4,
                  7, 6, 2, 4, 1, 8, 3, 5, 9,
                  0, 1, 4, 2, 3, 5, 7, 6, 8,
                  3, 2, 8, 6, 5, 4, 1, 9, 7,
                  6, 5, 7, 9, 8, 1, 4, 2, 3,
                  4, 9, 1, 3, 2, 7, 6, 8, 5]
        # Convert the board to a computer-friendly format
        puzzle = [set(range(9)) if x is 0 else {x - 1} for x in puzzle]

        new_puzzle = self.utils3x3.reduce_puzzle(puzzle)
        self.assertFalse(new_puzzle)


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.utils = BoardUtils()
    # TODO copy
    # TODO history or something

# TODO Add tests to make sure the certain functions don't take too long
# TODO Try to generate a 4x4 game of sudoku
