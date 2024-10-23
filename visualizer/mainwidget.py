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
from widget_dict import *
from enum import Enum



MARGIN_LEFT = 10
MARGIN_TOP = 10
MARGIN_RIGHT = 10
MARGIN_BOTTOM = 10

class Color(Enum):
    NORMAL = 1
    DISTANCE = 2

class Arg(Enum):
    NONE = 1
    ONE = 2
    TWO = 3




class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # refactor: 変数の名前をもっと具体的に
        # refactor: 色モードの指定はenumを使う
        self.args = sys.argv


        self.color_mode = Color.NORMAL
        self.arg_len = Arg.NONE


        self.answers_list = []
        for i in self.args:
            if i  == "s":
                self.color_mode = Color.DISTANCE

        # refactor: if文に直す
        if len(self.args) >= 2:
            arg = self.args[1]
            if not (self.args[1] == 'a' or self.args[1] == 's'):
                self.arg_len = Arg.ONE
                with open(arg) as file:
                    self.problem = json.load(file)


        elif len(self.args) >= 3:
            arg = self.args[2]
            if not (self.args[2] == 'a' or self.args[2] == 's'):
                self.arg_len = Arg.TWO
                with open(arg) as file:
                    self.file_answer = json.load(file)








        self.one_get = False

        self.widgets_list = []#scroll widget 内にある widgetのリスト
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



        layout.setContentsMargins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT, MARGIN_BOTTOM)
        layout.addLayout(layout_settings, 1)
        layout_settings.addLayout(self.first_gl_layout)
        layout_settings.addLayout(layout_cont)
        layout.addLayout(self.layout_gl, 2)

        self.container_layout = QVBoxLayout()
        self.container_widget = QWidget()


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
        self.update_widget()




    def keyPressEvent(self, event: QKeyEvent):
        # if self.args[2] == "a":

        if event.key() == Qt.Key.Key_Right and not(self.op_idx == self.answer_num):
                self.right_key_check = self.applyOn(self.op_idx+1)
            #左キーに進むと一手戻る
        elif event.key() == Qt.Key.Key_Left and not(self.op_idx == 0):
                self.right_key_check = self.applyOn(self.op_idx-1)


        self.glwidget.keyPressEvent(event)
        self.glwidget_goal.keyPressEvent(event)

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
            # if "start_board" in self.widgets_list[0]:
                if  not(self.widgets_list[0].start_board == self.glwidget):
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

    # refactor: 長いのでもっと処理ごとに関数にわける
    def get(self):
            if self.one_get:
                    for widget in self.widgets_list:
                        self.scroll_area.scroll_area_layout.removeWidget(widget.double_widget)
                        widget.double_widget.deleteLater()
                    self.widgets_list = []
                    self.first_gl_layout.removeWidget(self.first_double_widget)
                    self.first_double_widget.deleteLater()

            self.get_process()

   



            if self.get_pro.status_code == 200:
                    self.message.setText("取得成功です")
            elif  self.get_pro.status_code == 100:
                    self.message.setText("ソルバー取得成功")


            print("status 200")
            self.make_first_widget()

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
        for i in range(len(self.widgets_list),len(self.answers_list)):
            widgets_dict = WidgetDict()
            self.widgets_list.append(widgets_dict)


            self.op_idx = 0

            b_wid = self.get_pro.board_width
            widgets_dict.board_width = b_wid


            b_hei = self.get_pro.board_height
            widgets_dict.board_height = b_hei



            widgets_dict.answer = self.answers_list[i]
            print("answers_list")
            print(self.answers_list)

            print("widgets_dict.answer")
            print(widgets_dict.answer)


            dis_board = [[0 for _ in range(b_wid)]for _ in range(b_hei)]
            widgets_dict.dis_board = dis_board

            start_board = [row[:] for row in self.get_pro.start_board]
            widgets_dict.start_board = start_board

            goal_board =  [row[:] for row in self.get_pro.goal_board]
            widgets_dict.goal_board = goal_board

            zoom = widgets_dict.zoom
            zoom_direction = widgets_dict.zoom_direction

            start_gl_board = OpenGLWidget(start_board, goal_board, zoom, zoom_direction, None, None, self.color_mode == Color.DISTANCE, self)
            widgets_dict.start_widget = start_gl_board
            start_gl_board.resize(int((self.width()*2/3)/2-40), int((self.width()*2/3)/2-40))

            goal_gl_board = OpenGLWidget(goal_board, [[ -1 for _ in range(b_wid)]for _ in range(b_hei)], zoom, zoom_direction, self)
            widgets_dict.goal_widget = goal_gl_board


            # if self.arg_two:
            if self.arg_len == Arg.TWO:
                answer = self.args[2]
            else:
                answer = tempfile.mktemp()
                with open(answer, "w+") as f:
                    f.write(json.dumps(self.answers_list[i]))
            config = self.config

            double_widget = DoubleWidget(start_gl_board, goal_gl_board, answer, config)
            double_widget.slider.valueChanged.connect(self.SliderChange)

            double_widget.op_idx = 0
            print("widgets_dict.answer.n")
            print(widgets_dict.answer)
            double_widget.answer_num = widgets_dict.answer["n"]
            widgets_dict.double_widget = double_widget
            self.container_layout.addWidget(double_widget)


    def decide_focus_widget(self):
        for i in range(len(self.widgets_list)):
                if  (
                    self.widgets_list[i].double_widget.start_board.is_focus
                    or
                    self.widgets_list[i].double_widget.goal_board.is_focus
                    ):
                        self.index = i
                        return self.widgets_list[i]
        return self.first_widgets_dict

    def focusInEvent(self, event):
        super().focusInEvent(event)


    def SliderChange(self, value):
        # if self.double_widget != self.widgets_list[0]["double_widget"]:
        if self.double_widget != self.first_widgets_dict.double_widget:
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


    def update_widget(self):
        if not(self.widgets_list == []):
            self.glwidget_info = self.decide_focus_widget()


            self.glwidget = self.glwidget_info.start_widget


            self.glwidget_goal = self.glwidget_info.goal_widget


            self.double_widget = self.glwidget_info.double_widget

            self.op_idx = self.double_widget.op_idx


            self.answer = self.glwidget_info.answer

            self.answer_num = self.double_widget.answer_num

            self.dis_board = self.glwidget_info.dis_board

            self.board_width = self.glwidget_info.board_width


    def addExecSolver(self):
        for i in range(self.solver_layout.count()):
            item = self.solver_layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QLineEdit):
                # self.config.solvers.append(item.widget().text())
                if not(item.widget().text() == ""):
                        answer_exec = Exec(self.get_pro.problem, item.widget().text())
                        answer = answer_exec.exe_cpp(self.on_answer_created)


    def addPcSolver(self):
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


    def make_first_widget(self):
        self.first_widgets_dict = WidgetDict()
        start_board = [row[:] for row in self.get_pro.start_board]




        goal_board = [row[:] for row in self.get_pro.goal_board]

        b_wid = self.get_pro.board_width
        b_hei = self.get_pro.board_height


        self.first_widgets_dict.board_width = b_wid
        self.first_widgets_dict.baord_height = b_hei


        dis_board = [[0 for _ in range(b_wid)]for _ in range(b_hei)]
        self.first_widgets_dict.dis_board = dis_board

        zoom = self.first_widgets_dict.zoom
        zoom_direction = self.first_widgets_dict.zoom_direction


        if start_board != [[]] or goal_board != [[]]:
            first_start_gl = OpenGLWidget(start_board, goal_board, zoom , zoom_direction, None, None, self.color_mode == Color.DISTANCE, self)
            self.first_widgets_dict.start_widget = first_start_gl
            first_goal_gl = OpenGLWidget(goal_board, [[ -1 for _ in range(b_wid)]for _ in range(b_hei)], zoom, zoom_direction, None, None, False, self)
            self.first_widgets_dict.goal_widget = first_goal_gl

            first_double_widget = FirstDoubleWidget(first_start_gl, first_goal_gl)
            first_double_widget.op_idx = 0

            self.first_widgets_dict.double_widget = first_double_widget

            self.first_widgets_dict.double_widget.answer_num = 0
            self.answer_num = 0
            self.first_gl_layout.addWidget(first_double_widget)


            self.glwidget = self.first_widgets_dict.start_widget

            self.glwidget_goal = self.first_widgets_dict.goal_widget

            self.first_double_widget = self.first_widgets_dict.double_widget

            self.dis_board = self.first_widgets_dict.dis_board

            self.answer_num = self.first_widgets_dict.answer["n"]

        self.one_get = True


        self.container_widget.setLayout(self.container_layout)
        self.scroll_area.scroll_area.setWidget(self.container_widget)
        self.fixed_form_num = self.get_pro.fixed_form_num


        self.fixed_form_numbers = self.get_pro.fixed_form_numbers
        self.fixed_form_widths = self.get_pro.fixed_form_widths



        self.fixed_form_heights = self.get_pro.fixed_form_heights
        self.fixed_form_cells = self.get_pro.fixed_form_cells


    def get_process(self):
        if self.arg_len == Arg.ONE:
                    self.get_pro = GetByHand(self.problem)
                    print("hand problem")
                    print(self.get_pro.problem)
        else:
                    self.get_pro = Get(self.config)

        if self.get_pro.status_code== 200 or self.get_pro.status_code == 100:
                    self.answers_list = [ ]
                    # if self.arg_two:
                    if self.arg_len == Arg.TWO:
                        self.on_answer_created(self.file_answer)
                    else:
                        self.addPcSolver()
                    self.addExecSolver()

