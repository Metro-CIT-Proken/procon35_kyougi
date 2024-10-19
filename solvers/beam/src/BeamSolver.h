#pragma once

#include <memory>

#include "bitboard.h"
#include "solver.h"
#include "AnswerTree.h"

class BeamState
{
public:

    BeamState(const Board_bitboard &_board, int const &eval, AnswerIndex const &answer_index) :
        board(_board),
        eval(eval),
        answer_index(answer_index)
    {
    }

    BeamState &operator=(BeamState const &rhs) {
        
    }

    BeamState &operator=(BeamState && rhs) {
        return *this;
    }

    bool operator<(const BeamState &right) const {
        return this->eval < right.eval;
    }

    bool operator>(const BeamState &right) const {
        return this->eval > right.eval;
    }

    Board_bitboard board;
    int eval;
    AnswerIndex answer_index;
    // std::shared_ptr<BeamState> prevState;
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

// class ChokudaiBeamSolver : public SolverBase
// {
// public:
//     ChokudaiBeamSolver(int width, int depth) :
//         beamW(width),
//         beamD(depth)
//     {
//     }

//     virtual std::vector<Action> solve(const Problem &prob);

//     int beamW, beamD;
// };

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