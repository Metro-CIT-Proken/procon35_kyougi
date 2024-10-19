

from homewindow  import *
from subwindow import *
from mainwidget import *
from subhomewindow import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from PyQt6.QtWidgets import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.option = []
        self.setWindowTitle('Test GUI')
        self.setGeometry(300, 50, 1200, 1200)
        self.widget = MainWidget(self)


        # self.stacked_widget = QStackedWidget()
        # self.homewidget = HomeWindow(self)
        # self.widget_auto_red = MainWidget(self,"a","s")
        # self.widget_auto_normal = MainWidget(self,"a")
        # self.widget_mannual_red = MainWidget(self,"m","s")
        # self.widget_mannual_normal = MainWidget(self,"m")
        # self.widget_online_red = MainWidget(self,"o","s")
        # self.widget_online_normal = MainWidget(self,"o")
        # self.subhomewindow_auto = SubHomeWindow(self)
        # self.subhomewindow_mannual = SubHomeWindow(self)
        # self.subhomewindow_online = SubHomeWindow(self)

        self.layout().addWidget(self.widget)


        # self.subwidget = SubWindow(self)
    #     self.stacked_widget.addWidget(self.homewidget)
    #     self.stacked_widget.addWidget(self.subhomewindow_auto)
    #     self.stacked_widget.addWidget(self.subhomewindow_mannual)
    #     self.stacked_widget.addWidget(self.subhomewindow_online)
    #     self.stacked_widget.addWidget(self.widget_auto_normal)
    #     self.stacked_widget.addWidget(self.)


    #     self.homewidget.autobutton.clicked.connect(self.to_subhomewindow)
    #     self.homewidget.mannualbutton.clicked.connect(self.to_subhomewindow)
    #     self.
    #     # self.stacked_widget.addWidget(self.widget)

    # def to_subhomewindow(self):
    #     self.stacked_widget.setCurrentIndex(2)

    # def to_mainwidget(self):


    def resizeEvent(self, event: QResizeEvent):
        self.widget.resize(
            event.size().width(),
            event.size().height())

    def closeEvent(self, event: QCloseEvent):
        self.widget.close()
        event.accept()
