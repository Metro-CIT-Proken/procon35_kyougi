from PyQt6.QtCore import *
from PyQt6.QtGui import *

from PyQt6.QtWidgets import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class SettingWidget(QWidget):
    def __init__(self):
        self.container_layout = QVBoxLayout()
        self.container_widget = QWidget()

