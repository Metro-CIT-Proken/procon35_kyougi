


from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



class HomeWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.autobutton = QPushButton("自動モードで行う")
        self.mannualbutton = QPushButton("手動モードで行う")
        self.onlinebutton = QPushButton("オンライン対戦する")
        layout.addWidget(self.autobutton)
        layout.addWidget(self.mannualbutton)
        layout.addWidget(self.onlinebutton)
        self.setLayout(layout)
