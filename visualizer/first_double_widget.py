from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from mainwidget import *
from PyQt6.QtGui import *
from post_answer import *

class FirstDoubleWidget(QWidget):
    def __init__(self, start_board, goal_board ,parent=None):
        super().__init__(parent)
        self.is_focus = False
        self.start_board = start_board
        self.goal_board = goal_board
        self.op_idx = 0

        board_layout = QHBoxLayout()
        # button_layout = QHBoxLayout()
        layout = QVBoxLayout(self)
        layout.addLayout(board_layout)
        # layout.addLayout(button_layout)

        board_layout.addWidget(start_board)
        board_layout.addWidget(goal_board)


        self.setLayout(layout)
        self.setMinimumSize(0, 0)
        self.setMaximumSize(1000,1000)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)






