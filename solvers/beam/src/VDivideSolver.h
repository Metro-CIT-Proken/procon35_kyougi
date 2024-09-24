#pragma once

#include "solver.h"

class VDivideSolver : SolverBase {
public:
    VDivideSolver(int cells_per_once) :
        cells_per_once(cells_per_once)
    {
    }

    std::vector<Action> solve(const Problem &prob);

    int cells_per_once;
};