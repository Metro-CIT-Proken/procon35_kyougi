#include <iostream>
#include <fstream>

#include <nlohmann/json.hpp>

#include "board.h"
#include "VDivideSolver.h"

int main(int argc, char **argv) {
    std::cout << argv[1] << std::endl;
    std::ifstream f(argv[1]);
    const Problem prob = Problem::fromJson(f);

    VDivideSolver solver(32);
    auto answer = solver.solve(prob);

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