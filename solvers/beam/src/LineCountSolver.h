#pragma once

#include "solver.h"

class LineCountSolver : SolverBase {
public:
    LineCountSolver();

    std::vector<Action> solve(const Problem &prob);
};