import sys
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QMainWindow
from gl import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from mainwidget import *

class ScrollWidget(QWidget):
    def __init__(self, glwidget,glwidget_goal,parent=None):
        super().__init__(parent)
        self.glwidget = glwidget
        self.glwidget_goal = glwidget_goal
        scroll_area_layout = QVBoxLayout(self)
        scroll_area = CustomScrollArea()
        print(f'scroll size: {scroll_area}')
        scroll_area_layout.addWidget(scroll_area)
        scroll_widget = QWidget()

        scroll_layout = QHBoxLayout(scroll_widget)

        scroll_layout.addWidget(self.glwidget)
        scroll_layout.addWidget(self.glwidget_goal)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)



        scroll_area.verticalScrollBar().valueChanged.connect(self.update_gl_on_scroll)
        scroll_area.horizontalScrollBar().valueChanged.connect(self.update_gl_on_scroll)



    def update_gl_on_scroll(self,value):
        self.glwidget.update()

    def resizeEvent(self,event):
        width = self.width()
        height = self.height()

        print(f'Scroll Size {width} x {height}')



class CustomScrollArea(QScrollArea):
    def __init__(self,*args,**kwargs):
        super(CustomScrollArea,self).__init__(*args,**kwargs)

    def keyPressEvent(self,event: QKeyEvent):
        self.widget().keyPressEvent(event)





