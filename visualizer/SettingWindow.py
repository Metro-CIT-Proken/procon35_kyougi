

from setting_widget import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class SettingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Setting Window')
        self.setGeometry(300, 50, 600, 600)
        self.widget = SettingWidget()
        self.layout().addWidget(self.widget)


    def resizeEvent(self, event: QResizeEvent):
        self.widget.resize(
            event.size().width(),
            event.size().height())

    def closeEvent(self, event: QCloseEvent):
        self.widget.close()
        event.accept()
