#include <bit>
#include <x86intrin.h>

#include "bitboard.h"

Stencil_bitboard::Stencil_bitboard(const Stencil &stenc, const Problem *prob) :
    prob(prob), 
    width(stenc.width),
    height(stenc.height),
    cellsTable(),
    oneBitsTable(),
    id(stenc.id)
{
    cellsTable.resize(xMax() - xMin(), std::vector<std::vector<WordType>>(
        stenc.height, std::vector<WordType>((prob->width * CELL_BITS + WORD_BITS - 1) / WORD_BITS)));
    oneBitsTable.resize(xMax() - xMin(), std::vector<int>(stenc.height));
    
    for(int tx = xMin(); tx < xMax(); tx++) {
        auto &cells = cellsTable[tx - xMin()];
        for(int y = 0; y < height; y++) {
            for(int x = 0; x < width; x++) {
                int xoffset = x + tx;
                if(xoffset < 0)
                    continue;
                else if(xoffset >= prob->width) {
                    break;
                }
                int word_offset = (xoffset * CELL_BITS) / WORD_BITS,
                    word_rem    = (xoffset * CELL_BITS) % WORD_BITS;
                cells[y][word_offset] 
                    |= (stenc.cells[y][x] ? ((WordType)(1 << CELL_BITS) - 1) : 0) << (WORD_BITS - CELL_BITS - word_rem);
            }

            int words_count = (prob->width * CELL_BITS + WORD_BITS - 1) / WORD_BITS;
            for(int i = 0; i < words_count; i++) {
                oneBitsTable[tx - xMin()][y] += std::__popcount(cells[y][i]);
            }
        }
    }
}

Board_bitboard::Board_bitboard(const Board &board, const Problem *prob) :
    cells(prob->height, std::vector<WordType>((prob->width * CELL_BITS + WORD_BITS - 1) / WORD_BITS))
{
    for(int y = 0; y < prob->height; y++) {
        for(int x = 0; x < prob->width; x++) {
            int word_offset = (x * CELL_BITS) / WORD_BITS,
                word_rem    = (x * CELL_BITS) % WORD_BITS;
            cells[y][word_offset] 
                |= (WordType)board.cells[y][x] << (WORD_BITS - CELL_BITS - word_rem);
        }
    }
}

Board Board_bitboard::toBoard(const Problem &prob) const {
    Board board(prob.width, prob.height);
    for(int y = 0; y < prob.height; y++) {
        for(int x = 0; x < prob.width; x++) {
            int word_offset = (x * CELL_BITS) / WORD_BITS,
                word_rem    = (x * CELL_BITS) % WORD_BITS;
            board.cells[y][x] 
                = (cells[y][word_offset] >> (WORD_BITS - CELL_BITS - word_rem)) & (((WordType)1 << CELL_BITS) - 1);
        }
    }

    return board;
}

void Board_bitboard::advance(const Stencil_bitboard &stenc, int x, int y, int s) {
    int y_start = std::max(0, y),
        y_end   = std::min(stenc.prob->height, y + stenc.height);
    for(int yi = y_start; yi < y_end; yi++) {
        const auto &stenc_mask = stenc.cellsTable[x - stenc.xMin()][yi - y];
        int words_count = (stenc.prob->width * CELL_BITS + WORD_BITS - 1) / WORD_BITS;
        int left_pos = 0,
            right_pos = 0;
        if(s == 2) {
            left_pos = 0,
            right_pos = CELL_BITS * stenc.prob->width - stenc.oneBitsTable[x - stenc.xMin()][yi - y];
        }
        else if(s == 3) {
            left_pos = 0,
            right_pos = stenc.oneBitsTable[x - stenc.xMin()][yi - y];
        }
        std::vector<WordType> result(words_count);
        for(int i = 0; i < words_count; i++) {
            int mask_rem = std::min(WORD_BITS, stenc.prob->width * CELL_BITS - WORD_BITS * (i + 1));
            WordType mask = stenc_mask[i];
            WordType reversed_mask = ~mask & ((~(WordType)0) << (WORD_BITS - mask_rem));

            if(s == 2) {
                WordType left  = _pext_u64(cells[yi][i], reversed_mask);
                WordType right = _pext_u64(cells[yi][i], mask);
                int left_bits  = std::__popcount(reversed_mask),
                    right_bits = std::__popcount(mask);

                int left_word_offset = left_pos / WORD_BITS,
                    left_word_rem    = left_pos % WORD_BITS;
                result[left_word_offset] |= left << (WORD_BITS - left_bits - left_word_rem);
                if((left_pos + left_bits - 1) / WORD_BITS != left_pos / WORD_BITS) {
                    result[left_word_offset + 1] 
                        |= left << (WORD_BITS - left_bits - left_word_rem + WORD_BITS);
                }
                left_pos += left_bits;

                int right_word_offset = right_pos / WORD_BITS,
                    right_word_rem    = right_pos % WORD_BITS;
                result[right_word_offset] |= right << (WORD_BITS - right_bits - right_word_rem);
                if((right_pos + right_bits - 1) / WORD_BITS != right_pos / WORD_BITS) {
                    result[right_word_offset + 1]
                        |= right << (WORD_BITS - right_bits - right_word_rem + WORD_BITS);
                }
                right_pos += right_bits;
            }
            else if(s == 3) {
                WordType left  = _pext_u64(cells[yi][i], mask);
                WordType right = _pext_u64(cells[yi][i], reversed_mask);
                int left_bits  = std::__popcount(mask),
                    right_bits = std::__popcount(reversed_mask);
                
                int left_word_offset = left_pos / WORD_BITS,
                    left_word_rem    = left_pos % WORD_BITS;
                result[left_word_offset] |= left << (WORD_BITS - left_bits - left_word_rem);
                if((left_pos + left_bits - 1) / WORD_BITS != left_pos / WORD_BITS) {
                    result[left_word_offset + 1] 
                        |= left << (WORD_BITS - left_bits - left_word_rem + WORD_BITS);
                }
                left_pos += left_bits;

                int right_word_offset = right_pos / WORD_BITS,
                    right_word_rem    = right_pos % WORD_BITS;
                result[right_word_offset] |= right << (WORD_BITS - right_bits - right_word_rem);
                if((right_pos + right_bits - 1) / WORD_BITS != right_pos / WORD_BITS) {
                    result[right_word_offset + 1]
                        |= right << (WORD_BITS - right_bits - right_word_rem + WORD_BITS);
                }
                right_pos += right_bits;
            }
        }

        cells[yi].swap(result);
    }
}

Problem_bitboard::Problem_bitboard(const Problem *prob) :
    prob(prob),
    start(prob->start, prob),
    goal(prob->goal, prob),
    stencils(),
    width(prob->width),
    height(prob->height)
{
    for(auto it = prob->stencils.begin(); it != prob->stencils.end(); it++) {
        stencils.insert({it->first, Stencil_bitboard(it->second, prob)});
    }
}