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
        self.yazirusi = ""
        self.fournflag = fournflag
        self.is_focus = False
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.textures = {}

        self.generate_textures()


    def generate_textures(self):
        gen_chars = "0123"
        for c in gen_chars:
            self.generate_char_texture(c)

    def generate_char_texture(self, char):
        img = np.zeros((64, 64, 4), dtype=np.uint8)
        # img = cv2.flip(img,0)
        bgr_img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        bgr_img = cv2.putText(bgr_img, char, (32, 32), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255),  lineType=cv2.LINE_AA)
        out_img =  cv2.cvtColor(bgr_img,cv2.COLOR_BGR2RGBA)

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if np.all(out_img[i, j, :3] == (0, 0, 0)):
                    out_img[i, j, 3] = 0

        height,width, _ = img.shape
        glEnable(GL_TEXTURE_2D)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # OpenGLにテクスチャデータとして画像を送信
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, out_img)


        self.textures[char] = texture_id





    def initializeGL(self):
        glClearColor(1.0,1.0,1.0,1.0)
        # glEnable(GL_DEPTH_TEST)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # glGenerateMipmap(GL_TEXTURE_2D)
        # glEnable(GL_CULL_FACE)  # バックフェースカリングを有効化
        # glCullFace(GL_BACK)     # 裏面をスキップ


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
        print("paint gl")
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
                if self.fournflag:
                        ratio = self.search_near_goal(j,i)/max(self.b_hei,self.b_wid)*3#距離が遠ければ色が薄くなり近くなれば濃くなる
                        saturation = 90*(1.0-ratio)
                        h,ss,v = color[self.board[i][j]]*60,int(saturation*255//100),255
                        r,g,b = self.hsv_to_rgb(h,ss,v)
                        glColor3f(r, g, b)


                else:
                    if self.board[i][j] == self.goal_board[i][j] :
                        glColor3f(167/255,87/255,168/255)
                    elif self.board[i][j] == 0 :
                        glColor3f(1.0, 0.0, 0.0)
                    elif self.board[i][j] == 1 :
                        glColor3f(0.0,0.0,1.0)
                    elif self.board[i][j] == 2 :
                        glColor3f(0.0,1.0,0.0)
                    elif self.board[i][j] == 3 :
                        glColor3f(1.0,1.0,0.0)

                glVertex2f(first+(j*s),first+(i*s))#上縦の線
                glVertex2f(first+((j+1)*s),first+(i*s))
                glVertex2f(first+((j+1)*s),first+((i+1)*s))
                glVertex2f(first+(j*s),first+((i+1)*s))
        glEnd()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        for i in range(height_square):
            for j in range(width_square):
                glBindTexture(GL_TEXTURE_2D, self.textures[str(self.board[i][j])])

                glBegin(GL_QUADS)
                glTexCoord2f(0, 1)
                glVertex2f(first+(j*s), first+(i*s))

                glTexCoord2f(1, 1)
                glVertex2f(first+((j+1)*s), first+(i*s))

                glTexCoord2f(1, 0)
                glVertex2f(first+((j+1)*s),first+((i+1)*s))

                glTexCoord2f(0, 0)
                glVertex2f(first+(j*s), first+((i+1)*s))
                glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        glFlush()
        glutSwapBuffers()

    def resizeGL(self, width, height):



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
        # self.update()
        super().mousePressEvent(event)

    def focusInEvent(self,event):
        self.is_focus = True
        super().focusInEvent(event)

    def focusOutEvent(self,event):
        self.is_focus = False
        super().focusOutEvent(event)
