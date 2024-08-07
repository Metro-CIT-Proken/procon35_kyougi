import sys

from collections import deque
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QKeyEvent,QFocusEvent
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import json
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np
from collections import deque



WIDTH = 1000
HEIGHT = 1000
CELL_SIZE = 40 #一辺のセルの長さ
TEXT_LOCATION = 25 #テキストとセルの端との感覚
GAP = 100 #スタートボードとゴールボードとの間隔
FIRST = 100 #GUIの端とスタートボードとの感覚

FIRST_CELL_POSITION = (-0.9,0.9)
FIRST_POSITION = -1


TRANSLATE_GL = WIDTH/2#qtの座標系に変換する定数

class OpenGLWidget(QOpenGLWidget):
    def __init__(self,board,goal_board,zoom,zoom_direction,xtext=None,ytext=None,parent=None):
        super().__init__(parent)
        self.board = board
        self.goal_board = goal_board
        self.zoom = zoom
        self.zoom_direction = zoom_direction
        self.setMinimumSize(100, 100)
        self.setMaximumSize(400, 400)
        self.zoomx = 0
        self.zoomy = 0
        self.xtext = xtext
        self.ytext = ytext




    def write_text(self,r,g,b,w,h,string):#,r,g,b,w,h
        img = np.zeros((132,128,3),dtype=np.uint8)
        cv2.putText(img,string, (60, 70), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255))
        img = cv2.flip(img, 0)
        img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        glRasterPos2f(w,h)
        glColor3f(0.0, 0.0, 0.0)
        target_color = (0, 0, 0)
        change_color = (r, g, b)
        img = np.where(img == target_color, change_color, (255, 255, 255))
        glDrawPixels(img.shape[1], img.shape[0], GL_RGB,GL_UNSIGNED_BYTE, img)


    def initializeGL(self):
        glClearColor(1.0,1.0,1.0,1.0)





    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 0.0, 0.0)# 色を赤に設定

        glRasterPos2f(0.0,0.0)
        width_square = len(self.board[0])
        height_square = len(self.board)
        sx = 1/width_square
        sy = 1/height_square
        first = FIRST/TRANSLATE_GL
        s = min(sx,sy)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()

        first = 0

        glTranslate(-1, -1, 0)
        glTranslate(-self.zoomx, -self.zoomy, 1)
        glScale(2/self.zoom, 2/self.zoom, 1)




        glBegin(GL_QUADS)
        for i in range(height_square):
            for j in range(width_square):

                if not(self.xtext == None or self.ytext == None):
                    if self.ytext == i and self.xtext == j:
                        glColor3f(0.0,0.0,0.0)
                        continue
                if self.board[i][j] == self.goal_board[i][j]:
                    glColor3f(167/255,87/255,168/255)
                elif self.board[i][j] == 0:
                    glColor3f(1.0, 0.0, 0.0)
                elif self.board[i][j] == 1:
                    glColor3f(0.0,0.0,1.0)
                elif self.board[i][j] == 2:
                    glColor3f(0.0,1.0,0.0)
                elif self.board[i][j] == 3:
                    glColor3f(1.0,1.0,0.0)
                glVertex2f(first+(j*s),first+(i*s))#上縦の線
                glVertex2f(first+((j+1)*s),first+(i*s))
                glVertex2f(first+((j+1)*s),first+((i+1)*s))
                glVertex2f(first+(j*s),first+((i+1)*s))
        glEnd()
        for i in range(height_square):
            for j in range(width_square):
                if self.board[i][j] == self.goal_board[i][j]:
                    self.write_text(167,87,168,first+(j*s),first+(i*s),str(self.board[i][j]))
                    glRasterPos2f(0.0,0.0)
                elif self.board[i][j] == 0:
                    self.write_text(255,0,0,first+(j*s),first+(i*s),'0')
                    glRasterPos2f(0.0,0.0)
                elif self.board[i][j] == 1:
                    self.write_text(0,0,255,first+(j*s),first+(i*s),'1')
                    glRasterPos2f(0.0,0.0)
                elif self.board[i][j] == 2:
                    self.write_text(0,255,0,first+(j*s),first+(i*s),'2')
                    glRasterPos2f(0.0,0.0)
                elif self.board[i][j] == 3:
                    self.write_text(255,255,0,first+(j*s),first+(i*s),'3')
                    glRasterPos2f(0.0,0.0)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        glVertex2f(0.5,0)
        glVertex2f(0.5,1)
        glEnd()
        glBegin(GL_LINES)
        glVertex2f(0,first+((round(height_square/2))*s))
        glVertex2f(1,first+((round(height_square/2))*s))
        glEnd()
        glPopMatrix()
        glFlush()
        glutSwapBuffers()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)




class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.args = sys.argv
        try:
            arg2 = self.args[2]
        except:
            print("引数が足りません")
            exit(1)

        with open(self.args[1]) as f:
            self.problem = json.load(f)
        with open(self.args[2]) as f:
            self.answer = json.load(f)

        self.setMinimumSize(100, 100)
        self.setMaximumSize(1000, 1000)
        self.resize(800, 800)
        self.grabKeyboard()
        self.b_wid = self.problem['board']['width']
        self.b_hei = self.problem['board']['height']
        self.start_board =  [[ int(self.problem['board']['start'][y][x]) for x in range(self.b_wid)]for y in range(self.b_hei)]#スタート盤面
        self.goal_board = [[ int(self.problem['board']['goal'][y][x]) for x in range(self.b_wid)]for y in range(self.b_hei)]#完成盤面
        self.zoom = 1
        self.zoom_direction = 0
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        layout_gl = QHBoxLayout(self)
        layout.addLayout(layout_gl)

        self.error_text = ""

        self.dis_board = [[0 for x in range(self.b_wid)]for y in range(self.b_hei)]
        self.idx = 0
        self.next = self.b_wid*CELL_SIZE+100
        self.button_push
        self.opTimerCallback
        self.timer = QTimer()
        self.timer_oth = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.opTimerCallback)
        self.op_idx = 0#何番目手か
        self.right_key_check = False
        self.direction_mannual_move = 0
        # self.color = {0:0,1:0,2:0,3:0}
        self.dict_action = {0:"上",1:"下",2:"左",3:"右"}
        self.dic_dir = ["上","下","左","右"]
        check_int = True
        self.painter_text = QLabel("")
        self.painter_text.setFixedSize(200,50)
        self.stack_move = [[]]
        layout.addWidget(self.painter_text)
        self.error_label = QLabel("")
        if(self.args[3] == "m"):
            self.ytext = QLineEdit(self)#入力フォームを追加(y座標)
            self.xtext  = QLineEdit(self)#入力フォームを追加(x座標)
            try:#x座標,y座標は数字になっているか
                int(self.xtext.text())
                int(self.ytext.text())
            except ValueError:
                self.error = 5
                check_int = False
                self.Error()
                print('座標の値が有効ではありません')
            if check_int:
                self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,int(self.xtext.text),int(self.ytext.text),self)#操作盤面
            else:
                self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,self)#操作盤面


        elif(self.args[3] == "a"):
            self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,self)#操作盤面


        layout_gl.addWidget(self.glwidget)
        self.glwidget_goal = OpenGLWidget(self.goal_board,[[ -1 for x in range(self.b_wid)]for y in range(self.b_hei)],self.zoom,self.zoom_direction,self)#目的の盤面
        self.painter_layout = QVBoxLayout()
        layout_gl.addWidget(self.glwidget_goal)
        self.error = 0
        if self.args[3] == "a":#自動で移動する場合
            self.slider = QSlider(Qt.Orientation.Horizontal)
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.answer["n"])
            self.slider.setTickInterval(1)
            self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            self.slider.valueChanged.connect(self.onSliderChange)
            layout.addWidget(self.slider)
        elif self.args[3] == "m":#手動モードの場合
            direction_button_layout = QHBoxLayout(self)
            text_layout = QVBoxLayout(self)
            layout.addLayout(direction_button_layout)
            layout.addLayout(text_layout)
            # self.stext = QLineEdit(self)

            self.direction_button_right = QRadioButton("右")#移動する方向を決めるボタン
            self.direction_button_left = QRadioButton("左")
            self.direction_button_up = QRadioButton("上")
            self.direction_button_down = QRadioButton("下")



            direction_button_layout.addWidget(self.direction_button_up)
            self.direction_button_up.clicked.connect(self.up_move)
            direction_button_layout.addWidget(self.direction_button_down)
            self.direction_button_down.clicked.connect(self.down_move)
            direction_button_layout.addWidget(self.direction_button_left)
            self.direction_button_left.clicked.connect(self.left_move)
            direction_button_layout.addWidget(self.direction_button_right)
            self.direction_button_right.clicked.connect(self.right_move)



            self.error_label.setFixedSize(200,50)
            text_layout.addWidget(self.error_label)

            self.xlabel = QLabel("x座標")
            text_layout.addWidget(self.xlabel)
            self.xlabel.setFixedSize(50,20)

            text_layout.addWidget(self.xtext)
            self.ylabel = QLabel("y座標")
            self.ylabel.setFixedSize(50,20)
            text_layout.addWidget(self.ylabel)

            text_layout.addWidget(self.ytext)


            self.button = QPushButton('Move')#動かす処理を実行するボタンを追加

            layout.addWidget(self.button)
            self.button.clicked.connect(self.on_button_click)
            self.back_button = QPushButton('Back')
            layout.addWidget(self.back_button)
            self.back_button.clicked.connect(self.on_back_button_click)





    def up_move(self):#「上」のボタンを選択した場合
        self.direction_mannual_move = 1

    def down_move(self):#「下」のボタンを選択した場合
        self.direction_mannual_move = 2

    def left_move(self):#「左」のボタンを選択した場合
        self.direction_mannual_move = 3
    def right_move(self):#「右」のボタンを選択した場合
        self.direction_mannual_move = 4



    def on_back_button_click(self):#「Back」のボタンを押した場合

        if  self.op_idx >= 1:
            prev_list = self.stack_move.pop()
            self.back(prev_list[0],prev_list[1],self.direction_mannual_move-1)
        else:
            self.error = 6
            self.Error()
            return
        self.error = 0
        self.Error()

        self.update()
        self.glwidget.update()



    def on_button_click(self):#Moveボタンが押されたときの処理
        if  (self.xtext.text() is None) or (self.ytext.text() is None) or (self.direction_mannual_move == 0) or (self.xtext.text() == "") or (self.ytext.text()==""):
            self.error = 4
            self.Error()
            print("入力してください")
            return
        try:#x座標,y座標は数字になっているか
            int(self.xtext.text())
            int(self.ytext.text())
        except ValueError:
            self.error = 5
            self.Error()
            print('座標の値が有効ではありません')
            return




        if (0 <= int(self.xtext.text()) and int(self.xtext.text()) < self.b_wid):#x座標が範囲外の場合

                if (0 <= int(self.ytext.text()) and int(self.ytext.text()) < self.b_hei ):#y座標が範囲外の場合
                    self.move(int(self.xtext.text()),int(self.ytext.text()),self.direction_mannual_move-1)#入力したx座標,y座標,方向を盤面を動かす関数に送る
                    self.stack_move.append([int(self.xtext.text()),int(self.ytext.text())])
                else:
                    self.error = 2
                    self.Error()
                    return

        else:
            self.error = 1
            self.Error()
            return
        self.error = 0
        self.Error()

        self.update()
        self.glwidget.update()

    def Error(self):
        if self.error == 1:
            self.error_label.setText("指定したx座標が範囲外です")
            print('error 1')
        elif self.error == 2:
            self.error_label.setText("指定したy座標が範囲外です")
            print('error 2')
        elif self.error == 3:
            self.error_label.setText("方向が指定できていません 上、下、左、右のどちらかを指定してください。")
            print('error 3')
        elif self.error == 4:
            self.error_label.setText("入力してください")
            print('error 4')
        elif self.error == 5:
            self.error_label.setText("入力した値が数字ではありません")
            print("error5")
        elif self.error == 6:
            self.error_label.setText("これ以上戻せません")
            print("error6")

        else:
            self.error_label.setText("")


    def paintEvent(self, event):
        if not(self.op_idx >= self.answer["n"]):
            x = self.answer["ops"][self.op_idx]["x"]
            y = self.answer["ops"][self.op_idx]["y"]
            s = self.answer["ops"][self.op_idx]["s"]

        painter = QPainter(self)

        painter.setPen(QColor("black"))

        action_text_point = QPoint(30,40)

        if(self.args[3] == "a"):
            self.painter_text.setText(f'{self.op_idx}手目 あと {self.answer["n"]-self.op_idx}手')
            print(f'{self.op_idx}手目 あと {self.answer["n"]-self.op_idx}手')
        elif(self.args[3] == "m"):
            self.painter_text.setText(f'{self.op_idx}手目 ')
            print(f'{self.op_idx}手目')
        if not(self.op_idx >= self.answer["n"]):
            painter.drawText(action_text_point,f'座標: x:{x}y:{y} 次の行動: {self.dict_action[s]} にずらす')
            print(f'座標: x:{x}y:{y} 次の行動: {self.dict_action[s]} にずらす' )
        painter.setPen(QColor("red"))
        if self.args[3] == "m":
            print(f'x内容{self.xtext.text()}')
            print(f'y内容{self.ytext.text()}')
            print(f'方向内容{self.dict_action[self.direction_mannual_move-1] if self.direction_mannual_move > 0 else " "}')


        painter.setBrush(QColor("white"))

        font = painter.font()



    def search_near_goal(self,x,y):#幅優先探索で今の盤面からゴールの盤面の距離を計算している
        que = deque()
        search_board = [[-1 for x in range(self.b_wid)]for y in range(self.b_hei)]
        search_board[y][x] = 0
        if self.start_board[y][x] == self.goal_board[y][x]:
            return search_board[y][x]
        que.append((y,x))
        dy = [1,0,-1,0]
        dx = [0,-1,0,1]
        while que:
            h,w = que.popleft()
            for i in range(4):
                next_h = h + dy[i]
                next_w = w + dx[i]
                if 0 <= next_h < len(search_board) and 0 <= next_w < len(search_board[0]):
                    if search_board[next_h][next_w] == -1:
                        search_board[next_h][next_w] = search_board[h][w]+1
                        que.append((next_h,next_w))
                    if self.start_board[y][x] == self.goal_board[next_h][next_w]:#ゴールした場合
                        return search_board[next_h][next_w]





    def onSliderChange(self,value):
        self.applyOn(value)








    def mousePressEvent(self,event: QMouseEvent):#マウスを押した座標を取得
        x = event.position().x()
        y = event.position().y()
        if y > 460:
            self.releaseKeyboard()
        else:
            self.grabKeyboard()

        print(f"Clicked x:{x}  y:{y}")

    def keyPressEvent(self, event: QKeyEvent):
        if self.args[3] == "a":
            #右キーを押すと一手進む
            if event.key() == Qt.Key.Key_Right and not(self.op_idx == self.answer["n"]):
                self.right_key_check = self.applyOn(self.op_idx+1)
            #左キーに進むと一手戻る
            elif event.key() == Qt.Key.Key_Left and not(self.op_idx == 0):
                self.right_key_check = self.applyOn(self.op_idx-1)

        if event.key() == Qt.Key.Key_W:#Wキーが押された場合
                self.ZoomController(1)

        if event.key() == Qt.Key.Key_A:#Aキーが押された場合
                self.ZoomController(2)

        if event.key() == Qt.Key.Key_S:#Sキーが押された場合
                self.ZoomController(3)

        if  event.key() == Qt.Key.Key_D:#Dキーが押された場合
                self.ZoomController(4)

        if event.key() == Qt.Key.Key_Up:#UPキーが押された場合
                self.ZoomController(5)

        if event.key() == Qt.Key.Key_Down:#Downキーが押された場合
                self.ZoomController(6)

        if event.key() == Qt.Key.Key_R:#Rキーが押された場合
                self.ZoomController(7)

        if event.key() == Qt.Key.Key_E:#Eキーが押された場合
                self.ZoomController(8)





    def ZoomController(self,num):#クリックしたキーごとに処理を実行する
        print(f'ZOOM:{self.glwidget.zoom}')
        print(f'ZOOMX:{self.glwidget.zoomx}')
        print(f'ZOOMY:{self.glwidget.zoomy}')
        if num == 1:
            if self.glwidget.zoomy*self.glwidget.zoom+(self.glwidget.zoom*2)+0.1  <=  2.0:#拡大する場合ZZZ
                self.glwidget.zoomy += 0.1
                if self.glwidget.zoom_direction >= 2:
                    self.glwidget.zoom_direction -= 2
            else:
                self.glwidget.zoomy = 2/self.glwidget.zoom-2



        elif num == 2:
            if self.glwidget.zoomx-0.1  >=  0:
                self.glwidget.zoomx -= 0.1
                if self.glwidget.zoom_direction % 2 == 1:
                    self.glwidget.zoom_direction -= 1
            else:
                self.glwidget.zoomx = 0
            print(self.glwidget.zoom_direction)
        elif num == 3:
            if self.glwidget.zoomy-0.1  >=  0:
                self.glwidget.zoomy -= 0.1
                if self.glwidget.zoom_direction <= 2:
                    self.glwidget.zoom_direction += 2
            else:
                self.glwidget.zoomy = 0

        elif num == 4:
            if self.glwidget.zoomx*self.glwidget.zoom+(self.glwidget.zoom*2)+0.1  <=  2.0:
                self.glwidget.zoomx += 0.1
                if self.glwidget.zoom_direction % 2 == 0:
                    self.glwidget.zoom_direction += 1
            else:
                self.glwidget.zoomx = 2/self.glwidget.zoom-2



        elif num == 5:
            if self.glwidget.zoom >= 0.05:
                self.glwidget.zoom /=2
        elif num == 6:
            if self.glwidget.zoom*2 <= 1:
                self.glwidget.zoom*=2

        elif num == 7:
            self.glwidget.zoom = 1
            self.glwidget.zoomx = 0
            self.glwidget.zoomy = 0
        self.glwidget.update()

    #0.5秒ごとに進む・戻る
    def opTimerCallback(self):
        self.applyOn(self.op_idx+1)
        if self.op_idx == self.answer["n"]:
                self.timer.stop()

    def print_distance_board(self):
        self.dis_board = [[self.search_near_goal(x,y) for x in range(self.b_wid)]for y in range(self.b_hei)]
        print("------------------距離ボード--------------")
        for i in range(len(self.dis_board)):
            print(self.dis_board[i])

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
        self.glwidget.update()
    #一手進める
    def apply_forward(self):
        print(1)
        print(self.op_idx)
        x = self.answer["ops"][self.op_idx]["x"]
        y = self.answer["ops"][self.op_idx]["y"]
        s = self.answer["ops"][self.op_idx]["s"]
        self.move(x,y,s)


    def move(self,x,y,s):#ボードを変更する
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
        print(2)
        print(self.op_idx)
        x = self.answer["ops"][self.op_idx-1]["x"]
        y = self.answer["ops"][self.op_idx-1]["y"]
        s = self.answer["ops"][self.op_idx-1]["s"]
        self.back(x,y,s)

    def back(self,x,y,s):
        if s == 0:
            for i in range(self.b_hei-1,y,-1):
                self.start_board[i-1][x],self.start_board[i][x] = self.start_board[i][x],self.start_board[i-1][x]#上方向のずれを戻す
        elif s == 1:
            for i in range(0,y):
                self.start_board[i][x],self.start_board[i+1][x] = self.start_board[i+1][x],self.start_board[i][x]#下方向のずれを戻す

        elif s == 2:
            for i in range(self.b_wid-1,x,-1):
                self.start_board[y][i],self.start_board[y][i-1] = self.start_board[y][i-1],self.start_board[y][i]#左方向のずれを戻す

        else:
            for i in range(0,x):
                self.start_board[y][i],self.start_board[y][i+1] = self.start_board[y][i+1],self.start_board[y][i]#右方向のずれを戻す
        self.op_idx -= 1

    #タイマーを開始させる
    def start_play(self):
        #qTimerを作る
        self.timer.start()
    def button_push():
        print("pushed! button")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test GUI')
        self.setGeometry(300, 50, 1000, 1000)
        self.widget = MainWidget(self)
        self.layout().addWidget(self.widget)



def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    # w.start_play()
    w.show()
    w.raise_()
    app.exec()



if __name__ == '__main__':
    main()
