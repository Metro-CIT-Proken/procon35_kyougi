#pragma once

#include "solver.h"

class BeamSolver : public SolverBase
{
public:
    BeamSolver(int width, int depth) :
        beamW(width),
        beamD(depth)
    {
    }

    virtual std::vector<Action> solve(const Problem &prob);

    int beamW, beamD;
};