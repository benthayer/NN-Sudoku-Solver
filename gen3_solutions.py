import os

from sudokulib.grid import StringGrid
from sudokulib.solver import SudokuSolver


with open(os.path.join(os.path.dirname(__file__), 'data/puzzles.txt')) as puzzle_file,\
        open(os.path.join(os.path.dirname(__file__), 'data/solutions.txt'), 'w+') as solution_file:
    for i, puzzle in enumerate(puzzle_file):
        puzzle = puzzle.strip()
        solver = SudokuSolver(puzzle, grid_class=StringGrid)
        solver.run()
        solution = str(solver.grid.layer)
        solution_file.write(solution + '\n')
        print("Solved puzzle {}".format(i))

