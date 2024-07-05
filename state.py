import numpy as np
import copy

"""
NF -> Not Finished
W -> Win
L -> Lost
D -> Draw
"""

class TrisState:
    def __init__(self, initial_state=None, alpha=None, beta=None):
        if initial_state is None:
            self.__board__ = np.full((3, 3), "", dtype='<U1')  # Create a 3x3 array of empty strings
            self.__state__ = "NF"
        else:
            #if not isinstance(initial_state, np.ndarray) or initial_state.shape != (3, 3):
             #   raise Exception("Bad type or shape for initial state")
            self.__board__ = copy.deepcopy(initial_state)
            self.__update_state__()

        self.alpha = alpha if alpha is not None else -2
        self.beta = beta if beta is not None else 12

    def get_state(self):
        return copy.deepcopy(self.__state__)

    def add_move(self, player: str, row: int, col: int):
        if (not -1 < row < 3) or (not -1 < col < 3):
            raise Exception("Not valid rows or columns")
        if self.__board__[row, col] != "":
            raise Exception("Cell already used")

        if player == "max":
            self.__board__[row, col] = "O"
        elif player == "min":
            self.__board__[row, col] = "X"
        else:
            raise Exception("Invalid Player")
        self.__update_state__()

    def is_final(self):
        return self.__state__ != 'NF'

    def get_cell(self, row: int, col: int):
        if (not -1 < row < 3) or (not -1 < col < 3):
            raise Exception("Not valid rows or columns")
        return self.__board__[row, col]

    def get_board(self):
        return self.__board__

    def __update_state__(self):
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if np.all(self.__board__[i, :] == self.__board__[i, 0]) and self.__board__[i, 0] != "":
                self.__state__ = "W" if self.__board__[i, 0] == "O" else "L"
                return
            if np.all(self.__board__[:, i] == self.__board__[0, i]) and self.__board__[0, i] != "":
                self.__state__ = "W" if self.__board__[0, i] == "O" else "L"
                return

        # Check diagonals
        if np.all(self.__board__.diagonal() == self.__board__[0, 0]) and self.__board__[0, 0] != "":
            self.__state__ = "W" if self.__board__[0, 0] == "O" else "L"
            return
        if np.all(np.fliplr(self.__board__).diagonal() == self.__board__[0, 2]) and self.__board__[0, 2] != "":
            self.__state__ = "W" if self.__board__[0, 2] == "O" else "L"
            return

        # Check for a draw (no empty cells)
        if not np.any(self.__board__ == ""):
            self.__state__ = "D"
        else:
            self.__state__ = "NF"

    def __str__(self):
        board_str = '\n'.join([' '.join(cell if cell != "" else " " for cell in row) for row in self.__board__])
        return f"{board_str}\nState: {self.__state__}"

    def __eq__(self, other):
        if not isinstance(other, TrisState):
            return False
        return np.array_equal(self.__board__, other.__board__) and self.__state__ == other.__state__

    def __hash__(self):
        return hash((self.__board__.tobytes(), self.__state__))
