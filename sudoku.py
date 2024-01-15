import numpy as np

easy1 = np.array([
    [0, 0, 9, 0, 0, 0, 1, 0, 0],
    [2, 1, 7, 0, 0, 0, 3, 6, 8],
    [0, 0, 0, 2, 0, 7, 0, 0, 0],
    [0, 6, 4, 1, 0, 3, 5, 8, 0],
    [0, 7, 0, 0, 0, 0, 0, 3, 0],
    [1, 5, 0, 4, 2, 8, 0, 7, 9],
    [0, 0, 0, 5, 8, 9, 0, 0, 0],
    [4, 8, 5, 0, 0, 0, 2, 9, 3],
    [0, 0, 6, 3, 0, 2, 8, 0, 0]
])

easy2 = np.array([
    [2, 9, 0, 7, 0, 1, 0, 0, 0],
    [5, 3, 0, 0, 6, 0, 1, 0, 0],
    [0, 0, 6, 3, 0, 0, 0, 4, 0],
    [0, 0, 0, 5, 9, 0, 0, 0, 4],
    [0, 1, 5, 0, 0, 4, 6, 8, 9],
    [0, 0, 0, 1, 8, 0, 0, 0, 3],
    [0, 0, 2, 6, 0, 0, 0, 9, 0],
    [3, 6, 0, 0, 4, 0, 7, 0, 0],
    [9, 4, 0, 8, 0, 5, 0, 0, 0]
])

medium1 = np.array([
    [0, 1, 0, 5, 0, 6, 0, 2, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 9, 1, 0, 4, 5, 0, 0],
    [0, 9, 0, 0, 1, 0, 0, 4, 0],
    [0, 7, 0, 3, 0, 2, 0, 5, 0],
    [0, 3, 0, 0, 8, 0, 0, 6, 0],
    [0, 0, 3, 2, 0, 7, 1, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 5, 0, 6, 0, 1, 0, 8, 0]
])

medium2 = np.array([
    [0, 0, 1, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 4, 7, 5, 0],
    [0, 6, 0, 0, 5, 0, 0, 0, 0],
    [8, 0, 6, 0, 0, 2, 3, 4, 9],
    [0, 0, 9, 0, 0, 0, 0, 0, 0],
    [3, 0, 4, 0, 0, 8, 1, 7, 2],
    [0, 3, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 8, 0, 1, 5, 6, 0],
    [0, 0, 2, 0, 3, 0, 0, 0, 0]
])

class Sudoku:
    def __init__(self, n_board=1, difficulty="", board="") -> None:
        if difficulty == 'easy':
            self.board = easy1 if n_board == 1 else easy2
        elif difficulty == 'medium':
            self.board = medium1 if n_board == 1 else medium2
        elif difficulty == 'hard':
            self.board = medium1 if n_board == 1 else medium2

        if board:
            self.board = np.array(board)

    def size_validator(self):
        """
        Validate a 9x9 board
        """
        return len(self.board) == 9 and all(len(fila) == 9 for fila in self.board)

    def rows_validate(self):
        return np.all(np.apply_along_axis(lambda x: np.unique(x[x != 0]).size == np.count_nonzero(x[x != 0]), axis=1, arr=self.board))

    def column_validate(self):
        return np.all(np.apply_along_axis(lambda x: np.unique(x[x != 0]).size == np.count_nonzero(x[x != 0]), axis=0, arr=self.board))

    def validate_cells(self):
        return np.all(np.array([np.unique(self.board[i:i+3, j:j+3][self.board[i:i+3, j:j+3] != 0]).size == np.count_nonzero(self.board[i:i+3, j:j+3][self.board[i:i+3, j:j+3] != 0]) for i in range(0, 9, 3) for j in range(0, 9, 3)]))
