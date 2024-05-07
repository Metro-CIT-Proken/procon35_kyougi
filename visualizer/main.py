import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import json
import numpy as np

CELL_SIZE = 50
TEXT_LOCATION = 25
GAP = 100
FIRST = 100



class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setGeometry(300, 50, 1000, 1000)
        with open('./problem.json') as f:
            self.problem = json.load(f)
        with open('./answer.json') as f:
            self.answer = json.load(f)

        self.b_wid = self.problem['board']['width']
        self.b_hei = self.problem['board']['height']
        self.start_board =  [[ int(self.problem['board']['start'][y][x]) for x in range(self.b_wid)]for y in range(self.b_hei)]#スタート盤面
        self.goal_board = [[ int(self.problem['board']['goal'][y][x]) for x in range(self.b_wid)]for y in range(self.b_hei)]#完成盤面
        self.idx = 0
        self.next = self.b_wid*CELL_SIZE+100
        self.opTimerCallback
        self.start_play
        self.button_push
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.opTimerCallback)
        self.op_idx = 0#何番目手か









    def paintEvent(self, event):
        button = QPushButton("button",self)
        painter = QPainter(self)
        layout = QVBoxLayout()
        self.setLayout(layout)
        painter.setPen(QColor("black"))
        painter.setBrush(QColor("white"))

        for i in range(0,self.b_hei):
            for j in range(0,self.b_wid):
                point = QPoint(j* CELL_SIZE+TEXT_LOCATION+FIRST,i*CELL_SIZE+TEXT_LOCATION+FIRST)
                rect = QRect(j*CELL_SIZE+FIRST,i*CELL_SIZE+FIRST,CELL_SIZE,CELL_SIZE)
                painter.drawRect(rect)
                painter.drawText(point,str(self.start_board[i][j]))


        for i in range(0,self.b_hei):
            for j in range(0,self.b_wid):

                point = QPoint(j* CELL_SIZE+TEXT_LOCATION+self.next+FIRST,i*CELL_SIZE+TEXT_LOCATION+FIRST)
                rect = QRect(j*CELL_SIZE+self.next+FIRST,i*CELL_SIZE+FIRST,CELL_SIZE,CELL_SIZE)
                painter.drawRect(rect)
                painter.drawText(point,str(self.goal_board[i][j]))
        button.clicked.connect(self.start_play)
        button.setFixedSize(100, 50)
        layout.addWidget(button)



    def opTimerCallback(self):
        self.applyOn(self.op_idx+1)
        if self.op_idx == self.answer["n"]:
            self.timer.stop()

    def applyOn(self,idx):
        #手を
        if idx > self.op_idx:#未来を指定した場合
            for i in range(0,idx-self.op_idx):
                self.apply_forward()
        else:#過去を指定した場合
            for i in range(0,self.op_idx-idx):
                self.apply_backward()
        self.op_idx == idx
        self.update()

    def apply_forward(self):
        x = self.answer["ops"][self.op_idx]["x"]
        y = self.answer["ops"][self.op_idx]["y"]
        s = self.answer["ops"][self.op_idx]["s"]

        board = self.start_board

        if s == 0:
            for i in range(y,len(self.start_board)-1):
                self.start_board[i][x],self.start_board[i+1][x] = self.start_board[i+1][x],self.start_board[i][x]#上方向にずらす
        elif s == 1:
            for i in range(y,0,-1):
                self.start_board[i][x],self.start_board[i-1][x] = self.start_board[i-1][x],self.start_board[i][x]#下方向にずらす
        elif s == 2:
            for i in range(x,len(self.start_board[0])-1):
                self.start_board[y][i],self.start_board[y][i+1] = self.start_board[y][i+1],self.start_board[y][i]#左方向にずらす
        else:
            for i in range(x,0,-1):
                self.start_board[y][i],self.start_board[y][i-1] = self.start_board[y][i-1],self.start_board[y][i]#右方向にずらす
        self.op_idx += 1











    def apply_backward(self):
        x = self.answer["ops"][self.op_idx]["x"]
        y = self.answer["ops"][self.op_idx]["y"]
        s = self.answer["ops"][self.op_idx]["s"]
        board_x_size = len(self.start_board[0])#ボードの横の大きさ
        board_y_size = len(self.start_board)#ボードの縦の大きさ
        if s == 0:
            for i in range(board_y_size-1,y+1,-1):
                self.start_board[i-1][x],self.start_board[i][x] = self.start_board[i][x],self.start_board[i-1][x]
        elif s == 1:
            for i in range(0,y-1,1):
                self.start_board[i][x],self.start_board[i+1][x] = self.start_board[i+1][x],self.start_board[i][x]

        elif s == 2:
            for i in range(board_x_size-1,x+1,-1):
                self.start_board[y][i],self.start_board[y][i-1] = self.start_board[y][i-1],self.start_board[y][i]

        else:
            for i in range(0,x-1,1):
                self.start_board[y][i],self.start_board[y][i+1] = self.start_board[y][i+1],self.start_board[y][i]
        self.op_idx -= 1

    def start_play(self):
        #qTimerを作る
        self.timer.start()

    def button_push(self):
        print("button pushed!")















def main():
    app = QApplication(sys.argv)
    w = Widget()
    w.start_play()
    w.show()
    w.raise_()
    app.exec()



if __name__ == '__main__':
    main()
