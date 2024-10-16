#pragma once

#include <memory>
#include "bitboard.h"
#include "solver.h"

struct BeamState
{
public:
    BeamState() : p(-1)
    {
    }

    BeamState(std::shared_ptr<Board_bitboard> board, int eval, int p, int x, int y, StencilDirection s, std::shared_ptr<BeamState> prevState) :
        board(board), eval(eval), p(p), x(x), y(y), s(s), prevState(prevState)
    {
    }

    bool operator<(const BeamState &right) const {
        return this->eval < right.eval;
    }

    bool operator>(const BeamState &right) const {
        return this->eval > right.eval;
    }

    std::shared_ptr<Board_bitboard> board;
    int eval, p, x, y;
    StencilDirection s;
    std::shared_ptr<BeamState> prevState;
};

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

class ChokudaiBeamSolver : public SolverBase
{
public:
    ChokudaiBeamSolver(int width, int depth) :
        beamW(width),
        beamD(depth)
    {
    }

    virtual std::vector<Action> solve(const Problem &prob);

    int beamW, beamD;
};

class InboundBeamSolver : public SolverBase
{
public:
    InboundBeamSolver(int width, int depth) :
        beamW(width),
        beamD(depth)
    {
    }

    virtual std::vector<Action> solve(const Problem &prob);

    int beamW, beamD;
};