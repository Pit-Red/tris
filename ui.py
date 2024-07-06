import sys

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont, QCursor

from state import TrisState
from tris_tree import TrisTree


class TicTacToeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tris_tree = None
        self.widget = None
        self.buttons = None
        self.initUI()
        self.algorithm_starts = True

    def initUI(self):
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(300, 300, 300, 300)

        # Create a widget and set it as the central widget
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # Set the layout
        grid_layout = QGridLayout()
        self.widget.setLayout(grid_layout)

        self.buttons = {}
        for row in range(3):
            for col in range(3):
                button = QPushButton(' ')
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda checked, r=row, c=col: self.on_click(r, c))
                font = QFont()
                font.setPointSize(50)
                button.setFont(font)
                self.buttons[(row, col)] = button
                grid_layout.addWidget(button, row, col)

        # Reset button
        self.change_starter_button = QPushButton('Algorithm Starts')
        self.change_starter_button.setStyleSheet('background-color: #FF7F50;')
        self.change_starter_button.clicked.connect(self.change_starter)
        self.change_starter_button.setCursor(QCursor(Qt.PointingHandCursor))
        grid_layout.addWidget(self.change_starter_button, 3, 0, 1, 2)
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_game)
        self.reset_button.setCursor(QCursor(Qt.PointingHandCursor))
        grid_layout.addWidget(self.reset_button, 3, 2)

        starting_state = np.array([["O", "", ""],
                                   ["", "", ""],
                                   ["", "", ""]])

        self.tris_tree = TrisTree(initial_state=starting_state)
        self.update_board(self.tris_tree.current_state)

    def on_click(self, row, col):
        try:

            # Human move
            if self.tris_tree is None:
                state = TrisState()
                state.add_move('min', row, col)
                self.tris_tree = TrisTree(state.get_board())
                self.update_board(state)
            else:
                state = self.tris_tree.opponent_move(row, col)
                self.update_board(state)

            # Algorithm's move
            if not state.is_final():
                self.algorithm_move()
        except Exception as e:
            QMessageBox.warning(self, 'Invalid Move', str(e))

    def algorithm_move(self):
        new_state = self.tris_tree.get_best_move()
        self.update_board(new_state)

    def update_board(self, state):
        for row in range(3):
            for col in range(3):
                cell = state.get_cell(row, col)
                self.buttons[(row,col)].setText(cell if cell else '')
                if cell == 'X':
                    self.buttons[(row, col)].setStyleSheet('color:#008080;')
                if cell == 'O':
                    self.buttons[(row, col)].setStyleSheet('color:#FF7F50;')

        if state.is_final():
            result = 'Draw' if state.get_state() == 'D' else 'You Loose :P' if state.get_state() == 'W' else 'Win'
            QMessageBox.information(self, 'Game Over', f"Game Over: {result}")

    def reset_game(self):
        if self.algorithm_starts:
            initial_state = np.array([["O", "", ""],
                                      ["", "", ""],
                                      ["", "", ""]])
            self.tris_tree = TrisTree(initial_state=initial_state)
            self.update_board(self.tris_tree.current_state)  # Let the algorithm make the first move again
        else:
            initial_state = TrisState(np.array([["", "", ""],
                                                ["", "", ""],
                                                ["", "", ""]]))
            self.tris_tree = None
            self.update_board(initial_state)

    def change_starter(self):
        self.algorithm_starts = not self.algorithm_starts
        if self.algorithm_starts:
            self.change_starter_button.setStyleSheet('background-color: #FF7F50')
            self.change_starter_button.setText('Algorithm Starts')
        else:
            self.change_starter_button.setStyleSheet('background-color: #008080')
            self.change_starter_button.setText('You Start')
        self.reset_game()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TicTacToeGame()
    ex.show()
    sys.exit(app.exec_())
