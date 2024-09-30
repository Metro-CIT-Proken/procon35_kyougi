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



class MainWidget(QWidget):
    def __init__(self,parent=None):
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

        # self.setMinimumSize(100, 100)
        # self.setMaximumSize(1000, 1000)
        # self.resize(1000, 1000)
        # self.grabKeyboard()

        self.fixed_form_num =  self.problem['general']['n']
        self.fixed_form_numbers = [ self.problem['general']['patterns'][x]['p'] for x in range(self.fixed_form_num)]
        self.fixed_form_widths = { self.fixed_form_numbers[x] : self.problem['general']['patterns'][x]['width'] for x in range(self.fixed_form_num)}
        self.fixed_form_heights = {self.fixed_form_numbers[x] : self.problem['general']['patterns'][x]['height'] for x in range(self.fixed_form_num)}
        self.fixed_form_cells = {self.fixed_form_numbers[x] : [ [self.problem['general']['patterns'][x]['cells'][i][j] for j in range(len(self.problem['general']['patterns'][x]['cells'][i]))]for i in range(len(self.problem['general']['patterns'][x]['cells'])) ]  for x in range(self.fixed_form_num)}
        print(f"fixed_form_cells types: {type(self.fixed_form_cells)}")
        print(f"numbers: {self.fixed_form_numbers}")
        print(f"widths: {self.fixed_form_widths}")
        print(f'heights: {self.fixed_form_heights}')
        print(f'cells: {self.fixed_form_cells}')
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
        layout.addLayout(layout_cont,1)
        # layout.addLayout(layout_gl,2)
        layout.addLayout(layout_gl,2)


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
        layout_cont.addWidget(self.painter_text)
        self.error_label = QLabel("")
        fournflag = False

        try:
                self.args[4]
        except IndexError:
                self.args.append("")
                fournflag = True
        if(self.args[3] == "m"):
            self.ytext = QLineEdit(self)#入力フォームを追加(y座標)
            self.xtext  = QLineEdit(self)#入力フォームを追加(x座標)
            self.nukigata_hen = QLineEdit(self)
            self.cell_type_line = QLineEdit(self)

            try:#x座標,y座標は数字になっているか
                int(self.xtext.text())
                int(self.ytext.text())
            except ValueError:
                check_int = False
                if  not((self.xtext.text() is None) or (self.ytext.text() is None) or (self.direction_mannual_move == 0) or (self.xtext.text() == "") or (self.ytext.text()=="")):
                    self.error = 5
                    self.Error()

            if check_int and (int(self.xtext.text()) >= 0 ) and int(self.ytext.text()) >= 0 and int(self.ytext.text()) < self.b_hei and int(self.xtext.text()) < self.b_wid and not(self.args[4] == 's'):
                self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,int(self.xtext.text()),int(self.ytext.text()),None,self)#操作盤面
            if check_int and (int(self.xtext.text()) >= 0 ) and int(self.ytext.text()) >= 0 and int(self.ytext.text()) < self.b_hei and int(self.xtext.text()) < self.b_wid and self.args[4] == 's':
                self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,int(self.xtext.text()),int(self.ytext.text()),fournflag,self)
            else:
                if fournflag and not(self.args[4] == 's'):
                    self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,None,None,None,self)#操作盤面
                else:
                    self.glwidget= OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,None,None,fournflag,self)

        elif(self.args[3] == "a"):
            if self.args[4] == 's':
                self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,None,None,fournflag,self)
            else:
                self.glwidget = OpenGLWidget(self.start_board,self.goal_board,self.zoom,self.zoom_direction,None,None,None,self)#操作盤面



        self.glwidget_goal = OpenGLWidget(self.goal_board,[[ -1 for x in range(self.b_wid)]for y in range(self.b_hei)],self.zoom,self.zoom_direction,self)#目的の盤面



        scroll_area = ScrollWidget(self.glwidget,self.glwidget_goal)


        layout_gl.addWidget(scroll_area)

        self.error = 0
        if self.args[3] == "a":#自動で移動する場合
            self.slider = QSlider(Qt.Orientation.Horizontal)
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.answer["n"])
            self.slider.setTickInterval(1)
            self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            self.slider.valueChanged.connect(self.onSliderChange)
            layout_cont.addWidget(self.slider)
        elif self.args[3] == "m":#手動モードの場合
            # direction_button_layout = QHBoxLayout(self)
            # text_layout = QVBoxLayout(self)
            # layout_cont.addLayout(direction_button_layout)
            # layout_cont.addLayout(text_layout)
            # self.stext  = QLineEdit(self)
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

            self.nukigata_hen_label = QLabel("抜き型の辺の長さ")
            self.nukigata_hen_label.setFixedSize(50,20)
            layout_text2.addWidget(self.nukigata_hen_label)
            layout_text2.addWidget(self.nukigata_hen)

            self.cell_type_label = QLabel("セルのタイプ")
            self.cell_type_label.setFixedSize(50,20)
            layout_text2.addWidget(self.cell_type_label)
            layout_text2.addWidget(self.cell_type_line)


            layout_action = QHBoxLayout()
            layout_cont.addLayout(layout_action)
            self.button = QPushButton('Move')#動かす処理を実行するボタンを追加

            layout_action.addWidget(self.button)
            self.button.clicked.connect(self.on_button_click)
            self.back_button = QPushButton('Back')
            layout_action.addWidget(self.back_button)
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
        if  (self.xtext.text() is None) or (self.ytext.text() is None) or (self.direction_mannual_move == 0) or (self.xtext.text() == "") or (self.ytext.text()=="") or (self.nukigata_hen.text() == "") or (self.nukigata_hen.text() == None):
            self.error = 4
            self.Error()
            print("入力してください")
            return
        try:#x座標,y座標は数字になっているか
            int(self.xtext.text())
            int(self.ytext.text())
            int(self.nukigata_hen.text())
            int(self.cell_type_line.text())
        except ValueError:
            self.error = 5
            self.Error()
            print('値が有効ではありません')
            return
        self.update()
        self.glwidget.update()




        if (0 <= int(self.xtext.text()) + int(self.nukigata_hen.text()) and int(self.xtext.text()) < self.b_wid):#x座標が範囲外の場合

                if (0 <= int(self.ytext.text()) + int(self.nukigata_hen.text()) and int(self.ytext.text()) < self.b_hei ):#y座標が範囲外の場合
                    self.move(int(self.xtext.text()),int(self.ytext.text()),self.direction_mannual_move-1,self.nukigata_hen.text(),self.cell_type_line)#入力したx座標,y座標,方向を盤面を動かす関数に送る
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











    def onSliderChange(self,value):
        self.applyOn(value)








    def mousePressEvent(self,event: QMouseEvent):#マウスを押した座標を取得
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





    def ZoomController(self,num):#クリックしたキーごとに処理を実行する
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
        print(f"idx: {idx}")

        if idx > self.op_idx:#未来を指定した場合
            for i in range(0,idx-self.op_idx):
                self.apply_forward()
        else:#過去を指定した場合
            for i in range(0,self.op_idx-idx):
                self.apply_backward()
        self.op_idx == idx
        self.update()
        self.glwidget.update()

    def define_cell(self,x,y,s,p):
        cell_type = 0
        cell_size = 0
        if p in self.fixed_form_numbers:
            cells = self.fixed_form_cells[p]
            print(f"tokusyucells:{cells}")
            print(f"typetokusyucells:{type(cells)}")
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

        print(f"{self.op_idx}手目")
        print(f"x:{x}")
        print(f"y:{y}")
        print(f"s:{s}")
        print(f"p:{p}")
        print(f"cell_size: {cell_size}")
        print(f"cell_type: {cell_type}")
        print(f"cells:")
        for i in range(len(cells)):
            print(cells[i])
        return cells
    #一手進める
    def apply_forward(self):

        p = self.answer["ops"][self.op_idx]["p"]
        x = self.answer["ops"][self.op_idx]["x"]
        y = self.answer["ops"][self.op_idx]["y"]
        s = self.answer["ops"][self.op_idx]["s"]
        cells = self.define_cell(x,y,s,p)
        self.move(x,y,s,cells)







    def move(self,x,y,s,cells):#ボードを変更する
        count = 0
        first_board = []
        if s == 0:
            for a in range(len(cells[0])):
                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    first_board = [row[x+a] for row in self.start_board]
                for b in range(len(cells)):
                    count+=1
                    print(f"a: {a},b: {b}")
                    if cells[b][a] == 1:
                        if not(y + b < 0 or x + a < 0 or y+b >= len(self.start_board) or x+a >= len(self.start_board[0])):
                            self.basic_move(x,y,s,a,b,cells)

                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    print(f"{self.op_idx}手目")
                    print(f"x:{x}")
                    print(f"y:{y}")
                    print(f"s:{s}")
                    print(f"cells:")
                    for i in range(len(cells)):
                        print(cells[i])
                    print(f"{a}列目")
                    print("手最初")
                    print(first_board)
                    print("手最後")
                    print([row[x+a] for row in self.start_board])

        elif s == 1:
            for a in range(len(cells[0])):
                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    first_board = [row[x+a] for row in self.start_board]
                for b in range(len(cells)-1,-1,-1):
                    count+=1
                    print(f"a: {a},b: {b}")
                    if cells[b][a] == 1:
                        if not(y + b < 0 or x + a < 0 or y+b >= len(self.start_board) or x+a >= len(self.start_board[0])):
                            self.basic_move(x,y,s,a,b,cells)

                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    print(f"{self.op_idx}手目")
                    print(f"x:{x}")
                    print(f"y:{y}")
                    print(f"s:{s}")
                    print(f"cells:")
                    for i in range(len(cells)):
                        print(cells[i])
                    print(f"{a}列目")
                    print("手最初")
                    print(first_board)
                    print("手最後")
                    print([row[x+a] for row in self.start_board])
        elif s == 2:
            for a in range(len(cells)):
                if not(  y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    first_board = [i for i in self.start_board[y+a]]
                for b in range(len(cells[0])):
                    count+=1
                    print(f"a: {a},b: {b}")
                    if cells[a][b] == 1:
                        if  not(y + a < 0 or x + b < 0 or y+a >= len(self.start_board) or x+b >= len(self.start_board[0])):#抜き型が場外
                            self.basic_move(x,y,s,a,b,cells)

                if not(  y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    print(f"{self.op_idx}手目")
                    print(f"x:{x}")
                    print(f"y:{y}")
                    print(f"s:{s}")
                    print(f"cells:")
                    for i in range(len(cells)):
                        print(cells[i])
                    print(f"{a}行目")
                    print("手最初")
                    print(first_board)
                    print("手最終")
                    print(self.start_board[y+a])

        elif s == 3:
            for a in range(len(cells)):
                # one_count= -1
                if  not(y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    first_board = [i for i in self.start_board[y+a]]
                for b in range(len(cells[0])-1,-1,-1):
                    count+=1
                    print(f"a: {a},b: {b}")
                    if cells[a][b] == 1:
                        if  not(y + a < 0 or x + b < 0 or y+a >= len(self.start_board) or x+b >= len(self.start_board[0])):#抜き型が場外
                            self.basic_move(x,y,s,a,b,cells)

                if  not(y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    print(f"{self.op_idx}手目")
                    print(f"x:{x}")
                    print(f"y:{y}")
                    print(f"s:{s}")
                    print(f"cells:")
                    for i in range(len(cells)):
                        print(cells[i])
                    print(f"{a}行目")
                    print("手最初")
                    print(first_board)
                    print("手最終")
                    print(self.start_board[y+a])
        print(count)

        if self.goal_board == self.start_board:
            print("=========================== GOAL!!! ==================")

        self.op_idx += 1


    def basic_move(self,x,y,s,a,b,cells):
            print("basic_move")
            true_count = 0
            remove = 0
            pre_x = -1 #座標を保存するための変数
            pre_y = -1
            first_board = []


            if s == 0:


                print("最初")
                print(first_board)
                for i in range(y+b,len(self.start_board)-1):#動かそうとしているますの座標〜下端
                    # print(f"s:{s} i:{i} remove:{remove}")
                    print(f"i: {i}")
                    if i-y+1 >= 0 and i-y+1 < len(cells):
                        if cells[i-y+1][a] == 1:
                            print(f"i-y+1: {i-y+1}")
                            # remove+=1
                            if pre_y == -1:
                                pre_y = i #前に動かす予定のますがあったら移動しない今動かそうとしているますの座標を保存する
                                print(f"s:{s} i:{i} pre_x: {pre_x} pre_y: {pre_y}")


                        else:
                            # self.start_board[i][x+a],self.start_board[i+1+remove][x+a] = self.start_board[i+1+remove][x+a],self.start_board[i][x+a]#上方向にずらす
                            if pre_y != -1:
                                self.start_board[pre_y][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[pre_y][x+a]#上方向にずらす#保存していた座標と交換する
                                print(f"move_pre!: {pre_y}, {i+1}")
                                print([row[x+a] for row in self.start_board])
                                pre_y = -1
                            else:
                                # pre_y = -1
                                self.start_board[i][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[i][x+a]#上方向にずらす#座標が保存されず抜き型内で移動をする場合
                                print(f"move_in!")
                                print([row[x+a] for row in self.start_board])
                            # remove = 0
                    # remove = 0
                    # pre_y = -1
                    else:
                        if pre_y != -1:
                            self.start_board[pre_y][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[pre_y][x+a]#上方向にずらす#保存していた座標と交換する
                            print(f"move_in_pre!: {pre_y}, {i+1}")
                            print([row[x+a] for row in self.start_board])
                            pre_y = -1

                        else:
                            self.start_board[i][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[i][x+a]#上方向にずらす#抜き型外で移動を行う場合い
                            print([row[x+a] for row in self.start_board])
                            print(f"move!")
                print("最初")
                print(first_board)
                print("最終")
                print([row[x+a] for row in self.start_board])

            elif s == 1:

                first_board = [row[x+a] for row in self.start_board]
                print("最初")
                print(first_board)
                for i in range(y+b,0,-1):
                    print(f"i: {i}")
                    if i-y-1 >= 0 and i-y-1 < len(cells):
                        if cells[i-y-1][a] == 1:
                            print(f"i-y-1: {i-y-1}")
                            if pre_y == -1:
                                pre_y = i
                                print(f"s:{s} i:{i} pre_x: {pre_x} pre_y: {pre_y}")
                            # remove-=1
                        else:
                            # self.start_board[i][x+a],self.start_board[i-1+remove][x+a] = self.start_board[i-1+remove][x+a],self.start_board[i][x+a]
                            if pre_y != -1:
                                self.start_board[i-1][x+a],self.start_board[pre_y][x+a] = self.start_board[pre_y][x+a],self.start_board[i-1][x+a]
                                print(f"move_pre!: {pre_y}, {i-1}")
                                print([row[x+a] for row in self.start_board])
                                pre_y = -1
                            else:
                                # pre_y = -1
                                self.start_board[i][x+a],self.start_board[i-1][x+a] = self.start_board[i-1][x+a],self.start_board[i][x+a]
                                print("move!_in")
                                print([row[x+a] for row in self.start_board])
                            # remove = 0
                    else:
                        if pre_y != -1:
                            self.start_board[i-1][x+a],self.start_board[pre_y][x+a] = self.start_board[pre_y][x+a],self.start_board[i-1][x+a]
                            (f"move_pre_in!: {pre_y}, {i-1}")
                            pre_y = -1
                            print([row[x+a] for row in self.start_board])
                        else:
                            self.start_board[i][x+a],self.start_board[i-1][x+a] = self.start_board[i-1][x+a],self.start_board[i][x+a]
                            print("move!")
                            print([row[x+a] for row in self.start_board])
                print("最初")
                print(first_board)
                print("最終")
                print([row[x+a] for row in self.start_board])

            elif s == 2:
                first_board = [i for i in self.start_board[y+a]]
                print("最初")
                print(first_board)
                for i in range(x+b,len(self.start_board[0])-1):
                    print(f"i: {i}")
                    if i-x+1 >= 0 and i-x+1 < len(cells[0]):
                        if cells[a][i-x+1] == 1:
                            print(f"i-x+1: {i-x+1}")
                            if pre_x == -1:
                                pre_x = i
                                print(f"s:{s} i:{i} pre_x: {pre_x} pre_y: {pre_y}")
                        else:
                            if pre_x != -1:
                                self.start_board[y+a][pre_x],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][pre_x]#左方向にずらす
                                print(f"move_pre!: {pre_x} {i+1}")
                                print(self.start_board[y+a])
                                pre_x = -1

                            else:
                                self.start_board[y+a][i],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][i]#左方向にずらす
                                print("move_in!")
                                print(self.start_board[y+a])
                    else:
                        if  pre_x != -1:
                            self.start_board[y+a][pre_x],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][pre_x]
                            print(f"move_pre_in!: {pre_x} {i+1}")
                            print(self.start_board[y+a])
                            pre_x = -1
                        else:
                            self.start_board[y+a][i],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][i]#左方向にずらす
                            print(self.start_board[y+a])
                        print("move!")
                print("最初")
                print(first_board)
                print("最終")
                print(self.start_board[y+a])

            elif s == 3:
                first_board = [i for i in self.start_board[y+a]]
                print("最初")
                print(first_board)
                for i in range(x+b,0,-1):
                    print(f"i: {i}")
                    if i-x-1 >= 0 and i-x-1 < len(cells[0]):
                        if cells[a][i-x-1] == 1:
                            print(f"i-x-1: {i-x-1}")
                            if pre_x == -1:
                                pre_x = i
                                print(f"s:{s} i:{i} pre_x: {pre_x} pre_y: {pre_y}")
                        else:
                            if pre_x != -1:
                                self.start_board[y+a][pre_x],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][pre_x]
                                print(f"move_pre!: {pre_x} {i-1}")
                                print(self.start_board[y+a])
                                pre_x = -1
                            else:
                                # pre_x = -1
                                self.start_board[y+a][i],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][i]#右方向にずらす
                                print("move_in!")
                                print(self.start_board[y+a])

                    else:
                        if pre_x != -1:
                            self.start_board[y+a][pre_x],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][pre_x]
                            print(f"move_pre_in!: {pre_x} {i-1}")
                            print(self.start_board[y+a])
                            pre_x = -1

                        else:
                            self.start_board[y+a][i],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][i]#右方向にずらす
                            print("move!")
                            print(self.start_board[y+a])
                print("最初")
                print(first_board)
                print("最終")
                print(self.start_board[y+a])


    #一手戻る
    def apply_backward(self):
        p = self.answer["ops"][self.op_idx-1]["p"]
        x = self.answer["ops"][self.op_idx-1]["x"]
        y = self.answer["ops"][self.op_idx-1]["y"]
        s = self.answer["ops"][self.op_idx-1]["s"]
        cells = self.define_cell(x,y,s,p)
        print("apply_backward")
        print(f"op_idx {self.op_idx}")
        self.back(x,y,s,p,cells)


    def back(self,x,y,s,p,cells):
        print("back")
        pre_start = [[ self.start_board[i][j]  for j in range(0,len(self.start_board[i]))] for i in range(0,len(self.start_board))]
        first_board = []
        one_counts = {}
        one_index_dic = {}
        one_index_list = []
        if s == 0 or s==1:
            for j in range(len(cells[0])):
                one_count = 0
                one_index_list = []
                for i in range(len(cells)):
                    if cells[i][j] == 1:
                        if  not(y + i < 0 or x + j < 0 or y+i >= len(self.start_board) or x+j >= len(self.start_board[0])):#抜き型が場外
                            one_count+=1
                            one_index_list.append(i+y)
                one_counts[j+x] = one_count
                one_index_dic[j+x] = one_index_list

        elif s == 2 or s == 3:
            for i in range(len(cells)):
                one_count = 0
                one_index_list = []
                for j in range(len(cells[0])):
                    if cells[i][j] == 1:
                        if  not(y + i < 0 or x + j < 0 or y+i >= len(self.start_board) or x+j >= len(self.start_board[0])):#抜き型が場外
                            one_count+=1
                            one_index_list.append(j+x)
                one_counts[i+y] = one_count
                one_index_dic[i+y] = one_index_list
        if s == 1 or s == 3:
            one_index_list.reverse

        counts = 0
        if s == 0:
            print("s=0")
            for j in range(x,x+len(cells[0])):
                print(f"j:{j}")
                counts = one_counts[j]
                # first_board = [row[j] for row in self.start_board]
                for i in range(y,y+len(cells)):
                    print(f"j:{j} i:{i}")
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            print(f"i-y {i-y} j-x {j-x}")
                            if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                counts-=1


        elif s == 1:
            print("s=1")
            for j in range(x,x+len(cells[0])):
                print(f"i:{i}")
                counts = one_counts[j]
                first_board = [row[i][j] for row in self.start_board]
                # if j in one_counts:
                for i in range(y+len(cells),y,-1):
                    print(f"j:{j} i:{i}")
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            print(f"i-y {i-y} j-x {j-x}")
                            if cells[i-y][j-x] == 1:
                            # if i >= 0 and i < len(cells) and j >= 0 and j < len(cells[0]):
                            #     if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                counts-=1

        elif s == 2:
            print("s=2")
            for i in range(y,y+len(cells)):
                print(f"i:{i}")
                # if i in one_counts:
                print(f"back x start {x}")
                print(f"back x end {x+len(cells[0])}")
                print(f"back start: {y}")
                print(f"back end: {y+len(cells)}")
                counts = one_counts[i]
                if i >= 0 and i < len(self.start_board):
                    first_board = [ retu for retu in self.start_board[i]]
                # for j in range(len(self.start_board[0])-one_counts[i],len(self.start_board)):
                for j in range(x,x+len(cells[0])):
                        print(f"j:{j} i:{i}")
                        if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                            if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                                print(f"i-y {i-y} j-x {j-x}")
                                if cells[i-y][j-x] == 1:
                            # if i-y >= 0 and i-y < len(cells) and one_index_dic[i]-x >= 0 and one_index_dic[i]-x < len(cells[0]):
                            #     print("safe")
                            #     if cells[i-y][one_index_dic[i]-x] == 1:
                                    self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                    counts-=1
                print("最初")
                print(first_board)
                print("最後")
                if i >= 0 and i < len(self.start_board):
                    print([ retu for retu in self.start_board[i]])


        elif s == 3:
            print("s=3")
            for i in range(y,y+len(cells)):
                print(f"i:{i}")
                # if i in one_counts:
                # for j in range(one_counts[i]-1,-1,-1):
                print(f"back x start {x+len(cells[0])-1}")
                print(f"back x end {x-2}")
                print(f"back y start: {y}")
                print(f"back y end: {y+len(cells)}")
                counts = one_counts[i]
                if i >= 0 and i < len(self.start_board):
                    first_board = [ retu for retu in self.start_board[i]]
                for j in range(x+len(cells[0])-1,x-1,-1):
                    print(f"j:{j} i:{i}")
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        print(f"i-y {i-y} j-x {j-x}")
                        print("bbbbbbbbbbbbbbbbbbbbbbb")
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            print(f"i-y {i-y} j-x {j-x}")
                            if cells[i-y][j-x] == 1:
                            # if i >= 0 and i < len(cells) and one_index_dic[i]-x >= 0 and one_index_dic[i]-x < len(cells[0]):
                            #     if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_dic,i,j,counts)
                                counts-=1
                print("最初")
                print(first_board)
                print("最後")
                if i >= 0 and i < len(self.start_board):
                    print([ retu for retu in self.start_board[i]])

        print(f"s: {s}")
        print("cells:")
        for i in range(len(cells)):
            print(cells[i])

        print("変更前")
        for i in range(len(pre_start)):
            print()
            for j in range(len(pre_start[0])):
                if (i >= y and j >= x) and (i < y+len(cells) and j < x+len(cells[0])):
                    print(colored(str(pre_start[i][j])+'*', "red"),end=" ")
                else:
                    print(str(pre_start[i][j])+'+',end=" ")
        print()
        print("変更後")
        for i in range(len(self.start_board)):
            print()
            for j in range(len(self.start_board[0])):
                if (i >= y and j >= x) and (i < y+len(cells) and j < x+len(cells[0])):
                    print(colored(str(self.start_board[i][j])+'*', "red"),end=" ")
                else:
                    print(str(self.start_board[i][j])+'+',end=" ")
        print()
        self.op_idx -= 1




    def basic_back(self,x,y,s,p,cells,one_counts,one_index_dic:dict,i,j,counts):
        print("basic_back")
        print(f"basic_back:  i {i},j {j}")
        print(f"counts: {counts}")


        if s == 0:
            print(f"start: {len(self.start_board)-1-counts} end: {i+1}")
            for a in range(len(self.start_board)-counts,i,-1):
                self.start_board[a][j],self.start_board[a-1][j] = self.start_board[a-1][j],self.start_board[a][j]
                print(f"move!:  {self.start_board[i]}")
        elif s== 1:
            print(f"start: {len(self.start_board)-1+counts} end: {i-1}")
            for a in range(counts-1,i-1):
                self.start_board[a][j],self.start_board[a+1][j] = self.start_board[a+1][j],self.start_board[a][j]
                print(f"move!:  {self.start_board[i]}")
        elif s == 2:
            print(f"直前 {self.start_board[i]}")
            print(f"start: {len(self.start_board[0])-counts} end: {j+1}")
            for a in range(len(self.start_board[0])-counts,j,-1):
                print(f"a: {a}")

                self.start_board[i][a],self.start_board[i][a-1] = self.start_board[i][a-1],self.start_board[i][a]
                print(f"move!: {a} & {a-1} :{self.start_board[i]}")
        elif s == 3:
            print(f"直前 {self.start_board[i]}")
            print(f"start: {counts-1} end: {j-2}")
            for a in range(counts-1,j):
                self.start_board[i][a],self.start_board[i][a+1] = self.start_board[i][a+1],self.start_board[i][a]
                print(f"move!: {a} & {a+1}: {self.start_board[i]}")




    #タイマーを開始させる
    def start_play(self):
        #qTimerを作る
        self.timer.start()
    def button_push():
        print("pushed! button")

    def resizeEvent(self,event):
        self.glwidget.resize(int((self.width()*2/3)/2-40), int((self.width()*2/3)/2-40))
        self.glwidget_goal.resize(int((self.width()*2/3)/2-40),int((self.width()*2/3)/2-40))

        print(f"GLWidget Size: {self.glwidget.width()} x {self.glwidget.height()}")
        print(f"GLgoalWidget Size {self.glwidget_goal.width()} x {self.glwidget_goal.height()}")
        print(f" Widget Size: {self.width()} x {self.height()}")

        super().resizeEvent(event)
