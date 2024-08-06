import json
import sys
import copy

import numpy as np
from enum import IntEnum

class Board:
    def __init__(self, prob: "Problem", json):
        self.board = np.array([[int(x) for x in line] for line in json], dtype=np.int8)
        self.height = self.board.shape[0]
        self.width = self.board.shape[1]
        self.prob = prob

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
    
    def apply(self, board: Board, x, y, s: StencilDirection):
        new_board = copy.copy(board)
        if s == Stencil.StencilDirection.UP:
            x_start = max(0, x)
            x_end = min(board.width, x + self.width)
            for px in range(max(x_start, x_end)):
                push_idx = 0
                line_idx = board.height - 1
                for py in range(board.height):
                    if py >= y and py < y + self.height and self.cells[py - y][px - x] == 1:
                        new_board.board[line_idx][px] = board.board[py][px]
                        line_idx -= 1
                    else:
                        new_board.board[push_idx][px] = board.board[py][px]
                        push_idx += 1
                    np.flip(new_board.board[push_idx:, :])
                

        # TODO: DOWN, LEFT, RIGHTを実装する


    def placeables(self, board: Board):
        for y in range(1 - self.height, board.height):
            for x in range(1 - self.width, board.width):
                yield (x, y)

class Problem:
    def __init__(self, json):
        self.start = Board(self, json["board"]["start"])
        self.goal = Board(self, json["board"]["goal"])
        self.generals = dict[int, Stencil]()
        for stencil in json["general"]["patterns"]:
            p = Stencil.from_json(self, stencil)
            self.generals[p.id] = p
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