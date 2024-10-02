import sys
import random
import time
import numpy as np

sys.path.append("..")
import solvers.problem as problem

CELLS = [0, 1, 2, 3]

if len(sys.argv) < 3:
    print("usage: python3 {} <width> <height>".format(sys.argv[0]))
    exit()

width = int(sys.argv[1])
height = int(sys.argv[2])

def generate(width, height, seed = 0):
    rng = random.Random()
    rng.seed(seed)

    board_start = np.array(rng.choices(CELLS, k=width * height)).reshape([height, width])
    board_goal = board_start.copy()

    goal_view = board_goal.reshape(-1)
    for _ in range(10 * width * height):
        i = rng.randint(0, width * height - 1)
        j = rng.randint(0, width * height - 1)
        goal_view[i], goal_view[j] = goal_view[j], goal_view[i]

    prob = problem.Problem(width=width, height=height)
    prob.start.board = board_start
    prob.goal.board = board_goal

    return prob

prob = generate(width, height, time.time_ns())
print(prob.to_json())