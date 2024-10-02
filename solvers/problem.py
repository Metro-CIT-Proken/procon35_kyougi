import json
import sys
import copy

import numpy as np
from enum import IntEnum

class Board:
    CELL_SIZE = 2 * 256 * 256 // 256

    def __init__(self, prob: "Problem", json = None, width = None, height = None):
        self.prob = prob
        if json is not None:
            self.board = np.array([[int(x) for x in line] for line in json], dtype=np.int8)
            self.height = self.board.shape[0]
            self.width = self.board.shape[1]
        else:
            self.board = np.zeros((height, width), dtype=np.int8)
            self.height = height
            self.width = width

    def to_json(self):
        return ["".join(map(str, line)) for line in self.board]

class Stencil:
    class StencilDirection(IntEnum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    def __init__(self, prob, id, width, height):
        self.prob = prob
        self.id = id
        self.width = width
        self.height = height
        self.cells = np.zeros([height, width], dtype=np.int8)
    
    @staticmethod
    def from_json(prob, json):
        width = json["width"]
        height = json["height"]
        p_id = json["p"]
        ret = Stencil(prob, p_id, width, height)
        ret.prob = prob
        ret.cells = np.array([[int(x) for x in line] for line in json["cells"]], dtype=np.int8)
        return ret
    
    def to_json(self):
        return {
            "width": self.width,
            "height": self.height,
            "p": self.id,
            "cells": [
                "".join(map(str, line)) for line in self.cells
            ]
        }
    
    def apply(self, board: Board, x, y, s: StencilDirection):
        new_board = copy.copy(board)
        x_start = max(0, x)
        x_end = min(board.width, x + self.width)
        y_start = max(0, y)
        y_end = min(board.height, y + self.height)
        px_start = max(0, -x)
        px_end = min(self.width, board.width - x)
        py_start = max(0, -y)
        py_end = min(self.height, board.height - y)
        if s == Stencil.StencilDirection.UP:
            for tx in range(x_start, x_end):
                cond = np.zeros((board.height), dtype=bool)
                cond[y_start:y_end] = self.cells[py_start:py_end, tx - x]
                pushed_cells = np.extract(~cond, board.board[:, tx])
                float_cells = np.extract(cond, board.board[:, tx])
                new_board.board[:, tx] = np.concatenate((pushed_cells, float_cells))
        elif s == Stencil.StencilDirection.DOWN:
            for tx in range(x_start, x_end):
                cond = np.zeros((board.height), dtype=bool)
                cond[y_start:y_end] = self.cells[py_start:py_end, tx - x]
                pushed_cells = np.extract(~cond, board.board[:, tx])
                float_cells = np.extract(cond, board.board[:, tx])
                new_board.board[:, tx] = np.concatenate((float_cells, pushed_cells))
        elif s == Stencil.StencilDirection.LEFT:
            for ty in range(y_start, y_end):
                cond = np.zeros((board.width), dtype=bool)
                cond[x_start:x_end] = self.cells[ty - y, px_start:px_end]
                pushed_cells = np.extract(~cond, board.board[ty, :])
                float_cells = np.extract(cond, board.board[ty, :])
                new_board.board[ty, :] = np.concatenate((pushed_cells, float_cells))
        elif s == Stencil.StencilDirection.RIGHT:
            for ty in range(y_start, y_end):
                cond = np.zeros((board.width), dtype=bool)
                cond[x_start:x_end] = self.cells[ty - y, px_start:px_end]
                pushed_cells = np.extract(~cond, board.board[ty, :])
                float_cells = np.extract(cond, board.board[ty, :])
                new_board.board[ty, :] = np.concatenate((float_cells, pushed_cells))

        return new_board


    def placeables(self, board: Board):
        for y in range(1 - self.height, board.height):
            for x in range(1 - self.width, board.width):
                yield (x, y)

class Problem:
    def __init__(self, json = None, width = None, height = None):
        if json is not None:
            self.start = Board(self, json["board"]["start"])
            self.goal = Board(self, json["board"]["goal"])
            self.generals = dict[int, Stencil]()
            self.width = json["board"]["width"]
            self.height = json["board"]["height"]
            for stencil in json["general"]["patterns"]:
                p = Stencil.from_json(self, stencil)
                self.generals[p.id] = p
        else:
            self.start = Board(self, width=width, height=height)
            self.goal = Board(self, width=width, height=height)
            self.generals = dict[int, Stencil]()
            self.width = width
            self.height = height
        self.createStencils()

    def createStencils(self):
        funcs = [lambda x, y: True, 
                 lambda x, y: y % 2 == 0,
                 lambda x, y: x % 2 == 0]
        p = Stencil(self, 0, 1, 1)
        p.cells[0][0] = 1
        self.generals[p.id] = p

        # 2^1 ~ 2^(9-1)
        for n in range(1, 9):
            size = 2 ** n
            for i in range(len(funcs)):
                p_id = (n - 1) * 3 + i + 1
                p = Stencil(self, p_id, size, size)
                for y in range(size):
                    for x in range(size):
                        p.cells[y][x] = 1 if funcs[i](x, y) else 0
                self.generals[p_id] = p

    def to_json(self):
        general_stencils = list(filter(lambda x: x.id >= 26, self.generals.values()))
        return {
            "board": {
                "width": self.width,
                "height": self.height,
                "start": self.start.to_json(),
                "goal": self.goal.to_json()
            },
            "general": {
                "n": len(general_stencils),
                "patterns": [
                    x.to_json() for x in general_stencils
                ]
            }
        }