from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from mainwidget import *
from PyQt6.QtGui import *
from post_answer import *

class DoubleWidget(QWidget):
    def __init__(self, start_board, goal_board, answer_json_file, config ,parent=None):
        super().__init__(parent)
        self.op_idx = 0

        # self.is_focus = False
        self.start_board = start_board
        self.goal_board = goal_board
        self.post_button = QPushButton("POST",self)
        self.post_button.clicked.connect(self.post)
        self.answer_file = answer_json_file
        self.answer_num = 0
        self.config = config
        self.effort_label = QLabel()
        self.effort_label.setFixedSize(300,20)


        board_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        layout = QVBoxLayout(self)
        layout.addWidget(self.effort_label)
        layout.addLayout(board_layout)
        layout.addLayout(button_layout)


        board_layout.addWidget(start_board)
        board_layout.addWidget(goal_board)

        button_layout.addWidget(self.post_button)

        self.setLayout(layout)
        self.setMinimumSize(0, 600)
        self.setMaximumSize(1000,1000)
        print(f"double widget size: height:{self.height()} width:{self.width()}")
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(QPen(QColor("black"), 5, Qt.PenStyle.SolidLine))  # 黒色のペンで描画

    #     # 四角形の描画 (x, y, width, height)
    #     rect = painter.drawRect(0, 0, 1000, 1000)
    #     # rect.raise_()



        # self.setMaximumHeight(start_board.size().height())
        # self.setMaximumHeight()


    # def focusInEvent(self,event):
    #     self.is_focus = True
    #     print("double focus in")
    #     print(self)
    #     super().focusInEvent(event)

    # def focusOutEvent(self,event):
    #     self.is_focus = False
    #     print("double focus out")
    #     print(self)
    #     super().focusOutEvent(event)

    def resizeGL(self,width,height):
        print(f"double widget size: height:{height} width:{width}")

    def post(self):
        Post(self.answer_file, self.config)

    def paintEvent(self, event):
        self.effort_label.setText(f"手数 {self.answer_num }現在 {self.op_idx} 手目 あと {self.answer_num-self.op_idx}")






