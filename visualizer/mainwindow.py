

from homewindow  import *
from subwindow import *
from mainwidget import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from PyQt6.QtWidgets import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test GUI')
        self.setGeometry(300, 50, 1000, 1000)
        # self.stacked_widget = QStackedWidget()

        self.widget = MainWidget(self)
        self.layout().addWidget(self.widget)
        # self.homewidget = HomeWindow(self)
        # self.subwidget = SubWindow(self)
        # self.stacked_widget.addWidget(self.homewidget)
        # self.stacked_widget.addWidget(self.widget)
