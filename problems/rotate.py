import numpy
import json
import sys

if len(sys.argv) < 2:
    print("usage: python {} <problem json>".format(sys.argv[0]))
    exit()

problem = json.load(open(sys.argv[1]))

start_json = problem["board"]["start"]
goal_json = problem["board"]["goal"]

start_board = numpy.array([[int(x) for x in line] for line in start_json])
start_board = start_board.transpose()
goal_board = numpy.array([[int(x) for x in line] for line in goal_json])
goal_board = goal_board.transpose()

problem["board"]["start"] = ["".join([str(x) for x in line]) for line in start_board]
problem["board"]["goal"]  = ["".join([str(x) for x in line]) for line in goal_board]

problem["board"]["width"], problem["board"]["height"] = problem["board"]["height"], problem["board"]["width"]

for stenc in problem["general"]["patterns"]:
    cells = numpy.array([[int(x) for x in line] for line in stenc["cells"]])
    cells = cells.transpose()
    stenc["height"] = cells.shape[0]
    stenc["width"]  = cells.shape[1]
    stenc["cells"]  = ["".join([str(x) for x in line]) for line in cells]

print(json.dumps(problem, indent=2))