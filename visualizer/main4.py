import sys

from mainwindow import *
from mainwidget import MainWidget
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from PyQt6.QtWidgets import *


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    # w.start_play()
    w.show()
    w.raise_()
    app.exec()



if __name__ == '__main__':
    main()
