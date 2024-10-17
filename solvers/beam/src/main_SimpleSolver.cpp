#include <iostream>
#include <fstream>

#include <nlohmann/json.hpp>

#include "SimpleSolver.h"

int main(int argc, char **argv) {
    std::cerr << argv[1] << std::endl;
    std::ifstream f(argv[1]);
    auto prob = Problem::fromJson(f, false);
    std::vector<Action> answer;

    SimpleSolver solver_simple;
    auto answer_simple = solver_simple.solve(*prob);
    answer.insert(answer.end(), answer_simple.begin(), answer_simple.end());

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
    std::cout << answer_json.dump() << std::endl;
}