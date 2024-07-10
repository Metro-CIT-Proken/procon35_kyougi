import sys

from collections import deque
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import json
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np

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
    def __init__(self,board,goal_board,zoom,zoom_direction,parent=None):
        super().__init__(parent)
        self.board = board
        self.goal_board = goal_board
        self.zoom = zoom
        self.zoom_direction = zoom_direction
        self.setMinimumSize(100, 100)
        self.setMaximumSize(400, 400)
        self.loc = 0
        self.pox = 0
        self.poy = 0
        self.zoomx = 0
        self.zoomy = 0




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


    # def drawText(self,position,string,fontsize=32):
    #     font = ImageFont.truetype("Roboto-Regular.ttf", fontsize)
    #     textWidth, textHeight = font.getsize(string)
    #     image = Image.new("RGBA", (textWidth, textHeight))
    #     draw = ImageDraw.Draw(image)
    #     draw.text((0, 0), string, font=font, fill=(255, 255, 255, 255))
    #     data = image.tobytes("raw", "RGBA", 0, -1)
    #     glRasterPos2f(*position)
    #     glDrawPixels(textWidth, textHeight, GL_RGBA, GL_UNSIGNED_BYTE, data)


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

        # if self.zoom_direction == 0:
        #     self.poy = self.poy + (first+height_square*s)*self.zoom
        #     glOrtho(self.pox, self.pox+1*self.zoom, self.poy, self.poy+(first+height_square*s)*self.zoom, -1, 1)


        # elif self.zoom_direction == 1:
        #     self.poy = self.poy + (first+height_square*s)*self.zoom
        #     self.pox = self.pox + 1*self.zoom
        #     glOrtho(self.pox, self.pox+1*self.zoom, self.poy, self.poy+(first+height_square*s)*self.zoom, -1, 1)

        # elif self.zoom_direction == 2:
        #     glOrtho(self.pox, self.pox+1*self.zoom, self.poy, self.poy+(first+height_square*s)*self.zoom, -1, 1)

        # elif self.zoom_direction == 3:
        #     self.pox = self.pox + 1*self.zoom
        #     glOrtho(self.pox, self.pox+1*self.zoom, self.poy, self.poy+(first+height_square*s)*self.zoom, -1, 1)

        first = 0

        glTranslate(-1, -1, 0)
        glTranslate(self.zoomx, self.zoomy, 0)
        glScale(2/self.zoom, 2/self.zoom, 1)




        glBegin(GL_QUADS)
        for i in range(height_square):
            for j in range(width_square):

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
        layout_gl = QHBoxLayout()
        layout.addLayout(layout_gl)
        # self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,self)

        # layout_gl.addWidget(self.glwidget)
        # self.glwidget_goal = OpenGLWidget(self.goal_board,[[ -1 for x in range(self.b_wid)]for y in range(self.b_hei)],self.zoom,self.zoom_direction,self)
        # layout_gl.addWidget(self.glwidget_goal)


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
        # self.color = {0:0,1:0,2:0,3:0}
        self.dict_action = {0:"上",1:"下",2:"左",3:"右"}
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.answer["n"])
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self.onSliderChange)


        self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,self)
        layout_gl.addWidget(self.glwidget)
        self.glwidget_goal = OpenGLWidget(self.goal_board,[[ -1 for x in range(self.b_wid)]for y in range(self.b_hei)],self.zoom,self.zoom_direction,self)
        layout_gl.addWidget(self.glwidget_goal)
        layout.addWidget(self.slider)




    def paintEvent(self, event):
        if not(self.op_idx >= self.answer["n"]):
            x = self.answer["ops"][self.op_idx]["x"]
            y = self.answer["ops"][self.op_idx]["y"]
            s = self.answer["ops"][self.op_idx]["s"]

        painter = QPainter(self)
        painter.setPen(QColor("black"))
        count_point = QPoint(30,20)
        action_text_point = QPoint(30,40)
        painter.drawText(count_point,f'{self.op_idx}手目 あと {self.answer["n"]-self.op_idx}手')
        print(f'{self.op_idx}手目 あと {self.answer["n"]-self.op_idx}手')
        if not(self.op_idx >= self.answer["n"]):
            painter.drawText(action_text_point,f'座標: x:{x}y:{y} 次の行動: {self.dict_action[s]} にずらす' )
            print(f'座標: x:{x}y:{y} 次の行動: {self.dict_action[s]} にずらす' )
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


    def keyPressEvent(self, event: QKeyEvent):
        #右キーを押すと一手進む
        if event.key() == Qt.Key.Key_Right and not(self.op_idx == self.answer["n"]):
            self.right_key_check = self.applyOn(self.op_idx+1)
        #左キーに進むと一手戻る
        elif event.key() == Qt.Key.Key_Left and not(self.op_idx == 0):
            self.right_key_check = self.applyOn(self.op_idx-1)


        if event.key() == Qt.Key.Key_W:
            self.ZoomController(1)

        if event.key() == Qt.Key.Key_A:
            self.ZoomController(2)

        if event.key() == Qt.Key.Key_S:
            self.ZoomController(3)

        if  event.key() == Qt.Key.Key_D:
            self.ZoomController(4)

        if event.key() == Qt.Key.Key_Up:
            self.ZoomController(5)

        if event.key() == Qt.Key.Key_Down:
            self.ZoomController(6)
        if event.key() == Qt.Key.Key_R:
            self.ZoomController(7)

        if event.key() == Qt.Key.Key_E:
            self.ZoomController(8)

    def ZoomController(self,num):
        if num == 1:
            if self.glwidget.zoom_direction >= 2:
                self.glwidget.zoom_direction -= 2
            self.glwidget.zoomy += 0.1


        elif num == 2:
            if self.glwidget.zoom_direction % 2 == 1:
                self.glwidget.zoom_direction -= 1
            self.glwidget.zoomx -= 0.1

            print("minus")
            print(self.glwidget.zoom_direction)
        elif num == 3:
            if self.glwidget.zoom_direction <= 2:
                self.glwidget.zoom_direction += 2
            self.glwidget.zoomy -= 0.1
        elif num == 4:
            if self.glwidget.zoom_direction % 2 == 0:
                self.glwidget.zoom_direction += 1
            self.glwidget.zoomx += 0.1

        elif num == 5:
            if self.glwidget.zoom >= 0.05:
                self.glwidget.zoom /=2
                print("zoom")
                print(self.glwidget.zoom)
        elif num == 6:
            if self.glwidget.zoom*2 <= 1:
                self.glwidget.zoom*=2
                print("zoomout")
                print(self.glwidget.zoom)

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
        board_x_size = len(self.start_board[0])#ボードの横の大きさ
        board_y_size = len(self.start_board)#ボードの縦の大きさ
        if s == 0:
            for i in range(board_y_size-1,y,-1):
                self.start_board[i-1][x],self.start_board[i][x] = self.start_board[i][x],self.start_board[i-1][x]#上方向のずれを戻す
        elif s == 1:
            for i in range(0,y):
                self.start_board[i][x],self.start_board[i+1][x] = self.start_board[i+1][x],self.start_board[i][x]#下方向のずれを戻す

        elif s == 2:
            for i in range(board_x_size-1,x,-1):
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
