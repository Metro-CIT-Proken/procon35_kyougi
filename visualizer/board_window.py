from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from mainwidget import *

class BoardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test GUI')
        self.setGeometry(300, 50, 1200, 1200)
        self.widget = MainWidget(self)

    def resizeEvent(self, event: QResizeEvent):
        self.widget.resize(
            event.size().width(),
            event.size().height())

    def closeEvent(self, event: QCloseEvent):
        self.widget.close()
        event.accept()
