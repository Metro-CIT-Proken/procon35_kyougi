#pragma once

#include <vector>

#include "board.h"

using WordType = unsigned long long;
constexpr int CELL_BITS = 2;
constexpr int WORD_BITS = sizeof(WordType) * 8;

class Stencil_bitboard {
public:

    Stencil_bitboard(const Stencil &stenc, const Problem *prob);

    int xMin() const { return 1 - this->width; }
    int xMax() const { return this->prob->start.width; }

    WordType &getWord(const int &apply_x, const int &y, const int &wi) {
        return cellsTable[(apply_x - xMin()) * height * wordCount + y * wordCount + wi];
    }

    const WordType &getWord(const int &apply_x, const int &y, const int &wi) const {
        return cellsTable[(apply_x - xMin()) * height * wordCount + y * wordCount + wi];
    }

    int &getOneBitsCount(const int &apply_x, const int &y) {
        return oneBitsTable[(apply_x - xMin()) * height + y];
    }

    const int &getOneBitsCount(const int &apply_x, int const &y) const {
        return oneBitsTable[(apply_x - xMin()) * height + y];
    }

    const int width, height;
    const int id;
    const int wordCount;
    const Problem *prob;

private:
    std::vector<WordType> cellsTable;
    std::vector<int> oneBitsTable;
};

class Board_bitboard {
public:

    Board_bitboard(const Board &board, const Problem *prob);

    Board toBoard(const Problem &prob) const;
    void advance(const Stencil_bitboard &stenc, int x, int y, int s);

    int getCell(int x, int y) const {
        int word_offset = (CELL_BITS * x) / WORD_BITS,
            word_rem    = (CELL_BITS * x) % WORD_BITS;
        auto word = getWord(y, word_offset);
        return (word >> (WORD_BITS - CELL_BITS - word_rem)) & (((WordType)1 << CELL_BITS) - 1);
    }

    WordType &getWord(const int &y, const int &wi) {
        return cells[y * wordsPerLine + wi];
    }

    const WordType &getWord(const int &y, const int &wi) const {
        return cells[y * wordsPerLine + wi];
    }

    const int wordsPerLine;
    std::vector<WordType> cells;
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