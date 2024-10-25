

from homewindow  import *
from mainwidget import *
from subhomewindow import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from PyQt6.QtWidgets import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from setting_widget import *




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test GUI')
        self.setGeometry(300, 50, 1200, 1200)
        self.widget = SettingWidget(self)



        self.layout().addWidget(self.widget)



    def resizeEvent(self, event: QResizeEvent):
        self.widget.resize(
            event.size().width(),
            event.size().height())

    def closeEvent(self, event: QCloseEvent):
        self.widget.close()
        event.accept()
