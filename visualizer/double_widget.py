from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from mainwidget import *
from PyQt6.QtGui import *

class DoubleWidget(QWidget):
    def __init__(self, start_board, goal_board, parent=None):
        super().__init__(parent)
        self.is_focus = False
        self.start_board = start_board
        self.goal_board = goal_board
        layout = QHBoxLayout(self)
        layout.addWidget(start_board)
        layout.addWidget(goal_board)
        self.setLayout(layout)
        self.setMinimumSize(0, 0)
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
        # self.setMaximumSize(600,600)

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




