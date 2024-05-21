import sys

from collections import deque
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import *
import json
import numpy as np

CELL_SIZE = 50 #一辺のセルの長さ
TEXT_LOCATION = 25 #テキストとセルの端との感覚
GAP = 100 #スタートボードとゴールボードとの間隔
FIRST = 100 #GUIの端とスタートボードとの感覚



class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setWindowTitle('Test GUI')
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
        self.start_play
        self.button_push
        self.opTimerCallback
        self.timer = QTimer()
        self.timer_oth = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.opTimerCallback)
        self.op_idx = 0#何番目手か
        self.right_key_check = False
        self.color = {0:"red",1:"blue",2:"green",3:"yellow"}
        self.dict_action = {0:"上",1:"下",2:"左",3:"右"}
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.answer["n"])
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self.onSliderChange)
        layout.addWidget(self.slider)






    def paintEvent(self, event):

        # button = QPushButton("button",self)
        # button.setFixedSize(100, 50)

        if not(self.op_idx >= self.answer["n"]):
            x = self.answer["ops"][self.op_idx]["x"]
            y = self.answer["ops"][self.op_idx]["y"]
            s = self.answer["ops"][self.op_idx]["s"]


        painter = QPainter(self)
        painter.setPen(QColor("black"))
        count_point = QPoint(30,20)
        action_text_point = QPoint(30,40)
        painter.drawText(count_point,f'{self.op_idx}手目 あと {self.answer["n"]-self.op_idx}手')
        if not(self.op_idx >= self.answer["n"]):
            painter.drawText(action_text_point,f'座標: x:{x}y:{y} 次の行動: {self.dict_action[s]} にずらす' )
        painter.setBrush(QColor("white"))

        font = painter.font()
        for i in range(0,self.b_hei):
            for j in range(0,self.b_wid):

                if not(self.op_idx >= self.answer["n"]):
                    if i==y and j==x :
                        print(self.search_near_goal(i,j))
                        if self.start_board[y][x] != 0:
                            line_pen = QPen(QColor("black"),5,Qt.PenStyle.SolidLine)
                            #枠に太線をつける
                            painter.setPen(line_pen)
                            painter.drawLine(j*CELL_SIZE+FIRST,i*CELL_SIZE+FIRST,j*CELL_SIZE+FIRST,(i+1)*CELL_SIZE+FIRST)
                            painter.drawLine(j*CELL_SIZE+FIRST,i*CELL_SIZE+FIRST,(j+1)*CELL_SIZE+FIRST,i*CELL_SIZE+FIRST)
                            painter.drawLine((j+1)*CELL_SIZE+FIRST,i*CELL_SIZE+FIRST,(j+1)*CELL_SIZE+FIRST,(i+1)*CELL_SIZE+FIRST)
                            painter.drawLine(j*CELL_SIZE+FIRST,(i+1)*CELL_SIZE+FIRST,(j+1)*CELL_SIZE+FIRST,(i+1)*CELL_SIZE+FIRST)
                            #
                            #
                            painter.setPen(QColor(self.color[self.start_board[y][x]-1]))
                        else:
                            painter.setPen(QColor(self.color[3]))
                        font = painter.font()
                        font.setBold(True)
                        painter.setFont(font)

                point = QPoint(j* CELL_SIZE+TEXT_LOCATION+FIRST,i*CELL_SIZE+TEXT_LOCATION+FIRST)
                rect = QRect(j*CELL_SIZE+FIRST,i*CELL_SIZE+FIRST,CELL_SIZE,CELL_SIZE)
                rect_color = QColor(self.color[self.start_board[i][j]])
                painter.fillRect(rect,rect_color)
                #ずらす方向の矢印をつける
                if not(self.op_idx >= self.answer["n"]):
                    if (j == x and i < y) and self.dict_action[s] == "下":
                            painter.drawText(point,f'{str(self.start_board[i][j])}↓')
                    elif (j == x and i > y) and  self.dict_action[s] == "上":

                            painter.drawText(point,f'{str(self.start_board[i][j])}↑')
                    elif (i == y and j > x) and  self.dict_action[s] == "左":
                            painter.drawText(point,f'{str(self.start_board[i][j])}←')
                    elif (i == y and j < x )and  self.dict_action[s] == "右":
                            painter.drawText(point,f'{str(self.start_board[i][j])}→')
                    else:
                        painter.drawText(point,str(self.start_board[i][j]))


                    if i==y and j==x :
                            if self.start_board[y][x] != 0:
                                line_pen = QPen(QColor("black"),5,Qt.PenStyle.SolidLine)
                                painter.setPen(line_pen)
                                painter.drawLine((j+1)*CELL_SIZE+FIRST,i*CELL_SIZE+FIRST,(j+1)*CELL_SIZE+FIRST,(i+1)*CELL_SIZE+FIRST)
                                painter.drawLine(j*CELL_SIZE+FIRST,(i+1)*CELL_SIZE+FIRST,(j+1)*CELL_SIZE+FIRST,(i+1)*CELL_SIZE+FIRST)
                                painter.setPen(QColor(self.color[self.start_board[y][x]-1]))
                else:
                    painter.drawText(point,str(self.start_board[i][j]))
                painter.setPen(QColor("black"))
                font.setBold(False)
                painter.setFont(font)


        for i in range(0,self.b_hei):
            for j in range(0,self.b_wid):
                if self.goal_board[i][j] == self.start_board[i][j]:
                    rect_color = QColor("purple")
                else:
                    rect_color = QColor(self.color[self.goal_board[i][j]])
                point = QPoint(j* CELL_SIZE+TEXT_LOCATION+self.next+FIRST,i*CELL_SIZE+TEXT_LOCATION+FIRST)
                rect = QRect(j*CELL_SIZE+self.next+FIRST,i*CELL_SIZE+FIRST,CELL_SIZE,CELL_SIZE)
                painter.fillRect(rect,rect_color)
                painter.drawText(point,str(self.goal_board[i][j]))
        # button.clicked.connect(self.button_push)
        # layout.addWidget(button)

    def search_near_goal(self,x,y):
        que = deque()
        search_board = [[-1 for x in range(self.b_wid)]for y in range(self.b_hei)]
        for i in range(0,len(search_board)):
            print(search_board[i])
        search_board[y][x] = 0
        que.append((y,x))
        dy = [1,0,-1,0]
        dx = [0,-1,0,1]
        while que:
            h,w = que.popleft()
            for i in range(4):
                print(que)
                next_h = h + dy[i]
                next_w = w + dx[i]
                if 0 <= next_h < len(search_board) and 0 <= next_w < len(search_board[0]) and not(self.start_board[next_h][next_w]==self.goal_board[next_h][next_w]):
                    if search_board[next_h][next_w] == -1:
                        search_board[next_h][next_w] = search_board[h][w]+1
                        que.append((next_h,next_w))
                    if self.start_board[next_h][next_w] == self.goal_board[next_h][next_w]:
                        return search_board[next_h][next_w]
            for i in range(len(search_board)):
                print(search_board[i])






    def onSliderChange(self,value):
        self.applyOn(value)


    def keyPressEvent(self, event: QKeyEvent):
        #右キーを押すと一手進む
        if event.key() == Qt.Key.Key_Right and not(self.op_idx == self.answer["n"]):
            self.right_key_check = self.applyOn(self.op_idx+1)
            print("進む")
        #左キーに進むと一手戻る
        elif event.key() == Qt.Key.Key_Left and not(self.op_idx == 0):
            self.right_key_check = self.applyOn(self.op_idx-1)
            print("戻る")

    #0.5秒ごとに進む・戻る
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
    #一手進める
    def apply_forward(self):
        print(self.op_idx)
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


    #一手戻る
    def apply_backward(self):
        print(self.op_idx)
        x = self.answer["ops"][self.op_idx-1]["x"]
        y = self.answer["ops"][self.op_idx-1]["y"]
        s = self.answer["ops"][self.op_idx-1]["s"]
        board_x_size = len(self.start_board[0])#ボードの横の大きさ
        board_y_size = len(self.start_board)#ボードの縦の大きさ
        if s == 0:
            for i in range(board_y_size-1,y,-1):
                self.start_board[i-1][x],self.start_board[i][x] = self.start_board[i][x],self.start_board[i-1][x]
        elif s == 1:
            for i in range(0,y):
                self.start_board[i][x],self.start_board[i+1][x] = self.start_board[i+1][x],self.start_board[i][x]

        elif s == 2:
            for i in range(board_x_size-1,x,-1):
                self.start_board[y][i],self.start_board[y][i-1] = self.start_board[y][i-1],self.start_board[y][i]

        else:
            for i in range(0,x):
                self.start_board[y][i],self.start_board[y][i+1] = self.start_board[y][i+1],self.start_board[y][i]
        self.op_idx -= 1

    #タイマーを開始させる
    def start_play(self):
        #qTimerを作る
        self.timer.start()
    def button_push():
        print("pushed! button")



def main():
    app = QApplication(sys.argv)
    w = Widget()
    # w.start_play()
    w.show()
    w.raise_()
    app.exec()



if __name__ == '__main__':
    main()
