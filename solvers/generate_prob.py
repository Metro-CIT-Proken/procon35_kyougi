import numpy as np
import json
import sys
import copy

from problem import Problem

if len(sys.argv) < 4:
    print("usage: %s <problem json> <answer json> <output problem json>" % sys.argv[0])
    exit()

problem_json = sys.argv[1]
answer_json = sys.argv[2]

with open(problem_json) as f:
    problem = Problem(json.loads(f.read()))
with open(answer_json) as f:
    answer = json.loads(f.read())

board_test = copy.deepcopy(problem.start)
ops = answer["ops"]
for i in range(len(ops)):
    op = ops[i]
    x = op["x"]
    y = op["y"]
    s = op["s"]
    p = op["p"]

    stencil = problem.generals[p]
    board_test = stencil.apply(board_test, x, y, s)

problem.goal = board_test
json.dump(problem.to_json(),  open(sys.argv[3], "w"))