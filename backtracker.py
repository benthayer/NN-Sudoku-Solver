import random
from game_board import BoardUtils, Board
import copy
from datetime import datetime, timedelta


class Backtracker:
    def __init__(self, dims=(3, 3)):
        # TODO generalize this to a n x n
        # TODO change from strings to
        # TODO move this into the game class
        # TODO add to the game class to support changing

        self.board_utils = BoardUtils(dims)

        self.dims = dims
        self.size = dims[0] * dims[1]

    def gen_pair(self, max_time=None, display_time=False):
        raise NotImplementedError
        self.generate(self)
        while True:
            pass
            # remove random one
            # search
            # if search is false, remove
            # modify search to produce a list of posible solutions

    def generate(self, max_time=None, display_time=False):
        # TODO Change this empty board to an instance of Board in
        board = [set(range(self.size)) for _ in range(self.size ** 2)]
        return self.search(board, start_time=None, max_time=max_time, display_time=display_time)

    def search(self, board, start_time=None, max_time=None, display_time=False):
        """
        
        Args:
            board: The game board to search on
            start_time: The start time of the game, to be used with 
            max_time:
            display_time:

        Returns:

        """
        if not start_time:
            start_time = datetime.now()
        time = datetime.now() - start_time
        if display_time:
            print(time)
        if max_time and time > max_time:
            raise TimeoutError

        board = self.board_utils.reduce_puzzle(board)
        if board is False:
            return False
        if all(len(board[box]) == 1 for box in self.board_utils.boxes):
            return board
        # all the boxes with more than 1 entry i.e. that still have notes
        reduction_boxes = [box for box in self.board_utils.boxes if len(board[box]) > 1]
        # we want to pick the box with the fewest possibilities, but randomize which one
        box = sorted(reduction_boxes, key=lambda box: float(len(board[box])) + random.random())[0]
        digits = list(board[box])
        random.shuffle(digits)
        for digit in digits:
            new_board = copy.deepcopy(board)
            new_board[box] = {digit}
            attempt = self.search(new_board, start_time, max_time, display_time)
            if type(attempt) is list:
                return attempt

        return False
