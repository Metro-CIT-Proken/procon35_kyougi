#pragma once

#include "solver.h"

class SimpleSolver : SolverBase {
public:
    SimpleSolver();

    std::vector<Action> solve(const Problem &prob);
};