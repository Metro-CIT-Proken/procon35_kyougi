#pragma once

#include <vector>

#include "board.h"

using WordType = long long;
constexpr int CELL_BITS = 2;
constexpr int WORD_BITS = sizeof(WordType) * 8;

class Stencil_bitboard {
public:

    Stencil_bitboard(const Stencil &stenc, const Problem *prob);

    int xMin() const { return 1 - this->width; }
    int xMax() const { return this->prob->start.width; }

    std::vector<std::vector<std::vector<WordType>>> cellsTable;
    std::vector<std::vector<int>> oneBitsTable;
    int width, height;
    int id;
    const Problem *prob;
};

class Board_bitboard {
public:

    Board_bitboard(const Board &board, const Problem *prob);

    Board toBoard(const Problem &prob) const;
    void advance(const Stencil_bitboard &stenc, int x, int y, int s);

    int getCell(int x, int y) const {
        int word_offset = (CELL_BITS * x) / WORD_BITS,
            word_rem    = (CELL_BITS * x) % WORD_BITS;
        return (cells[y][word_offset] >> (WORD_BITS - CELL_BITS - word_rem)) & (((WordType)1 << CELL_BITS) - 1);
    }

    std::vector<std::vector<WordType>> cells;
};

// implement
class Problem_bitboard {
public:

    Problem_bitboard(const Problem *prob);

    Board_bitboard start, goal;
    const Problem *prob;
    std::map<int, Stencil_bitboard> stencils;
    int width, height;
};