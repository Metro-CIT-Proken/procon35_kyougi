import sys

from gl import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from PyQt6.QtWidgets import *

import json
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from scroll_widget import *
from collections import Counter

import numpy
from termcolor import colored
from move import *
from back import *
from config import *
from get_problem import *
from post_answer import *



class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.args = sys.argv
        try:
            arg2 = self.args[2]
        except:
            exit(1)

        with open(self.args[1]) as f:
            self.problem = json.load(f)
        with open(self.args[2]) as f:
            self.answer = json.load(f)

        self.fixed_form_num =  self.problem['general']['n']
        self.fixed_form_numbers = [ self.problem['general']['patterns'][x]['p'] for x in range(self.fixed_form_num)]
        self.fixed_form_widths = { self.fixed_form_numbers[x] : self.problem['general']['patterns'][x]['width'] for x in range(self.fixed_form_num)}
        self.fixed_form_heights = {self.fixed_form_numbers[x] : self.problem['general']['patterns'][x]['height'] for x in range(self.fixed_form_num)}
        self.fixed_form_cells = {self.fixed_form_numbers[x] : [ [self.problem['general']['patterns'][x]['cells'][i][j] for j in range(len(self.problem['general']['patterns'][x]['cells'][i]))]for i in range(len(self.problem['general']['patterns'][x]['cells'])) ]  for x in range(self.fixed_form_num)}
        self.b_wid = self.problem['board']['width']
        self.b_hei = self.problem['board']['height']
        self.widgets_list = [[]]
        self.start_board =  [[ int(self.problem['board']['start'][y][x]) for x in range(self.b_wid)]for y in range(self.b_hei)]#スタート盤面
        self.goal_board = [[ int(self.problem['board']['goal'][y][x]) for x in range(self.b_wid)]for y in range(self.b_hei)]#完成盤面
        self.zoom = 1
        self.zoom_direction = 0
        layout = QHBoxLayout(self)
        layout_cont = QVBoxLayout()
        layout_gl = QHBoxLayout()


        layout.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(layout_cont, 1)
        # layout.addLayout(layout_gl,2)
        layout.addLayout(layout_gl, 2)


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
        self.config = Config("config.json")
        try:
            self.config.load()
        except:
            pass
        # self.color = {0:0,1:0,2:0,3:0}
        self.dict_action = {0:"上", 1:"下", 2:"左", 3:"右"}
        self.dic_dir = ["上", "下", "左", "右"]
        check_int = True
        self.painter_text = QLabel("")
        self.painter_text.setFixedSize(200, 50)
        self.stack_move = [[]]
        layout_cont.addWidget(self.painter_text)
        self.error_label = QLabel("")
        fournflag = False

        try:
                self.args[4]
        except IndexError:
                self.args.append("")
                fournflag = True
        if(self.args[3] == "m"):
            self.direction_mannual_move = -1
            self.ytext = QLineEdit(self)#入力フォームを追加(y座標)
            self.xtext  = QLineEdit(self)#入力フォームを追加(x座標)
            self.cells_number = QLineEdit(self)

            try:#x座標,y座標は数字になっているか
                int(self.xtext.text())
                int(self.ytext.text())
            except ValueError:
                check_int = False
                if  not((self.xtext.text() is None) or (self.ytext.text() is None) or (self.direction_mannual_move == -1) or (self.xtext.text() == "") or (self.ytext.text()=="")):
                    self.error = 5
                    self.Error()

            if check_int and (int(self.xtext.text()) >= 0 ) and int(self.ytext.text()) >= 0 and int(self.ytext.text()) < self.b_hei and int(self.xtext.text()) < self.b_wid and not(self.args[4] == 's'):
                self.glwidget = OpenGLWidget(self.start_board, self.goal_board, self.zoom, self.zoom_direction, int(self.xtext.text()), int(self.ytext.text()), None, self)#操作盤面
            if check_int and (int(self.xtext.text()) >= 0 ) and int(self.ytext.text()) >= 0 and int(self.ytext.text()) < self.b_hei and int(self.xtext.text()) < self.b_wid and self.args[4] == 's':
                self.glwidget = OpenGLWidget(self.start_board, self.goal_board, self.zoom, self.zoom_direction, int(self.xtext.text()), int(self.ytext.text()), fournflag, self)
            else:
                if fournflag and not(self.args[4] == 's'):
                    self.glwidget = OpenGLWidget(self.start_board, self.goal_board, self.zoom, self.zoom_direction, None, None, None, self)#操作盤面
                else:
                    self.glwidget= OpenGLWidget(self.start_board, self.goal_board, self.zoom, self.zoom_direction, None, None, fournflag, self)

        elif(self.args[3] == "a"):
            self.ip_address_line = QLineEdit(self)
            self.ip_address_line.setText(self.config.ip_address)

            self.ip_address_line.textEdited.connect(self.config.ip_address_edited)
            self.port_line = QLineEdit(self)
            self.port_line.setText(str(self.config.port))
            self.port_line.textEdited.connect(self.config.port_edited)
            self.token_line = QLineEdit(self)
            self.token_line.setText(self.config.token)
            self.token_line.textEdited.connect(self.config.token_edited)
            self.get_button = QPushButton("GET",self)
            self.post_button = QPushButton("POST",self)
            if self.args[4] == 's':
                self.glwidget = OpenGLWidget(self.start_board, self.goal_board, self.zoom, self.zoom_direction, None, None, fournflag, self)
            else:
                self.glwidget = OpenGLWidget(self.start_board, self.goal_board,self.zoom,self.zoom_direction,None,None,None,self)#操作盤面



        self.glwidget_goal = OpenGLWidget(self.goal_board, [[ -1 for x in range(self.b_wid)]for y in range(self.b_hei)], self.zoom, self.zoom_direction, self)#目的の盤面



        scroll_area = ScrollWidget(self.glwidget, self.glwidget_goal)


        layout_gl.addWidget(scroll_area)

        self.error = 0
        if self.args[3] == "a":#自動で移動する場合
            self.slider = QSlider(Qt.Orientation.Horizontal)
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.answer["n"])
            self.slider.setTickInterval(1)
            self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            self.slider.valueChanged.connect(self.onSliderChange)
            ip_address_label = QLabel("IPアドレス")
            ip_address_label.setFixedSize(100,20)

            port_label = QLabel("ポート番号")
            port_label.setFixedSize(100,20)

            token_label = QLabel("トークン")
            token_label.setFixedSize(100,20)

            layout_text = QVBoxLayout()
            layout_cont.addLayout(layout_text)
            layout_text.addWidget(ip_address_label)
            layout_text.addWidget(self.ip_address_line)
            layout_text.addWidget(port_label)
            layout_text.addWidget(self.port_line)
            layout_text.addWidget(token_label)
            layout_text.addWidget(self.token_line)



            self.get_button.clicked.connect(self.get)
            self.post_button.clicked.connect(self.post)

            layout_button = QHBoxLayout()
            layout_cont.addLayout(layout_button)

            layout_button.addWidget(self.get_button)
            layout_button.addWidget(self.post_button)


            layout_cont.addWidget(self.slider)

        elif self.args[3] == "m":
            layout_button = QHBoxLayout()
            layout_cont.addLayout(layout_button)
            self.direction_button_right = QRadioButton("右")#移動する方向を決めるボタン
            self.direction_button_left = QRadioButton("左")
            self.direction_button_up = QRadioButton("上")
            self.direction_button_down = QRadioButton("下")



            layout_button.addWidget(self.direction_button_up)
            self.direction_button_up.clicked.connect(self.up_move)
            layout_button.addWidget(self.direction_button_down)
            self.direction_button_down.clicked.connect(self.down_move)
            layout_button.addWidget(self.direction_button_left)
            self.direction_button_left.clicked.connect(self.left_move)
            layout_button.addWidget(self.direction_button_right)
            self.direction_button_right.clicked.connect(self.right_move)

            layout_text = QHBoxLayout()
            layout_text2 = QHBoxLayout()
            layout_cont.addLayout(layout_text)
            layout_cont.addLayout(layout_text2)


            self.error_label.setFixedSize(200,50)
            layout_cont.addWidget(self.error_label)

            self.xlabel = QLabel("x座標")
            layout_text.addWidget(self.xlabel)
            self.xlabel.setFixedSize(50,20)
            layout_text.addWidget(self.xtext)

            self.ylabel = QLabel("y座標")
            self.ylabel.setFixedSize(50,20)
            layout_text.addWidget(self.ylabel)
            layout_text.addWidget(self.ytext)

            self.cells_number_label = QLabel("抜き型の辺の長さ")
            self.cells_number_label.setFixedSize(50,20)
            layout_text2.addWidget(self.cells_number_label)
            layout_text2.addWidget(self.cells_number)




            layout_action = QHBoxLayout()
            layout_cont.addLayout(layout_action)
            self.button = QPushButton('Move')#動かす処理を実行するボタンを追加

            layout_action.addWidget(self.button)
            self.button.clicked.connect(self.on_button_click)
            self.back_button = QPushButton('Back')
            layout_action.addWidget(self.back_button)
            self.back_button.clicked.connect(self.on_back_button_click)








    def up_move(self):#「上」のボタンを選択した場合
        self.direction_mannual_move = 0

    def down_move(self):#「下」のボタンを選択した場合
        self.direction_mannual_move = 1

    def left_move(self):#「左」のボタンを選択した場合
        self.direction_mannual_move = 2
    def right_move(self):#「右」のボタンを選択した場合
        self.direction_mannual_move = 3



    def on_back_button_click(self):#「Back」のボタンを押した場合
        if  self.op_idx >= 1:
            prev_list = self.stack_move.pop()
            cells = self.define_cell(prev_list[3])
            Back(prev_list[0],prev_list[1],prev_list[2],prev_list[3],cells,self.start_board,self.goal_board)
            # self.back(prev_list[0],prev_list[1],prev_list[2],prev_list[3])
        else:
            self.error = 6
            self.Error()
            return
        self.error = 0
        self.Error()

        self.update()
        self.glwidget.update()



    def on_button_click(self):#Moveボタンが押されたときの処理
        if  (self.xtext.text() is None) or (self.ytext.text() is None) or (self.direction_mannual_move == -1) or (self.xtext.text() == "") or (self.ytext.text()=="") or (self.cells_number.text() == "") or (self.cells_number.text() == None):
            self.error = 4
            self.Error()
            print("入力してください")
            return
        try:#x座標,y座標は数字になっているか
            x = int(self.xtext.text())
            y = int(self.ytext.text())
            p = int(self.cells_number.text())
        except ValueError:
            self.error = 5
            self.Error()
            print('値が有効ではありません')
            return
        self.update()
        self.glwidget.update()

        cells = self.define_cell(int(self.xtext.text()), int(self.ytext.text()), int(self.cells_number))
        cells_y = len(cells)
        cells_x = len(cells[0])
        s = self.direction_mannual_move

        if  0 <= x+cells_x and x+cells_x < len(self.start_board):
            if 0<= y+cells_y and y+cells_y < len(self.start_board):
                Move(x,y,s,cells,self.start_board,self.goal_board)
                self.stack_move.append(x, y, s, p)
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
            self.error_label.setText("指定したx座標が範囲外です。x座標または辺の長さを変更してください")
        elif self.error == 2:
            self.error_label.setText("指定したy座標が範囲外です")
        elif self.error == 3:
            self.error_label.setText("方向が指定できていません 上、下、左、右のどちらかを指定してください。y座標または辺の長さを変更してください")
        elif self.error == 4:
            self.error_label.setText("入力してください")
        elif self.error == 5:
            self.error_label.setText("入力した値が数字ではありません")
        elif self.error == 6:
            self.error_label.setText("これ以上戻せません")

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
        elif(self.args[3] == "m"):
            self.painter_text.setText(f'{self.op_idx}手目 ')
        if not(self.op_idx >= self.answer["n"]):
            painter.drawText(action_text_point,f'座標: x:{x}y:{y} 次の行動: {self.dict_action[s]} にずらす')
        painter.setPen(QColor("red"))
        if self.args[3] == "m":

            try:#x座標,y座標は数字になっているか
                self.glwidget.xtext_int = int(self.xtext.text())
                self.glwidget.ytext_int = int(self.ytext.text())
            except ValueError:
                pass
            if self.direction_button_up.isChecked():
                self.glwidget.yazirusi = "v"
            elif self.direction_button_down.isChecked():
                self.glwidget.yazirusi = "^"
            elif self.direction_button_left.isChecked():
                self.glwidget.yazirusi = "->"
            elif self.direction_button_right.isChecked():
                self.glwidget.yazirusi = "<-"
            self.glwidget.update()
        elif self.args[3] == "a":
            pass



        painter.setBrush(QColor("white"))

        font = painter.font()











    def onSliderChange(self, value):
        self.applyOn(value)








    def mousePressEvent(self, event: QMouseEvent):#マウスを押した座標を取得
        x = event.position().x()
        y = event.position().y()
        if y > 460:
            self.releaseKeyboard()
        else:
            self.grabKeyboard()
        self.update()
        # self.glwidget.update()


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

        elif event.key() == Qt.Key.Key_A:#Aキーが押された場合
                self.ZoomController(2)

        elif event.key() == Qt.Key.Key_S:#Sキーが押された場合
                self.ZoomController(3)

        elif  event.key() == Qt.Key.Key_D:#Dキーが押された場合
                self.ZoomController(4)

        elif event.key() == Qt.Key.Key_Up:#UPキーが押された場合
                self.ZoomController(5)

        elif event.key() == Qt.Key.Key_Down:#Downキーが押された場合
                self.ZoomController(6)

        elif event.key() == Qt.Key.Key_R:#Rキーが押された場合
                self.ZoomController(7)

        elif event.key() == Qt.Key.Key_E:#Eキーが押された場合
                self.ZoomController(8)





    def ZoomController(self, num):#クリックしたキーごとに処理を実行する
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

    def applyOn(self, idx):
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

    def define_cell(self, p):
        cell_type = 0
        cell_size = 0
        if p in self.fixed_form_numbers:
            try:
                cells = [[ int(self.fixed_form_cells[p][i][j])for j in range(len(self.fixed_form_cells[p][i]))] for i in range(len(self.fixed_form_cells[p]))]
            except TypeError:
                print("無効な要素が入っています")
                return 0
            cell_size
        else:
            if p == 0:
                cell_type = 1
                cell_size = 1

            else:
                cell_type = int((p-1)%3+1)
                cell_size = 2**(((int((p-1)/3)))+1)
            cells = [[ 0 for _ in range(cell_size) ] for _ in range(cell_size)]

            for i in range(cell_size):
                for j in range(cell_size):
                    if cell_type == 1:
                        cells[i][j] = 1
                    elif cell_type == 2:
                        if i % 2 == 0:
                            cells[i][j] = 1
                    elif cell_type == 3:
                        if j % 2 == 0:
                            cells[i][j] = 1


        pre_start = [[ self.start_board[i][j]  for j in range(0,len(self.start_board[i]))] for i in range(0,len(self.start_board))]

        return cells
    #一手進める
    def apply_forward(self):

        p = self.answer["ops"][self.op_idx]["p"]
        x = self.answer["ops"][self.op_idx]["x"]
        y = self.answer["ops"][self.op_idx]["y"]
        s = self.answer["ops"][self.op_idx]["s"]
        cells = self.define_cell(p)
        Move(x, y, s, cells, self.start_board, self.goal_board)
        self.op_idx+=1


    #一手戻る
    def apply_backward(self):
        p = self.answer["ops"][self.op_idx-1]["p"]
        x = self.answer["ops"][self.op_idx-1]["x"]
        y = self.answer["ops"][self.op_idx-1]["y"]
        s = self.answer["ops"][self.op_idx-1]["s"]
        cells = self.define_cell(p)
        Back(x,y,s,p,cells,self.start_board,self.goal_board)

        self.op_idx -= 1





    #タイマーを開始させる
    def start_play(self):
        #qTimerを作る
        self.timer.start()
    def button_push():
        pass

    def resizeEvent(self, event):
        self.glwidget.resize(int((self.width()*2/3)/2-40), int((self.width()*2/3)/2-40))
        self.glwidget_goal.resize(int((self.width()*2/3)/2-40),int((self.width()*2/3)/2-40))


        super().resizeEvent(event)

    def closeEvent(self, event):
        self.config.save()


    def get(self):
        get = Get()
        problem = get.response_text



    def post(self):
        Post("answer.json")

    def reset():
        pass
