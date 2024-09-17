#include "VDivideSolver.h"
#include "BeamSolver.h"

std::vector<Action> VDivideSolver::solve(const Problem &prob)
{
    int lines_per_once = (cells_per_once + prob.width - 1) / prob.width;
    InboundChokudaiBeamSolver insolver(3, 10 * prob.width * prob.height);
    std::vector<Action> result;

    Problem cur_prob = prob;

    for(int l = 0; l < prob.height; l += lines_per_once) {
        int lines = std::min(lines_per_once, prob.width - l);
        auto cropped_prob = cur_prob.crop(0, l, prob.width, lines);
        auto cropped_answer = insolver.solve(cropped_prob);

        std::vector<Action> answer(cropped_answer);
        for(auto it = answer.begin(); it != answer.end(); it++) {
            it->x += cropped_prob.ox;
            it->y += cropped_prob.oy;
        }

        result.insert(result.end(), answer.begin(), answer.end());
        cur_prob = cur_prob.apply(answer);
    }

    return result;
}