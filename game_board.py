import numpy as np


class GameBoard:
    def __init__(self, board: np.ndarray, solution: np.ndarray, board_size=4):
        self.board = board.flatten()
        self.solution = solution.flatten()
        self.filled_spaces = board.reshape([board_size, board_size, board_size]).sum(2)
        self.board_size = board_size

        self.row = np.zeros(board_size)
        self.col = np.zeros(board_size)
        self.num = np.zeros(board_size)
        self.box = np.zeros(board_size)

        self.row[0] = 1
        self.col[0] = 1
        self.num[0] = 1
        self.box[0] = 1

        self.row_set = np.zeros(board_size)
        self.col_set = np.zeros(board_size)
        self.box_set = np.zeros(board_size)

        self.update_sets()

    def sub_size(self):
        return int(self.board_size ** 0.5)

    def get_vec(self):
        vec = np.append(self.board, [self.row, self.col, self.num, self.box,
                                     self.row_set, self.col_set, self.box_set])
        vec.shape = [1, self.board_size**3 + self.board_size*4]
        return vec
    
    def get_row(self):
        return np.argmax(self.row, 0)
    
    def get_col(self):
        return np.argmax(self.col, 0)
    
    def get_num(self):
        return np.argmax(self.num, 0)

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
        n = self.board_size
        box = self.get_box()
        col = box % n
        row = box // n
        board = self.board.reshape([n]*3)
        cells = board[row*n:(row+1)*n, col*n:(col+1)*n].reshape([n]*2)
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

    def select_row(self, row):
        self.row = np.zeros(self.board_size)
        self.row[row] = 1

        col = np.argmax(self.col, 0)
        self.select_box(row, col)

        self.update_row_set()
    
    def select_col(self, col):
        self.col = np.zeros(self.board_size)
        self.col[col] = 1

        row = np.argmax(self.row, 0)
        self.select_box(row, col)

        self.update_col_set()
    
    def select_num(self, num):
        self.num = np.zeros(self.board_size)
        self.num[num] = 1

    def get_selected(self):
        return self.get_row() * self.board_size**2 + self.get_col() * self.board_size + self.get_num()
    
    def commit(self):
        # If the space already has a value, don't change it
        if self.filled_spaces[self.get_row()][self.get_col()] == 1:
            return -0.05, False

        self.filled_spaces[self.get_row()][self.get_col()] = 1
        self.board[self.get_selected()] = 1

        if self.solution[self.get_selected()] == 1:
            return 1.0, False
        else:
            return 0.2, True
    
    def play_move(self, move_id):
        move_type = move_id // self.board_size
        move_val = move_id % self.board_size

        reward = -0.05
        done = False

        if move_type == 0:
            self.select_row(move_val)
        elif move_type == 1:
            self.select_col(move_val)
        elif move_type == 2:
            self.select_num(move_val)
        elif move_type == 3:
            reward, done = self.commit()
        done |= (self.board == self.solution).all()
        return reward, done

    def step(self, move_id):
        reward, done = self.play_move(move_id)
        observation = self.get_vec()
        return observation, reward, done, None
