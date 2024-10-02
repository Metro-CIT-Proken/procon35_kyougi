#include <iostream>
#include <fstream>

#include <nlohmann/json.hpp>

#include "board.h"
#include "VDivideSolver.h"
#include "BeamSolver.h"

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

    VDivideSolver solver(128);
    // ChokudaiBeamSolver solver(3, 100 * prob->width * prob->height);
    // prob->calculateLegalActions();
    auto answer = solver.solve(*prob);

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
}