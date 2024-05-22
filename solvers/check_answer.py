import numpy as np
import json
import sys

if len(sys.argv) < 3:
    print("usage: %s <problem json> <answer json>" % sys.argv[0])
    exit()

problem_json = sys.argv[1]
answer_json = sys.argv[2]

with open(problem_json) as f:
    problem = json.loads(f.read())

with open(answer_json) as f:
    answer = json.loads(f.read())

width = problem["board"]["width"]
height = problem["board"]["height"]
start = np.array([[int(x) for x in line] for line in problem["board"]["start"]], dtype=np.int8)
goal = np.array([[int(x) for x in line] for line in problem["board"]["goal"]], dtype=np.int8)

ops = answer["ops"]

for i in range(len(ops)):
    op = ops[i]
    x = op["x"]
    y = op["y"]
    s = op["s"]

    print("==========")
    print(y, x, "上下左右"[s])
    print("\n".join([" ".join([str(x) for x in line]) for line in start]))
    print()

    tmp = start[y:y+1, x:x+1].copy()
    if s == 0:
        start[y:height-1, x:x+1] = start[y+1:height, x:x+1]
        start[height-1:height, x:x+1] = tmp
    elif s == 1:
        start[1:y+1, x:x+1] = start[0:y, x:x+1]
        start[0:1, x:x+1] = tmp
    elif s == 2:
        start[y:y+1, x:width-1] = start[y:y+1, x+1:width]
        start[y:y+1, width-1:width] = tmp
    elif s == 3:
        start[y:y+1, 1:x+1] = start[y:y+1, 0:x]
        start[y:y+1, 0:1] = tmp

    print("\n".join([" ".join([str(x) for x in line]) for line in start]))