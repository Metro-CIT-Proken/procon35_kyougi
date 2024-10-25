import functools
from enum import Enum

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class CellColorsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.index = 0
        self.layout = QHBoxLayout(self)
        self.button_list = []
        self.color_list = [QColor(255, 0, 0), QColor(0, 0, 255), QColor(0, 255, 0), QColor(255, 255, 0), QColor(167, 87, 168)]

        for i in range(5):

            self.cell_color_widget = QWidget()
            self.layout.addWidget(self.cell_color_widget)
            self.cell_color_layout = QHBoxLayout(self.cell_color_widget)

            self.layout.addLayout(self.cell_color_layout)
            if i != 4:
                color_cell_label = QLabel(str(i))
            else:
                color_cell_label = QLabel("同じ")
            color_cell_button = QPushButton(" ")
            self.button_list.append(color_cell_button)
            red = QColor(self.color_list[i]).red()
            green = QColor(self.color_list[i]).green()
            blue = QColor(self.color_list[i]).blue()
            color_cell_button.setStyleSheet(f"background-color: rgb({red}, {green}, {blue});")
            color_cell_button.clicked.connect(functools.partial(self.change_color, i))
            self.cell_color_layout.addWidget(color_cell_label)
            self.cell_color_layout.addWidget(color_cell_button)

    def change_color(self, index, event):
        color = QColorDialog.getColor()
        clicked_button = self.sender()

        if color.isValid():
            print(index)
            color_red = QColor(color).red()
            color_green = QColor(color).green()
            color_blue = QColor(color).blue()
            for button in self.button_list:
                if button == clicked_button:
                    button.setStyleSheet(f"background-color: rgb({color_red} ,{color_green}, {color_blue} )")
            self.color_list[index] = color

            print(f"index: {index}, red: {color_red}, green: {color_green}, blue: {color_blue}")

