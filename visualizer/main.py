import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import json
import time

CELL_SIZE = 50
TEXT_LOCATION = 25
NEXT = 300
FIRST = 100



class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setGeometry(300, 50, 700, 700)
        with open('./mondai.json') as f:
            d = json.load(f)
        self.b_wid = d['board']['width']
        self.b_hei = d['board']['height']
        self.start_board = d['board']['start']
        self.goal_board= d['board']['goal']





    def paintEvent(self, event):
        print(self.start_board)
        painter = QPainter(self)
        painter.setPen(QColor("black"))
        painter.setBrush(QColor("white"))
        painter.drawText()
        for i in range(0,self.b_hei):
            for j in range(0,self.b_wid):
                point = QPoint(i* CELL_SIZE+TEXT_LOCATION+FIRST,j*CELL_SIZE+TEXT_LOCATION+FIRST)
                rect = QRect(i*CELL_SIZE+FIRST,j*CELL_SIZE+FIRST,CELL_SIZE,CELL_SIZE)
                painter.drawRect(rect)
                painter.drawText(point,str(self.start_board[j][i]))


        for i in range(0,self.b_hei):
            for j in range(0,self.b_wid):
                point = QPoint(i* CELL_SIZE+TEXT_LOCATION+NEXT+FIRST,j*CELL_SIZE+TEXT_LOCATION+FIRST)
                rect = QRect(i*CELL_SIZE+NEXT+FIRST,j*CELL_SIZE+FIRST,CELL_SIZE,CELL_SIZE)
                painter.drawRect(rect)
                painter.drawText(point,str(self.goal_board[j][i]))
                print(i,j)










def main():
    app = QApplication(sys.argv)

    w = Widget()

    w.show()
    w.raise_()
    app.exec()


if __name__ == '__main__':
    main()
