import functools
from enum import Enum

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# class Cells(Enum):
#     ZERO = 0
#     ONE = 1
#     TWO  = 2
#     THREE = 3
    # SAME = 4


class CellColorsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # painter = QPainter()
        # self.zero_color = QColor(255, 0, 0)
        # self.one_color = QColor(0, 0, 255)
        # self.two_color  = QColor(0, 255, 0)
        # self.three_color = QColor(255, 255, 0)
        # self.same_color = QColor(167, 87, 168)
        self.index = 0
        self.layout = QHBoxLayout(self)
        self.button_list = []
        # self.color_list = [self.zero_color, self.one_color, self.two_color, self.three_color, self.same_color]
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
        color.rgb

        if color.isValid():
            print(index)
                # self.zero_color = color
                # color_red = QColor(self.zero_color).red()
            color_red = QColor(color).red()
                # color_green = QColor(self.zero_color).green()
            color_green = QColor(color).green()
                # color_blue = QColor(self.zero_color).blue()
            color_blue = QColor(color).blue()
            for button in self.button_list:
                if button == clicked_button:
                    button.setStyleSheet(f"background-color: rgb({color_red} ,{color_green}, {color_blue} )")
                # self.color_list[index] = self.zero_color
            self.color_list[index] = color

            print(f"index: {index}, red: {color_red}, green: {color_green}, blue: {color_blue}")

            # elif index == 1:
            #     # self.one_color = color
            #     # color_red = QColor(self.one_color).red()
            #     color_red = QColor(color).red()
            #     # color_green = QColor(self.one_color).green()
            #     color_red = QColor(color).green()
            #     # color_blue = QColor(self.one_color).blue()
            #     color_blue = QColor(color).blue()
            #     for button in self.button_list:
            #         if button == clicked_button:
            #             button.setStyleSheet(f"background-color: rgb({color_red} ,{color_green}, {color_blue} )")
            #     # self.color_list[index] = self.one_color
            #     self.color_list[index] = color

            #     print(f"index: {index}, red: {color_red}, green: {color_green}, blue: {color_blue}")


            # elif index == 2:
            #     # self.two_color = color
            #     # color_red = QColor(self.two_color).red()
            #     # color_green = QColor(self.two_color).green()
            #     # color_blue = QColor(self.two_color).blue()
            #     color_red = QColor(color).red()
            #     color_green = QColor(color).green()
            #     color_blue = QColor(color).blue()
            #     for button in self.button_list:
            #         if button == clicked_button:
            #             button.setStyleSheet(f"background-color: rgb({color_red} ,{color_green}, {color_blue} )")
            #     self.color_list[index] = color

            #     print(f"index: {index}, red: {color_red}, green: {color_green}, blue: {color_blue}")

            # elif index == 3:
            #     # self.three_color = color
            #     # color_red = QColor(self.three_color).red()
            #     # color_green = QColor(self.three_color).green()
            #     # color_blue = QColor(self.three_color).blue()
            #     color_red = QColor(color).red()
            #     color_green = QColor(color).green()
            #     color_blue = QColor(color).blue()
            #     for button in self.button_list:
            #         if button == clicked_button:
            #             button.setStyleSheet(f"background-color: rgb({color_red} ,{color_green}, {color_blue} )")
            #     self.color_list[index] = color

            #     print(f"index: {index}, red: {color_red}, green: {color_green}, blue: {color_blue}")

            # else:
            #     # self.same_color = color
            #     # color_red = QColor(self.same_color).red()
            #     # color_green = QColor(self.same_color).green()
            #     # color_blue = QColor(self.same_color).blue()
            #     for button in self.button_list:
            #         if button == clicked_button:
            #             button.setStyleSheet(f"background-color: rgb({color_red} ,{color_green}, {color_blue} )")
            #     self.color_list[index] = self.same_color
            #     print(f"index: {index}, red: {color_red}, green: {color_green}, blue: {color_blue}")














