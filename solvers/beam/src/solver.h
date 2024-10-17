#pragma once

#include <vector>
#include "board.h"

class SolverBase
{
public:
    virtual std::vector<Action> solve(const Problem &prob) = 0;
};