import json
import sys
from queue import Queue

from problem import Problem, Board, Stencil

class BeamState:
    def __init__(self, board: Board, depth: int):
        self.board = board
        self.remaining_depth = depth

if len(sys.argv) < 2:
    print("usage: %s <problem json>" % sys.argv[0])
    exit()

problem_json = sys.argv[1]

with open(problem_json) as f:
    prob = Problem(json.loads(f.read()))

beam_q = Queue[BeamState]()
beam_q.put(BeamState(prob.start, 10))
while beam_q.qsize() != 0:
    state = beam_q.get()
    candidates = []

    for piece in state.board.prob.generals.values():
        for x, y in piece.placeables(state.board):
            for s in Stencil.StencilDirection:
                new_board = piece.apply(state.board, x, y, s)