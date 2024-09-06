

from PyQt6.QtCore import *
from PyQt6.QtGui import *

from PyQt6.QtWidgets import *


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



class SubHomeWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.redbutton = QPushButton("赤盤で行う")
        self.normalbutton = QPushButton("普通の盤で行う")
        layout.addWidget(self.redbutton)
        layout.addWidget(self.normalbutton)
        self.setLayout(layout)
