import sys
import json

import problem

if len(sys.argv) < 2:
    print("usage: python {} <problem path>".format(sys.argv[0]))
    exit(1)

prob_path = sys.argv[1]
prob = problem.Problem(json.load(open(prob_path)))

goal = prob.goal
goal = prob.generals[24].apply_inverse(goal, 0, 0, problem.Stencil.StencilDirection.RIGHT)
goal = prob.generals[23].apply_inverse(goal, 0, 0, problem.Stencil.StencilDirection.DOWN)

result = json.dumps(prob.to_json())
print(result)