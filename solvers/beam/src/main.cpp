#include <iostream>
#include <fstream>

#include <nlohmann/json.hpp>

#include "board.h"
#include "VDivideSolver.h"
#include "BeamSolver.h"
#include "LineCountSolver.h"

/*

本選までにやることリスト：
・盤面の回転
・問題生成のプログラム更新

（可能なら）
・マルチコアによる並列化
・chokudaiサーチのメモリ使用量固定

*/

int main(int argc, char **argv) {
    std::cout << argv[1] << std::endl;
    std::ifstream f(argv[1]);
    auto prob = Problem::fromJson(f, false);
    std::vector<Action> answer;

    LineCountSolver solver_lc;
    auto answer_lc = solver_lc.solve(*prob);
    for(auto const &ans : answer_lc) {
        prob->start.advance(prob->stencils.at(ans.p), ans.x, ans.y, ans.s);
    }
    answer.insert(answer.end(), answer_lc.begin(), answer_lc.end());

    VDivideSolver solver_vd(128);
    // BeamSolver solver_vd(3, 100 * prob->width * prob->height);
    // prob->calculateLegalActions();
    auto answer_vd = solver_vd.solve(*prob);
    answer.insert(answer.end(), answer_vd.begin(), answer_vd.end());

    nlohmann::json answer_json;
    answer_json["n"] = answer.size();
    for(auto it = answer.begin(); it != answer.end(); it++) {
        answer_json["ops"].push_back({
            {"p", it->p},
            {"x", it->x},
            {"y", it->y},
            {"s", it->s}
        });
    }

    std::cerr << "answer ops " << answer.size() << std::endl;
    std::ofstream output("answer.json");
    output << answer_json.dump(2);

    std::cout << answer_json.dump() << std::endl;
}