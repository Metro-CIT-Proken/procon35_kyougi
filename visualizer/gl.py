from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QWidget

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np
from collections import deque
import colorsys
from mainwidget import *

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
    def __init__(self,board,goal_board,zoom,zoom_direction,xtext_int=None,ytext_int=None,fournflag=None,parent=None):
        super().__init__(parent)
        self.is_focus = False
        self.board = board
        self.goal_board = goal_board
        self.zoom = zoom
        self.zoom_direction = zoom_direction
        self.setMinimumSize(0, 10)
        self.setMaximumSize(1000, 1000)

        self.zoomx = 0
        self.zoomy = 0
        self.xtext_int = xtext_int
        self.ytext_int = ytext_int
        # self.is_focus = False
        # self.answer = answer
        # self.op_idx = op_idx
        self.yazirusi = ""
        # self.args = args
        self.fournflag = fournflag
        self.is_focus = False
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)





    def write_text(self, r, g, b, w, h, string):
        # 初期化
        img = np.zeros((132, 128, 3), dtype=np.uint8)

        # 文字列を画像に描画 (BGR ではなく、最初からRGBで描画)
        cv2.putText(img, string, (60, 70), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

        # カラー変換を削除して最初からRGBで処理する
        img = cv2.flip(img, 0)

        # OpenGL描画位置設定
        glRasterPos2f(w, h)

        # OpenGL描画時の色設定
        glColor3f(0.0, 0.0, 0.0)

        # 指定の色で置換 (np.whereは非効率なので、画像全体に対して高速処理)
        target_color = (0, 0, 0)
        change_color = (r, g, b)

        # 遅いnp.whereの代わりに、numpyの直接操作で色を変更
        mask = np.all(img == target_color, axis=-1)
        img[mask] = change_color

        # OpenGLにピクセルを描画
        glDrawPixels(img.shape[1], img.shape[0], GL_RGB, GL_UNSIGNED_BYTE, img)


    # def write_text(self,r,g,b,w,h,string):#,r,g,b,w,h
    #     img = np.zeros((132,128,3),dtype=np.uint8)
    #     cv2.putText(img,string, (60, 70), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255))
    #     img = cv2.flip(img, 0)
    #     img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #     glRasterPos2f(w,h)
    #     glColor3f(0.0, 0.0, 0.0)
    #     target_color = (0, 0, 0)
    #     change_color = (r, g, b)
    #     img = np.where(img == target_color, change_color, (255, 255, 255))
    #     glDrawPixels(img.shape[1], img.shape[0], GL_RGB,GL_UNSIGNED_BYTE, img)


    def initializeGL(self):
        glClearColor(1.0,1.0,1.0,1.0)


    def hsv_to_rgb(self,h,s,v):
        return colorsys.hsv_to_rgb(h/255, s/255, v/255)

    def search_near_goal(self,x,y):#幅優先探索で今の盤面からゴールの盤面の距離を計算している
        que = deque()
        search_board = [[-1 for x in range(self.b_wid)]for y in range(self.b_hei)]
        search_board[y][x] = 0
        if self.board[y][x] == self.goal_board[y][x]:
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
                    if self.board[y][x] == self.goal_board[next_h][next_w]:#ゴールした場合
                        return search_board[next_h][next_w]

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 0.0, 0.0)# 色を赤に設定

        glRasterPos2f(0.0,0.0)
        width_square = len(self.board[0])
        height_square = len(self.board)
        if width_square != 0:
            sx = 1/width_square
            sy = 1/height_square
        else:
            sx = 1
            sy = 1
        first = FIRST/TRANSLATE_GL
        s = min(sx,sy)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()

        first = 0
        self.b_hei = len(self.board)
        self.b_wid = len(self.board[0])
        color = {0:0,1:0,2:0,3:0}
        r,g,b = 0.0,0.0,0.0
        glTranslate(-1, -1, 0)
        glTranslate(-self.zoomx, -self.zoomy, 1)
        glScale(2/self.zoom, 2/self.zoom, 1)




        glBegin(GL_QUADS)

        for i in range(height_square):
            for j in range(width_square):
                if self.fournflag and not(self.fournflag == None):
                        ratio = self.search_near_goal(j,i)/max(self.b_hei,self.b_wid)*3#距離が遠ければ色が薄くなり近くなれば濃くなる
                        saturation = 90*(1.0-ratio)
                        h,ss,v = color[self.board[i][j]]*60,int(saturation*255//100),255
                        r,g,b = self.hsv_to_rgb(h,ss,v)
                        glColor3f(r, g, b)



                elif self.board[i][j] == self.goal_board[i][j] and not(self.fournflag == None):
                    glColor3f(167/255,87/255,168/255)
                elif self.board[i][j] == 0 and not(self.fournflag == None):
                    glColor3f(1.0, 0.0, 0.0)
                elif self.board[i][j] == 1 and not(self.fournflag == None):
                    glColor3f(0.0,0.0,1.0)
                elif self.board[i][j] == 2 and not(self.fournflag == None):
                    glColor3f(0.0,1.0,0.0)
                elif self.board[i][j] == 3 and not(self.fournflag == None):
                    glColor3f(1.0,1.0,0.0)

                elif self.ytext_int == i and self.xtext_int == j and not(self.fournflag == None):
                    if not(self.xtext_int == None or self.ytext_int == None):
                        glColor3f(0.0,0.0,0.0)
                glVertex2f(first+(j*s),first+(i*s))#上縦の線
                glVertex2f(first+((j+1)*s),first+(i*s))
                glVertex2f(first+((j+1)*s),first+((i+1)*s))
                glVertex2f(first+(j*s),first+((i+1)*s))
        glEnd()
        for i in range(height_square):
            for j in range(width_square):
                if self.fournflag and not(self.fournflag == None) and not(self.ytext_int==i and self.xtext_int == j):
                    ratio = self.search_near_goal(j,i)/max(self.b_hei,self.b_wid)*3#距離が遠ければ色が薄くなり近くなれば濃くなる
                    saturation = 90*(1.0-ratio)
                    h,ss,v = color[self.board[i][j]]*60,int(saturation*255//100),255
                    r,g,b = self.hsv_to_rgb(h,ss,v)
                    r*=255
                    g*=255
                    b*=255
                    if self.ytext_int is not  None  and self.xtext_int is not  None and self.yazirusi == "v" and i > self.ytext_int and j == self.xtext_int:
                        self.write_text(r,g,b,first+(j*s),first+(i*s),self.yazirusi+str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                    elif self.ytext_int is not  None  and self.xtext_int is not  None and self.yazirusi == "^" and i < self.ytext_int and j == self.xtext_int:
                        self.write_text(r,g,b,first+(j*s),first+(i*s),self.yazirusi+str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                    elif self.ytext_int is not  None  and self.xtext_int is not  None and self.yazirusi == "->" and i == self.ytext_int and j < self.xtext_int:
                        self.write_text(r,g,b,first+(j*s),first+(i*s),self.yazirusi+str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                    elif self.ytext_int is not  None  and self.xtext_int is not  None and self.yazirusi == "<-" and i == self.ytext_int and j > self.xtext_int:
                        self.write_text(r,g,b,first+(j*s),first+(i*s),self.yazirusi+str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                    else:
                        self.write_text(r,g,b,first+(j*s),first+(i*s),str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                elif self.ytext_int == i and self.xtext_int == j:
                    if not(self.xtext_int == None or self.ytext_int == None):
                        self.write_text(0,0,0,first+(j*s),first+(i*s),str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)

                elif self.board[i][j] == self.goal_board[i][j]:
                    if self.yazirusi == "v" and i > self.ytext_int and j == self.xtext_int:
                        self.write_text(167,87,168,first+(j*s),first+(i*s),self.yazirusi+str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "^" and i < self.ytext_int and j == self.xtext_int:
                        self.write_text(167,87,168,first+(j*s),first+(i*s),self.yazirusi+str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "->" and i == self.ytext_int and j < self.xtext_int:
                        self.write_text(167,87,168,first+(j*s),first+(i*s),self.yazirusi+str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "<-" and i == self.ytext_int and j > self.xtext_int:
                        self.write_text(167,87,168,first+(j*s),first+(i*s),self.yazirusi+str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                    else:
                        self.write_text(167,87,168,first+(j*s),first+(i*s),str(self.board[i][j]))
                        glRasterPos2f(0.0,0.0)
                elif self.board[i][j] == 0:
                    if self.yazirusi == "v" and i > self.ytext_int and j == self.xtext_int:
                        self.write_text(255,0,0,first+(j*s),first+(i*s),self.yazirusi+'0')
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "^" and i < self.ytext_int and j == self.xtext_int:
                        self.write_text(255,0,0,first+(j*s),first+(i*s),self.yazirusi+'0')
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "->" and i == self.ytext_int and j < self.xtext_int:
                        self.write_text(255,0,0,first+(j*s),first+(i*s),self.yazirusi+'0')
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "<-" and i == self.ytext_int and j > self.xtext_int:
                        self.write_text(255,0,0,first+(j*s),first+(i*s),self.yazirusi+'0')
                        glRasterPos2f(0.0,0.0)
                    else:
                        self.write_text(255,0,0,first+(j*s),first+(i*s),'0')
                        glRasterPos2f(0.0,0.0)
                elif self.board[i][j] == 1:
                    if self.yazirusi == "v" and i > self.ytext_int and j == self.xtext_int:
                        self.write_text(0,0,255,first+(j*s),first+(i*s),self.yazirusi+'1')
                        glRasterPos2f(0.0,0.0)
                    elif  self.yazirusi == "^" and i < self.ytext_int and j == self.xtext_int:
                        self.write_text(0,0,255,first+(j*s),first+(i*s),self.yazirusi+'1')
                        glRasterPos2f(0.0,0.0)
                    elif  self.yazirusi == "->" and i == self.ytext_int and j < self.xtext_int:
                        self.write_text(0,0,255,first+(j*s),first+(i*s),self.yazirusi+'1')
                        glRasterPos2f(0.0,0.0)
                    elif  self.yazirusi == "<-" and i == self.ytext_int and j > self.xtext_int:
                        self.write_text(0,0,255,first+(j*s),first+(i*s),self.yazirusi+'1')
                        glRasterPos2f(0.0,0.0)
                    else:
                        self.write_text(0,0,255,first+(j*s),first+(i*s),'1')
                        glRasterPos2f(0.0,0.0)
                elif self.board[i][j] == 2:
                    if self.yazirusi == "v" and i > self.ytext_int and j == self.xtext_int:
                        self.write_text(0,255,0,first+(j*s),first+(i*s),self.yazirusi+'2')
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "^" and i < self.ytext_int and j == self.xtext_int:
                        self.write_text(0,255,0,first+(j*s),first+(i*s),self.yazirusi+'2')
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "->" and i == self.ytext_int and j < self.xtext_int:
                        self.write_text(0,255,0,first+(j*s),first+(i*s),self.yazirusi+'2')
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "<-" and i == self.ytext_int and j > self.xtext_int:
                        self.write_text(0,255,0,first+(j*s),first+(i*s),self.yazirusi+'2')
                        glRasterPos2f(0.0,0.0)
                    else:
                        self.write_text(0,255,0,first+(j*s),first+(i*s),'2')
                        glRasterPos2f(0.0,0.0)
                elif self.board[i][j] == 3:
                    if self.yazirusi == "v" and i > self.ytext_int and j == self.xtext_int:
                        self.write_text(255,255,0,first+(j*s),first+(i*s),self.yazirusi+'3')
                        glRasterPos2f(0.0,0.0)

                    elif self.yazirusi == "^" and i < self.ytext_int and j == self.xtext_int:
                        self.write_text(255,255,0,first+(j*s),first+(i*s),self.yazirusi+'3')
                        glRasterPos2f(0.0,0.0)
                    elif self.yazirusi == "->" and i == self.ytext_int and j < self.xtext_int:
                        self.write_text(255,255,0,first+(j*s),first+(i*s),self.yazirusi+'3')
                        glRasterPos2f(0.0,0.0)

                    elif self.yazirusi == "<-" and i == self.ytext_int and j > self.xtext_int:
                        self.write_text(255,255,0,first+(j*s),first+(i*s),self.yazirusi+'3')
                        glRasterPos2f(0.0,0.0)
                    else:
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
        print(f"height:{height},width:{width}")
        print(f"最小{min(height,width)}")



        # ウィンドウのサイズ変更時に呼ばれる
        if height == 0:
            height = 1  # ゼロ除算を防ぐため高さを1に設定

        # ビューポートをウィンドウサイズに合わせて設定
        glViewport(0, 0, width, height)

        # アスペクト比に応じた投影行列を設定
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect_ratio = width / height
        if aspect_ratio > 1.0:
            # 横長の場合は横に広げる
            glOrtho(-aspect_ratio, aspect_ratio, -1.0, 1.0, -1.0, 1.0)
        else:
            # 縦長の場合は縦に広げる
            glOrtho(-1.0, 1.0, -1.0 / aspect_ratio, 1.0 / aspect_ratio, -1.0, 1.0)

        glMatrixMode(GL_MODELVIEW)


    def mousePressEvent(self,event):
        self.update()
        super().mousePressEvent(event)

    def focusInEvent(self,event):
        self.is_focus = True
        print("get focus gl")
        super().focusInEvent(event)

    def focusOutEvent(self,event):
        self.is_focus = False
        print("lost focus gl")
        super().focusOutEvent(event)
