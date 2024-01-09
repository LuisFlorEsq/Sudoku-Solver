tablero = [
    ["5", "3", "0", "0", "7", "0", "0", "0", "0"],
    ["6", "0", "0", "1", "9", "5", "0", "0", "0"],
    ["0", "9", "8", "0", "0", "0", "0", "6", "0"],
    ["8", "0", "0", "0", "6", "0", "0", "0", "3"],
    ["4", "0", "0", "8", "0", "3", "0", "0", "1"],
    ["7", "0", "0", "0", "2", "0", "0", "0", "6"],
    ["0", "6", "0", "0", "0", "0", "2", "8", "0"],
    ["0", "0", "0", "4", "1", "9", "0", "0", "5"],
    ["0", "0", "0", "0", "8", "0", "0", "7", "9"]
]
[['5', '3', 0, 0, '7', 0, 0, 0, 0], 
 ['6', '4', 0, '1', '9', '5', 0, 0, 0],
 [0, '9', '8', 0, 0, 0, 0, '6', 0], 
 ['8', 0, 0, 0, '6', 0, 0, 0, '3'], 
 ['4', 0, 0, '8', 0, '3', 0, 0, '1'], 
 ['7', 0, 0, 0, '2', 0, 0, 0, '6'], 
 [0, '6', 0, 0, 0, 0, '2', '8', 0], 
 [0, 0, 0, '4', '1', '9', 0, 0, '5'],
  [0, 0, 0, 0, '8', 0, 0, '7', '9']]

class Sudoku:
    def __init__(self, difficulty="", board="") -> None:
        if difficulty == 'easy':
            self.board = tablero
        elif difficulty == 'medium':
            self.board = tablero
        elif difficulty == 'hard':
            self.board = tablero

        if board:
            print(f'ASDASDASDAS: {board}')
            self.board = board
        self.invert_list = list()

    def size_validator(self):
        """
        Validate a 9x9 board
        """
        return len(self.board) == 9 and all(len(fila) == 9 for fila in self.board)

    def rows_validate(self, lista='tablero_general'):
        if lista == 'tablero_general':
            lista = self.board

        return all(
            fila.count(elemento) == 1 if (elemento != '0' and elemento != 0) else True
            for fila in lista
            for elemento in fila
        )

    def column_validate(self):
        for column in range(0, 9):
            column_values = [self.board[row][column] for row in range(0, 9)]
            if not self.rows_validate([column_values]):
                return False
        return True

    def validate_cells(self):
        return (
            self.validate_3_cells(0, 3)
            and self.validate_3_cells(3, 6)
            and self.validate_3_cells(6, 9)
        )

    def validate_3_cells(self, range1, range2):
        for column in range(0, 9):
            if column == 3 or column == 6:
                self.invert_list.clear()
            for row in range(range1, range2):
                self.invert_list.append(self.board[row][column])
                if len(self.invert_list) == 9 and not self.rows_validate([self.invert_list]):
                    return False
        return True