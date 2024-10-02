#include "VDivideSolver.h"
#include "BeamSolver.h"

std::vector<Action> VDivideSolver::solve(const Problem &prob)
{
    int lines_per_once = (cells_per_once + prob.width - 1) / prob.width;
    BeamSolver insolver(30, 10 * prob.width * prob.height);
    std::vector<Action> result;

    Problem cur_prob = prob;

    for(int l = 0; l < prob.height; l += lines_per_once) {
        int lines = std::min(lines_per_once, prob.height - l);
        auto cropped_prob = cur_prob.crop(0, l, prob.width, lines);
        cropped_prob->calculateLegalActions(true);
        auto cropped_answer = insolver.solve(*cropped_prob);

        std::vector<Action> answer(cropped_answer);
        for(auto it = answer.begin(); it != answer.end(); it++) {
            it->x += cropped_prob->ox;
            it->y += cropped_prob->oy;
        }

        result.insert(result.end(), answer.begin(), answer.end());
        for(auto it = answer.begin(); it != answer.end(); it++) {
            cur_prob.start.advance(cur_prob.stencils.at(it->p), it->x, it->y, it->s);
        }
    }

    return result;
}