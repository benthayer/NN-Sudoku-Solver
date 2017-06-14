import numpy as np

# TODO Change this to be generic so all the parameters can be changed
# Instead of changing this code every time I have a new idea, I want to be able
# to change the thing that I call.

# Example splits RLBoard, RecorderBoard, SelectionBoard


class BoardUtils:
    """This class is used for things that are useful in the manipulation of a board
    and are similar between instances of boards and agents. This is done so that each
    time a new board or agent is constructed, the processing power doesn't need to be used."""

    # Preconstructed instances to save computing time
    instances = {}

    @staticmethod
    def cross(rows, cols, size=9):
        """Index of element that is in (row, col) for all (row, col) in (rows, cols)"""
        return [row*size + col for row in rows for col in cols]

    @staticmethod
    def get_utils(dims=(3, 3)):
        """Get a preconstructed utils class"""
        if dims not in BoardUtils.instances:
            BoardUtils.instances[dims] = BoardUtils(dims)
        return BoardUtils.instances[dims]

    @staticmethod
    def print_board(board):
        print('  0  1  2  3  4  5  6  7  8')
        for i in range(9):
            print(i, board[9*i:9*i+9])

    def __init__(self, dims=(3, 3)):
        self.rows = dims[0]
        self.cols = dims[1]
        # The number of classes
        self.size = self.rows * self.cols
        # All the classes
        self.numbers = list(range(1, self.size+1))
        # Ids for each row and column
        self.row_ids = list(range(self.size))
        self.col_ids = list(range(self.size))

        # Every single box there is, should be range(81) for 3x3 board
        self.boxes = self.cross(self.row_ids, self.col_ids, size=self.size)

        # Row and column units
        self.row_units = [self.cross([r], self.col_ids, size=self.size) for r in self.row_ids]
        self.column_units = [self.cross(self.row_ids, [c], size=self.size) for c in self.col_ids]

        # sets are how the rows and cols are divided up, like [[0, 1, 2], [3, 4, 5], [6, 7, 8]] for 3x3
        # these sets are crossed to create the square units
        self.row_sets = [[self.row_ids[r * self.cols + c] for c in range(self.cols)] for r in range(self.rows)]
        self.col_sets = [[self.col_ids[c * self.rows + r] for r in range(self.rows)] for c in range(self.cols)]
        self.square_units = [self.cross(rs, cs, size=self.size) for rs in self.row_sets for cs in self.col_sets]

        # List of every single unit
        self.unit_list = self.row_units + self.column_units + self.square_units
        # List of all units for each box
        self.units = [([u for u in self.unit_list if s in u]) for s in self.boxes]
        # I can't remember what this sum does, make sure that it's right.
        # The set of all peers for every box
        self.peers = [set(sum(self.units[s], [])) - {s} for s in self.boxes]

    def find_twins(self, values, unit):
        """Returns all twins in the unit minus the twins that have already been cleared"""
        twins = []
        # find all of the twins
        for i in range(len(unit)):
            box1 = unit[i]
            if len(values[box1]) == 2:
                pair1 = values[box1]
                for j in range(i + 1, len(unit)):
                    box2 = unit[j]
                    pair2 = values[box2]
                    if pair2 == pair1:
                        twins.append(pair2)
        return twins

    def clear_unit(self, values, unit, twins):
        """Clears the unit of twin values that are not in a twin and whether any action was needed to clear it."""
        cleared = False
        for twin in twins:
            for box in unit:
                if values[box] != twin:
                    for digit in twin:
                        if digit in values[box]:
                            cleared = True
                        values[box].discard(digit)
        return values, cleared

    def propagate_twins(self, values, unit):
        twins = self.find_twins(values, unit)
        return self.clear_unit(values, unit, twins)

    def naked_twins(self, values):
        """Eliminate values using the naked twins strategy.
        Args:
            values(dict): a dictionary of the form {'box_name': '123456789', ...}
    
        Returns:
            the values dictionary with the naked twins eliminated from peers.
        """
        last_update = None
        while True:
            for unit in self.unit_list:
                if last_update == tuple(unit):
                    return values
                values, cleared = self.propagate_twins(values, unit)
                if cleared:
                    last_update = tuple(unit)
            if last_update is None:
                return values

    def only_choice(self, board):
        for unit in self.unit_list:
            for digit in self.numbers:
                dplaces = [box for box in unit if digit in board[box]]
                if len(dplaces) == 1:
                    board[dplaces[0]] = {digit}
        return board

    def eliminate(self, board):
        """Eliminates solved values from the list of constraints"""
        for box in self.boxes:
            if len(board[box]) != 1:
                continue
            # There must be only 1 left
            [digit] = board[box]
            for peer in self.peers[box]:
                board[peer].discard(digit)
                # TODO Turn this into a change method so boards can take action when replacing things
        return board

    def reduce_puzzle(self, board):
        """

        Args:
            board(Board): 

        Returns:

        """
        # TODO Follow the solver step by step to determine where this goes wrong
        # Print the solution out when looking at the steps so it's easy to determine what's going wrong

        stalled = False
        while not stalled:
            solved_values_before = len([box for box in self.boxes if len(board[box]) == 1])
            board = self.eliminate(board)
            board = self.only_choice(board)
            board = self.naked_twins(board)
            solved_values_after = len([box for box in self.boxes if len(board[box]) == 1])
            if len([box for box in self.boxes if len(board[box]) == 0]) != 0:
                return False
            stalled = solved_values_before == solved_values_after
        return board


class Board:
    # TODO subclass this to make boards that track history and return vectors
    def __init__(self, board=None, dims=(3, 3)):
        """Initializes a new board. Size must be set explicitly if not 3x3"""

        self.dims = dims
        self.size = dims[0] * dims[1]

        if type(board) is list:
            board = board.copy()
            if type(board[0]) is list:
                self._board = []
                for row in board:
                    self._board.extend(row)
            else:
                self._board = board
            for i in range(len(board)):
                if board[i] == -1:
                    board[i] = set(range(self.size))
                elif type(board[i]) is int:
                    board[i] = {board[i]}
        else:
            self._board = [set(range(self.size))] * self.size ** 2

        # Size must match the length of the board
        assert len(self._board) == self.size ** 2

    def __getitem__(self, key):
        return self._board[key]

    def __setitem__(self, key, value):
        self._board[key] = value

    def copy(self):
        return Board(self._board.copy(), self.dims)

    def puzzle(self):
        return [next(iter(x)) if len(x) == 1 else -1 for x in self._board]


class GameBoard:
    # TODO Make this work as a subclass of board, call VectorBoard
    def __init__(self, board: np.ndarray, solution: np.ndarray, board_size=4,
                 correct_reward=1, incorrect_reward=-1, skip_reward=-0.05):
        self.board = board.flatten()
        self.solution = solution.flatten()
        self.filled_spaces = board.reshape([board_size, board_size, board_size]).sum(2)
        self.board_size = board_size

        self.correct_reward = correct_reward
        self.incorrect_reward = incorrect_reward
        self.skip_reward = skip_reward

        self.spaces_left = (board_size ** 2) - self.filled_spaces.sum()
        self.step_num = 0

        self.row = np.zeros(board_size)
        self.col = np.zeros(board_size)
        self.box = np.zeros(board_size)

        self.row[0] = 0
        self.col[0] = 0
        self.box[0] = 0

        self.row_set = np.zeros(board_size)
        self.col_set = np.zeros(board_size)
        self.box_set = np.zeros(board_size)

        self.select_next_open()

    def sub_size(self):
        return int(self.board_size ** 0.5)

    def get_vec(self):
        # vec = np.append(self.board, [self.row, self.col, self.box,
        #                              self.row_set, self.col_set, self.box_set])
        # vec.shape = [1, self.board_size**3 + self.board_size*6]
        vec = np.append(self.row_set, [self.col_set, self.box_set])
        # vec = np.minimum(sum(vec), np.ones(4))
        vec.shape = [1, self.board_size*3]
        return vec
    
    def get_row(self):
        return np.argmax(self.row, 0)
    
    def get_col(self):
        return np.argmax(self.col, 0)

    def get_box(self):
        return np.argmax(self.box, 0)

    def update_row_set(self):
        row = self.get_row()
        board = self.board.reshape([self.board_size]*3)
        cols = board[row]
        self.row_set = np.sum(cols, axis=0)

    def update_col_set(self):
        col = self.get_col()
        board = self.board.reshape([self.board_size]*3)
        rows = board[:, col]
        self.col_set = np.sum(rows, axis=0)

    def update_box_set(self):
        n = self.sub_size()
        box = self.get_box()
        col = box % n
        row = box // n
        board = self.board.reshape([self.board_size]*3)
        cells = board[row*n:(row+1)*n, col*n:(col+1)*n].reshape([self.board_size]*2)
        self.box_set = cells.sum(0)

    def update_sets(self):
        self.update_row_set()
        self.update_col_set()
        self.update_box_set()

    def select_box(self, row, col):
        box = self.sub_size() * (row // self.sub_size()) + col // self.sub_size()
        self.box = np.zeros(self.board_size)
        self.box[box] = 1

        self.update_box_set()

    def select_row(self, row, select_box=True):
        self.row = np.zeros(self.board_size)
        self.row[row] = 1

        if select_box:
            col = np.argmax(self.col, 0)
            self.select_box(row, col)

        self.update_row_set()
    
    def select_col(self, col, select_box=True):
        self.col = np.zeros(self.board_size)
        self.col[col] = 1

        if select_box:
            row = np.argmax(self.row, 0)
            self.select_box(row, col)

        self.update_col_set()

    def get_index(self, num):
        return self.get_row() * self.board_size**2 + self.get_col() * self.board_size + num
    
    def commit(self, num):
        num_index = self.get_index(num)

        if self.solution[num_index] != 1:
            self.select_next_open()
            return self.incorrect_reward
        else:
            self.filled_spaces[self.get_row()][self.get_col()] = 1
            self.board[num_index] = 1
            self.spaces_left -= 1
            self.select_next_open()
            return self.correct_reward

    def select_next_open(self):
        for row in range(self.get_row(), self.get_row() + 4):
            for col in range(self.get_col(), self.get_col() + 4):
                row %= 4
                col %= 4
                if self.filled_spaces[row][col] == 0:
                    self.select_row(row, select_box=False)
                    self.select_col(col, select_box=False)
                    self.select_box(row, col)
                    return
    
    def play_move(self, move_id):

        reward = self.skip_reward

        if move_id == 4:
            self.select_next_open()
        else:
            reward = self.commit(move_id)

        # if board is complete, end game
        done = self.spaces_left == 0

        self.step_num += 1

        if self.step_num > 40:
            done = True

        return reward, done

    def step(self, move_id, display=False):
        if display:
            print("Board: {}".format(np.minimum(sum(self.get_vec().reshape([3, 4])), np.ones(4))))
            print("Move: {}".format(move_id))
        reward, done = self.play_move(move_id)

        if display:
            print("Reward: {}".format(reward))
            input("Press any key to continue")

        observation = self.get_vec()

        return observation, reward, done, None
