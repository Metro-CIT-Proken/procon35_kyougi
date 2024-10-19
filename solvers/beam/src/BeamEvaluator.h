#pragma once

#include "board.h"
#include "bitboard.h"

struct BeamEvaluatorResult {
    int value;
    bool first_line_restored;
};

class BeamEvaluator {
public:
    BeamEvaluator(Problem_bitboard *problem) :
        problem(problem)
    {
    }

    BeamEvaluatorResult evaluate(Board_bitboard const &board) const;

    Problem_bitboard *problem;
};