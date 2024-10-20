import sys

from gl import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from PyQt6.QtWidgets import *
from get_problem import *
from first_double_widget import *
from double_widget  import *
import json
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from scroll_widget import *
from exec_solver import *
from external_solver import *
import time



from move import *
from back import *
from config import *





class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        # self.time_label = QLabel()
        # # update = pyqtSignal(int)

        # self.time = QTimer(self)
        # self.time.timeout.connect(self.update_time)
        # self.timer = Timer()
        # self.timer_thread = QThread()
        # self.timer.moveToThread(self.timer_thread)
        # self.timer.update.connect()


        super().__init__(parent)
        self.args = sys.argv
        self.aflag = False
        self.sflag = False
        # try:
        #     arg2 = self.args[1]
        # except:
        #     print("引数が足りません")
        #     exit(1)
        # self.answers_list = [None,]
        # with open(self.args[1]) as f:
        #     answer = json.load(f)[]
        self.arg_list = [False,False]
        # for _ in range(1,5):
        #     self.answers_list.append(answer)
        self.answers_list = [None, ]
        for i in self.args:
            if i == "a":
                break
            if i  == "s":
                self.sflag = True


        try:
            arg = self.args[1]
            if not (self.args[1] == 'a' or self.args[1] == 's'):
                self.arg_list[0] = True
                with open(arg) as file:
                    self.problem = json.load(file)

        except:
            pass

        try:
            arg = self.args[2]
            if not (self.args[2] == 'a' or self.args[2] == 's'):
                self.arg_list[1] = True
                with open(arg) as file:
                    self.file_answer = json.load(file)
        except:
            pass






        self.container_layout = QVBoxLayout()
        self.container_widget = QWidget()
        self.one_get = False

        self.widgets_list = []
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.answer = {}
        self.index = 0

        self.start_widgets_list = []
        self.goal_widgets_list = []
        self.first_start_board = [[]]
        self.first_goal_board = [[]]
        self.zoom = 0
        self.zoom_direction = 0
        self.glwidget_info = {}

        layout = QHBoxLayout(self)
        layout_settings = QVBoxLayout()
        self.first_gl_layout = QHBoxLayout()
        layout_cont = QVBoxLayout()
        self.layout_gl = QHBoxLayout()



        layout.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(layout_settings, 1)
        layout_settings.addLayout(self.first_gl_layout)
        layout_settings.addLayout(layout_cont)
        layout.addLayout(self.layout_gl, 2)


        self.error_text = ""


        # self.dis_board = [[0 for x in range(self.b_wid)]for y in range(self.b_hei)]
        self.idx = 0

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
        self.dict_action = {0:"上", 1:"下", 2:"左", 3:"右"}
        self.dic_dir = ["上", "下", "左", "右"]
        check_int = True
        self.painter_text = QLabel("")
        self.painter_text.setFixedSize(200, 50)
        self.stack_move = [[]]




        layout_cont.addWidget(self.painter_text)
        self.error_label = QLabel("")
        # self.s_flag = True

        # try:
        #         self.args[3]
        # except IndexError:
        #         self.args.append("")
        #         self.s_flag = False


        # if(self.aflag):



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


        self.solver_layout = QVBoxLayout()
        self.add_solver_button = QPushButton("ソルバーを追加する")
        self.remove_solver_button = QPushButton("ソルバーを削除する")



        self.pc_address_layout = QVBoxLayout()

        self.add_pc_address_button = QPushButton("PCのアドレスを追加する")
        self.remove_pc_address_button = QPushButton("PCのアドレスを削除する")



        self.message = QLabel()
        self.message.setFixedSize(300,100)
        self.message.setWordWrap(True)




        self.scroll_area = ScrollWidget()


        self.layout_gl.addWidget(self.scroll_area)

        # self.scroll_area.scroll_area.verticalScrollBar().valueChanged.connect(self.update_gl_on_scroll)
        # self.scroll_area.scroll_area.horizontalScrollBar().valueChanged.connect(self.update_gl_on_scroll)
        self.error = 0
        # if self.args[2] == "a":#自動で移動する場合
        ip_address_label = QLabel("IPアドレス")
        ip_address_label.setFixedSize(100,20)

        port_label = QLabel("ポート番号")
        port_label.setFixedSize(100,20)

        token_label = QLabel("トークン")
        token_label.setFixedSize(100,20)

        layout_text = QVBoxLayout()
        layout_cont.addLayout(layout_text)
        # layout_text.addWidget(self.time_label)
        layout_text.addWidget(ip_address_label)
        layout_text.addWidget(self.ip_address_line)
        layout_text.addWidget(port_label)
        layout_text.addWidget(self.port_line)
        layout_text.addWidget(token_label)
        layout_text.addWidget(self.token_line)




        self.get_button.clicked.connect(self.get)

        self.add_solver_button.clicked.connect(self.add_solver)
        self.remove_solver_button.clicked.connect(self.remove_solver)

        self.add_pc_address_button.clicked.connect(self.add_pc_address)
        self.remove_pc_address_button.clicked.connect(self.remove_pc_address)


            # self.post_button.clicked.connect(self.post)

        layout_button = QHBoxLayout()
        layout_cont.addLayout(layout_button)

        layout_button.addWidget(self.get_button)
        layout_cont.addLayout(self.solver_layout)
        layout_cont.addWidget(self.add_solver_button)
        layout_cont.addWidget(self.remove_solver_button)

        layout_cont.addLayout(self.pc_address_layout)

        layout_cont.addWidget(self.add_pc_address_button)
        layout_cont.addWidget(self.remove_pc_address_button)



        layout_cont.addWidget(self.message)

        for solver in self.config.solvers:
            text_solver = QLineEdit(solver)
            self.solver_layout.addWidget(text_solver)

        print(self.config.pcs)
        for pc in self.config.pcs:
            pc_address_line_layout = QHBoxLayout()
            add_pc_address_check = QCheckBox()
            if pc["is-Check"]:
                add_pc_address_check.setChecked(True)
            add_pc_address_line = QLineEdit(pc["ip_address"])
            add_pc_solver_line = QLineEdit(pc["solver"])

            self.pc_address_layout.addLayout(pc_address_line_layout)
            pc_address_line_layout.addWidget(add_pc_address_check)
            pc_address_line_layout.addWidget(add_pc_address_line)
            pc_address_line_layout.addWidget(add_pc_solver_line)


            # layout_button.addWidget(self.post_button)

        if "answer" in self.glwidget_info  :
                self.slider = QSlider(Qt.Orientation.Horizontal)
                self.slider.setMinimum(0)
                self.slider.setMaximum(self.glwidget_info["answer"]["n"])
                self.slider.setTickInterval(1)
                self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
                self.slider.valueChanged.connect(self.onSliderChange)
                layout_cont.addWidget(self.slider)


    def mousePressEvent(self, event: QMouseEvent):#マウスを押した座標を取得
        x = event.position().x()
        y = event.position().y()
        if y > 460:
            self.releaseKeyboard()
        else:
            self.grabKeyboard()
        if not(self.widgets_list == []):
            self.glwidget_info = self.decide_focus_widget()

            self.glwidget = self.glwidget_info["start_widget"]

            self.glwidget_goal = self.glwidget_info["goal_widget"]

            self.double_widget = self.glwidget_info["double_widget"]

            self.op_idx = self.double_widget.op_idx

            self.answer = self.glwidget_info["answer"]

            self.answer_num = self.double_widget.answer_num
            self.dis_board = self.glwidget_info["dis_board"]
            self.board_width = self.glwidget_info["board_width"]
            # self.glwidget.update()
        # self.update()



    def keyPressEvent(self, event: QKeyEvent):
        # if self.args[2] == "a":

        if event.key() == Qt.Key.Key_Right and not(self.op_idx == self.answer_num):
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
            if self.glwidget_goal.is_focus:
                if self.glwidget_goal.zoomy*self.glwidget_goal.zoom+(self.glwidget_goal.zoom*2)+0.1  <=  2.0:#拡大する場合ZZZ
                    self.glwidget_goal.zoomy += 0.1
                    if self.glwidget_goal.zoom_direction >= 2:
                        self.glwidget_goal.zoom_direction -= 2
                else:
                    self.glwidget_goal.zoomy = 2/self.glwidget_goal.zoom-2
            if self.glwidget.is_focus:
                if self.glwidget.zoomy*self.glwidget.zoom+(self.glwidget.zoom*2)+0.1  <=  2.0:#拡大する場合ZZZ
                    self.glwidget.zoomy += 0.1
                    if self.glwidget.zoom_direction >= 2:
                        self.glwidget.zoom_direction -= 2
                else:
                    self.glwidget.zoomy = 2/self.glwidget.zoom-2
            # else:
            #     if self.glwidget.is_focus:
            #         self.glwidget.zoomy = 2/self.glwidget.zoom-2
            #     if self.glwidget_goal.is_focus:




        elif num == 2:
            if self.glwidget_goal.is_focus:
                if self.glwidget_goal.zoomx-0.1  >=  0:
                    self.glwidget_goal.zoomx -= 0.1
                    if self.glwidget_goal.zoom_direction % 2 == 1:
                        self.glwidget_goal.zoom_direction -= 1
                else:
                    self.glwidget_goal.zoomx = 0

            if self.glwidget.is_focus:
                if self.glwidget.zoomx-0.1  >=  0:
                    self.glwidget.zoomx -= 0.1
                    if self.glwidget.zoom_direction % 2 == 1:
                        self.glwidget.zoom_direction -= 1
                else:
                    self.glwidget.zoomx = 0


        elif num == 3:
            if self.glwidget_goal.is_focus:
                if self.glwidget_goal.zoomy-0.1  >=  0:
                    self.glwidget_goal.zoomy -= 0.1
                    if self.glwidget_goal.zoom_direction <= 2:
                        self.glwidget_goal.zoom_direction += 2
                else:
                    self.glwidget_goal.zoomy = 0

            if self.glwidget.is_focus:
                if self.glwidget.zoomy-0.1  >=  0:
                    self.glwidget.zoomy -= 0.1
                    if self.glwidget.zoom_direction <= 2:
                        self.glwidget.zoom_direction += 2
                else:
                    self.glwidget.zoomy = 0

        elif num == 4:
            if self.glwidget_goal.is_focus:
                if self.glwidget_goal.zoomx*self.glwidget_goal.zoom+(self.glwidget_goal.zoom*2)+0.1  <=  2.0 :
                    self.glwidget_goal.zoomx += 0.1
                    if self.glwidget_goal.zoom_direction % 2 == 0:
                        self.glwidget_goal.zoom_direction += 1
                else:
                    self.glwidget_goal.zoomx = 2/self.glwidget_goal.zoom-2

            if self.glwidget.is_focus:
                if self.glwidget.zoomx*self.glwidget.zoom+(self.glwidget.zoom*2)+0.1  <=  2.0 :
                    self.glwidget.zoomx += 0.1
                    if self.glwidget.zoom_direction % 2 == 0:
                        self.glwidget.zoom_direction += 1
                else:
                    self.glwidget.zoomx = 2/self.glwidget.zoom-2



        elif num == 5:
            if self.glwidget_goal.is_focus:
                if self.glwidget_goal.zoom >= 0.05 :
                    self.glwidget_goal.zoom /=2

            if self.glwidget.is_focus:
                if self.glwidget.zoom >= 0.05:
                    self.glwidget.zoom /=2
        elif num == 6:
            if self.glwidget_goal.is_focus:
                if self.glwidget_goal.zoom*2 <= 1:
                    self.glwidget_goal.zoom*=2
            if self.glwidget.is_focus:
                if self.glwidget.zoom*2 <= 1:
                    self.glwidget.zoom*=2

        elif num == 7:
            if self.glwidget_goal.is_focus:
                self.glwidget_goal.zoom = 1
                self.glwidget_goal.zoomx = 0
                self.glwidget_goal.zoomy = 0
            if self.glwidget.is_focus:
                self.glwidget.zoom = 1
                self.glwidget.zoomx = 0
                self.glwidget.zoomy = 0

        self.glwidget_goal.update()
        self.glwidget.update()

    #0.5秒ごとに進む・戻る
    def opTimerCallback(self):
        self.applyOn(self.op_idx+1)
        if self.op_idx == self.answer_num:
                self.timer.stop()

    def print_distance_board(self):
        self.dis_board = [[self.search_near_goal(x,y) for x in range(self.glwidget_info["board_width"])]for y in range(self.glwidget_info["board_width"])]

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
        return cells
    #一手進める
    def apply_forward(self):
        p = self.answer["ops"][self.op_idx]["p"]
        x = self.answer["ops"][self.op_idx]["x"]
        y = self.answer["ops"][self.op_idx]["y"]
        s = self.answer["ops"][self.op_idx]["s"]
        cells = self.define_cell(p)
        start_board = self.glwidget.board
        goal_board = self.glwidget.goal_board
        Move(x, y, s, cells, self.glwidget.board, self.glwidget.goal_board)
        self.glwidget.board = start_board
        self.op_idx+=1
        self.double_widget.op_idx+=1


    #一手戻る
    def apply_backward(self):
            p = self.answer["ops"][self.op_idx-1]["p"]
            x = self.answer["ops"][self.op_idx-1]["x"]
            y = self.answer["ops"][self.op_idx-1]["y"]
            s = self.answer["ops"][self.op_idx-1]["s"]
            cells = self.define_cell(p)
            start_board = self.glwidget.board
            goal_board = self.glwidget.goal_board
            Back(x,y,s,p,cells,start_board,goal_board)
            self.glwidget.board = start_board
            self.op_idx -= 1
            self.double_widget.op_idx-=1







    def resizeEvent(self, event):
        if self.widgets_list != []:
            if "start_board" in self.widgets_list[0]:
                if  not(self.widgets_list[0]["start_widget"] == self.glwidget):
                        try:
                            self.glwidget.resize(int((self.width()*2/3)/2-40), int((self.width()*2/3)/2-40))
                            self.glwidget_goal.resize(int((self.width()*2/3)/2-40), int((self.width()*2/3)/2-40))
                            try:
                                self.double_widget.resize(self.glwidget.size().width()*2+50, self.glwidget.size().height())
                            except NameError:
                                pass
                        except AttributeError:
                            pass


        super().resizeEvent(event)

    def closeEvent(self, event):
        for i in range(self.solver_layout.count()):
            item = self.solver_layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QLineEdit):
                self.config.solvers[i] = item.widget().text()

        for i in range(self.pc_address_layout.count()):
            last_pc_address_line = self.pc_address_layout.itemAt(i)
            layout = last_pc_address_line.layout()
            check_item = layout.itemAt(0)
            check_widget = check_item.widget()
            pc_address_item = layout.itemAt(1)
            pc_address_widget = pc_address_item.widget()
            pc_solver_item = layout.itemAt(2)
            pc_solver_widget = pc_solver_item.widget()
            self.config.pcs[i]["is-Check"] = check_widget.isChecked()
            self.config.pcs[i]["ip_address"] = pc_address_widget.text()
            self.config.pcs[i]["solver"] = pc_solver_widget.text()


        self.config.save()

    def on_answer_created(self, answer):
        print("on_answer_created")
        print(answer)
        self.answers_list.append(answer)
        self.on_answer_added()
        return answer

    def get(self):
        # if not(self.one_get):
            if self.arg_list[0]:
                self.get_pro = GetByHand(self.problem)
                print("hand problem")
                print(self.get_pro.problem)
            else:
                self.get_pro = Get(self.config)

            if self.get_pro.status_code== 200 or self.get_pro.status_code == 100:
                self.answers_list = [None, ]
                if self.arg_list[1]:
                    self.on_answer_created(self.file_answer)
                else:

                        for i in range(self.pc_address_layout.count()):

                            last_pc_address_line = self.pc_address_layout.itemAt(i)
                            layout = last_pc_address_line.layout()
                            check_item = layout.itemAt(0)
                            check_widget = check_item.widget()
                            if check_widget.isChecked():
                                pc_address_item = layout.itemAt(1)
                                pc_address_widget = pc_address_item.widget()
                                pc_solver_item = layout.itemAt(2)
                                pc_solver_widget = pc_solver_item.widget()

                                external_solver = ExternalSolver(pc_address_widget.text(), pc_solver_widget.text(),self.get_pro.problem)
                                external_solver.solve(self.on_answer_created)

                        for i in range(self.solver_layout.count()):
                            item = self.solver_layout.itemAt(i)
                            if item.widget() and isinstance(item.widget(), QLineEdit):
                                # self.config.solvers.append(item.widget().text())
                                if not(item.widget().text() == ""):
                                    answer_exec = Exec(self.get_pro.problem, item.widget().text())
                                    answer = answer_exec.exe_cpp(self.on_answer_created)

                if self.get_pro.status_code == 200:
                    self.message.setText("取得成功です")
                elif  self.get_pro.status_code == 100:
                    self.message.setText("ソルバー取得成功")
                if self.one_get:
                    for widget in self.widgets_list:
                        self.scroll_area.scroll_area_layout.removeWidget(widget["double_widget"])
                        widget["double_widget"].deleteLater()
                    self.widgets_list = []

                op_idx = 0
                print("status 200")
                self.widgets_list.append({})
                zoom = 1
                self.widgets_list[0]["zoom"] = zoom
                zoom_direction = 0
                self.widgets_list[0]["zoom_direction"] = zoom_direction

                start_board = [row[:] for row in self.get_pro.start_board]




                goal_board = [row[:] for row in self.get_pro.goal_board]

                b_wid = self.get_pro.board_width
                b_hei = self.get_pro.board_height

                self.widgets_list[0]["board_width"] = b_wid
                self.widgets_list[0]["board_height"] = b_hei


                dis_board = [[0 for _ in range(b_wid)]for _ in range(b_hei)]
                self.widgets_list[0]["dis_board"] = dis_board

                self.widgets_list[0]["answer"] = {
                                                        "n": 0,
                                                        "ops": [
                                                        ]
                                                }

                # self.widgets_list[0]["answer_num"] = self.widgets_list[0]["answer"]["n"]



                if start_board != [[]] or goal_board != [[]]:
                    # if not(self.s_flag):
                    #     first_start_gl = OpenGLWidget(start_board, goal_board, zoom, zoom_direction, None, None, None, self)
                    #     self.widgets_list[0]["start_widget"] = first_start_gl
                    # else:
                    first_start_gl = OpenGLWidget(start_board, goal_board, zoom, zoom_direction, None, None, self.sflag, self)
                    self.widgets_list[0]["start_widget"] = first_start_gl
                    first_goal_gl = OpenGLWidget(goal_board, [[ -1 for _ in range(b_wid)]for _ in range(b_hei)], zoom, zoom_direction, None, None, False, self)
                    self.widgets_list[0]["goal_widget"] = first_goal_gl
                    # self.widgets_list[0]

                    first_double_widget = FirstDoubleWidget(first_start_gl, first_goal_gl)
                    first_double_widget.op_idx = 0
                    self.widgets_list[0]["double_widget"] = first_double_widget
                    self.widgets_list[0]["double_widget"].answer_num = 0
                    self.answer_num = 0
                    self.first_gl_layout.addWidget(first_double_widget)

                self.glwidget = self.widgets_list[0]["start_widget"]
                self.glwidget_goal = self.widgets_list[0]["goal_widget"]
                self.double_widget = self.widgets_list[0]["double_widget"]
                    # self.op_idx = 0
                self.dis_board = self.widgets_list[0]["dis_board"]
                self.answer_num = self.widgets_list[0]["answer"]["n"]

                self.one_get = True


                self.container_widget.setLayout(self.container_layout)
                self.scroll_area.scroll_area.setWidget(self.container_widget)
                self.fixed_form_num = self.get_pro.fixed_form_num


                self.fixed_form_numbers = self.get_pro.fixed_form_numbers
                self.fixed_form_widths = self.get_pro.fixed_form_widths



                self.fixed_form_heights = self.get_pro.fixed_form_heights
                self.fixed_form_cells = self.get_pro.fixed_form_cells












            else:


                if self.get_pro.status_code == 400:
                    self.message.setText("Error 400: リクエストの内容が不十分です")
                    return
                elif self.get_pro.status_code == 401:
                    self.message.setText("Error 401: トークンが未取得もしくは不正です")
                    return

                elif self.get_pro.status_code == 403:
                    self.message.setText("Error 403: 競技時間外です")
                    return

                else:
                    if self.get_pro.error != "":
                        self.message.setText(f"Error: {self.get_pro.error}")
                        return



    def on_answer_added(self):
        # for i in range(len(self.widgets_list) - 1, len(self.answers_list) - 1):
        for i in range(len(self.widgets_list)-1,len(self.answers_list) - 1):
            self.widgets_list.append({})
            zoom = 1
            zoom_direction = 0

            self.widgets_list[i+1]["zoom"] = zoom
            self.widgets_list[i+1]["zoom_direction"] = zoom_direction


            self.op_idx = 0

            b_wid = self.get_pro.board_width
            self.widgets_list[i+1]["board_width"] = b_wid

            next_pos = b_wid*CELL_SIZE+100
            self.widgets_list[i+1]["next_pos"] = next_pos

            b_hei = self.get_pro.board_height
            self.widgets_list[i+1]["board_height"] = b_hei


            self.widgets_list[i+1]["answer"] = self.answers_list[i+1]


            dis_board = [[0 for _ in range(b_wid)]for _ in range(b_hei)]
            self.widgets_list[i+1]["dis_board"] = dis_board

            start_board = [row[:] for row in self.get_pro.start_board]
            self.widgets_list[i+1]["start_board"] = start_board

            goal_board =  [row[:] for row in self.get_pro.goal_board]
            self.widgets_list[i+1]["goal_board"] = goal_board



            start_gl_board = OpenGLWidget(start_board, goal_board, zoom, zoom_direction, None, None, self.sflag, self)
            self.widgets_list[i+1]["start_widget"] = start_gl_board
            start_gl_board.resize(int((self.width()*2/3)/2-40), int((self.width()*2/3)/2-40))
            # self.start_widgets_list.append(start_gl_board)
            goal_gl_board = OpenGLWidget(goal_board, [[ -1 for _ in range(b_wid)]for _ in range(b_hei)], zoom, zoom_direction, self)
            self.widgets_list[i+1]["goal_widget"] = goal_gl_board


            if self.arg_list[1]:
                answer = self.args[2]
            else:
                answer = tempfile.mktemp()
                with open(answer, "w+") as f:
                    f.write(json.dumps(self.answers_list[i+1]))
            config = self.config

            double_widget = DoubleWidget(start_gl_board, goal_gl_board, answer, config)
            double_widget.slider.valueChanged.connect(self.SliderChange)
            double_widget.op_idx = 0
            double_widget.answer_num = self.widgets_list[i+1]["answer"]["n"]
            self.widgets_list[i+1]["double_widget"] = double_widget
            self.container_layout.addWidget(double_widget)


    def decide_focus_widget(self):
        for i in range(1,len(self.widgets_list)):
                if (
                    self.widgets_list[i]["double_widget"].start_board.is_focus or
                    self.widgets_list[i]["double_widget"].goal_board.is_focus):
                        self.index = i
                        return self.widgets_list[i]
        return self.widgets_list[0]

    def focusInEvent(self, event):
        super().focusInEvent(event)


    def update_gl_on_scroll(self, value):
        for widget in self.widgets_list:
            pass
            # widget.update()

    def SliderChange(self, value):
        if self.double_widget != self.widgets_list[0]["double_widget"]:
            self.applyOn(value)


    def add_solver(self):
        text_solver = QLineEdit()
        self.config.solvers.append("")
        self.solver_layout.addWidget(text_solver)

    def remove_solver(self):
        item = self.solver_layout.takeAt(self.solver_layout.count()-1)
        widget = item.widget()
        self.solver_layout.removeWidget(widget)
        widget.deleteLater()
        self.config.solvers.pop()

    def add_pc_address(self):
        self.config.pcs.append({"is-Check": False, "ip_address": "", "solver": ""})
        pc_address_line_layout = QHBoxLayout()
        add_pc_address_check = QCheckBox()
        add_pc_address_line = QLineEdit()
        add_pc_solver_line = QLineEdit()


        self.pc_address_layout.addLayout(pc_address_line_layout)
        pc_address_line_layout.addWidget(add_pc_address_check)
        pc_address_line_layout.addWidget(add_pc_address_line)
        pc_address_line_layout.addWidget(add_pc_solver_line)

    def remove_pc_address(self):
        self.config.pcs.pop()
        if self.pc_address_layout.count():
            last_pc_address_line = self.pc_address_layout.takeAt(self.pc_address_layout.count()-1)
            layout = last_pc_address_line.layout()
            while layout.count():
                item = layout.takeAt(layout.count()-1)
                widget = item.widget()
                layout.removeWidget(widget)
                widget.deleteLater()
            self.pc_address_layout.removeItem(last_pc_address_line)

    # def update_timer(self):
    #     self.time = self.time.addSecs(1)

    #     self.time_label.setText(str(300-self.time.second()))

    #     if self.time.second() >= 300:
    #         self.timer.stop()
    #         self.time_label.setText("終了")
#     def update_time(self):
#         pass


# class Timer(QObject):
#     update = pyqtSignal(int)
#     def __init__(self):
#         super().__init__()




    # def start_timer(self):
    #     self.timer.start(300)

    # def timer(self):
    #     while(1):
    #         current_timer = time.time()
    #         progress_time = self.end_time - current_timer
    #         self.time_label.setText(str(progress_time//1))
    #         if progress_time <= 0.0:
    #             break
    #         self.time_label.setText("終了")




