import numpy as np


class GameBoard:
    def __init__(self, board: np.ndarray, solution: np.ndarray, board_size=4):
        self.board = board.flatten()
        self.solution = solution.flatten()
        self.filled_spaces = board.reshape([board_size, board_size, board_size]).sum(2)
        self.board_size = board_size

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
            return -1.0
        else:
            self.filled_spaces[self.get_row()][self.get_col()] = 1
            self.board[num_index] = 1
            self.spaces_left -= 1
            self.select_next_open()
            return 1.0

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

        reward = -0.5

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
