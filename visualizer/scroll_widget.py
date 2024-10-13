import sys
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QMainWindow
from gl import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from mainwidget import *
from double_widget import *

class ScrollWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        # self.glwidget_goal = glwidget_goal
        scroll_area_layout = QVBoxLayout(self)
        self.scroll_area = CustomScrollArea()
        print(f'scroll size: {self.scroll_area}')
        scroll_area_layout.addWidget(self.scroll_area)
        # scroll_widget = QWidget()

        # scroll_layout = QHBoxLayout(scroll_widget)

        # scroll_layout.addWidget(self.glwidget)
        # scroll_layout.addWidget(self.glwidget_goal)

        # scroll_area.setWidget(scroll_widget)
        # self.scroll_area.setWidget(self.glwidget)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)



        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_gl_on_scroll)
        self.scroll_area.horizontalScrollBar().valueChanged.connect(self.update_gl_on_scroll)



    def update_gl_on_scroll(self,value):
        self.update()

    def resizeEvent(self,event):
        width = self.width()
        height = self.height()

        print(f'Scroll Size {width} x {height}')

    def AddWidget(self):
        pass



class CustomScrollArea(QScrollArea):
    def __init__(self,*args,**kwargs):
        super(CustomScrollArea,self).__init__(*args,**kwargs)

    def keyPressEvent(self,event: QKeyEvent):
        self.widget().keyPressEvent(event)





