

from visualizer.board_window import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


from cell_colors import *


class SettingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.args = sys.argv
        layout = QVBoxLayout(self)
        layout_cont = QVBoxLayout()

        layout.addLayout(layout_cont)

        self.cell_colors_widget = CellColorsWidget()

        self.ip_address_line = QLineEdit(self)
        self.ip_address_line.setText(self.config.ip_address_edited)
        
