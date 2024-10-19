#include <array>

#include "BeamEvaluator.h"

BeamEvaluatorResult BeamEvaluator::evaluate(Board_bitboard const &board) const 
{
    int eval = 0;
    bool end = false;
    int eval_r = 0,
        eval_l = 0;
    bool first_line_restored = false;
    for(int y = 0; y < problem->prob->height; y++) {
        for(int x = 0; x < problem->prob->width; x++) {
            if(board.getCell(x, y) != problem->goal.getCell(x, y)) {
                int sum_diff = 0;
                std::array<int, 4> x_start;
                std::fill(x_start.begin(), x_start.end(), x);
                int x_end = std::min(x + 1 + 8, problem->width);
                for(int tx = x; tx < x_end; tx++) {
                    int c = problem->goal.getCell(tx, y);
                    for(int sx = x_start[c]; sx < problem->width; sx++) {
                        if(board.getCell(sx, y) == c) {
                            sum_diff += std::abs(tx - sx);
                            x_start[c] = sx + 1;
                            break;
                        }
                    }
                }

                // eval_r += 1000 * (prob.width - x) - sum_diff;
                int factor = x == 0 ? 3 : 1;
                eval_r += factor * ((x_end - x) * problem->width - sum_diff);
                end = true;
                break;
            }
            eval_r += 1000000;
        }

        if(y == 0 && eval_r == 1000000 * problem->width) {
            first_line_restored = true;
        }

        for(int x = problem->prob->width - 1; x >= 0; x--) {
            if(board.getCell(x, y) != problem->goal.getCell(x, y)) {
                int sum_diff = 0;
                std::array<int, 4> x_start;
                std::fill(x_start.begin(), x_start.end(), x);
                int x_end = std::max(x - 1 - 8, 0);
                for(int tx = x; tx >= x_end; tx--) {
                    int c = problem->goal.getCell(tx, y);
                    for(int sx = x_start[c]; sx >= 0; sx--) {
                        if(board.getCell(sx, y) == c) {
                            sum_diff += std::abs(tx - sx);
                            x_start[c] = sx - 1;
                            break;
                        }
                    }
                }

                int factor = x == 0 ? 3 : 1;
                // eval_r += 1000 * (prob.width - x) - sum_diff;
                eval_l += factor * ((x - x_end) * problem->width - sum_diff);

                end = true;
                break;
            }
            eval_l += 1000000;
        }

        // if(end) {
        //     break;
        // }

        //eval += std::max(eval_r, eval_l);
    }

    eval = std::max(eval_r, eval_l);

    return {
        eval,
        first_line_restored
    };   
}