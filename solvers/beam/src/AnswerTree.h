#pragma once

#include <vector>
#include <functional>

#include "board.h"

using AnswerIndex = std::pair<int, int>;
constexpr AnswerIndex AnswerSentinel = {-1, -1};

class AnswerTree {
private:

    struct AnswerNode {
        AnswerIndex parent;
        Action action;
    };

public:

    AnswerTree(int num_threads) :
        nodes(num_threads)
    {
    }

    AnswerIndex add(int thread, const AnswerIndex &parent, const Action &action) {
        nodes[thread].emplace_back(parent, action);
        return {thread, nodes[thread].size() - 1};
    }

    std::vector<Action> build(const AnswerIndex &lastAction) const {
        std::vector<Action> answer;
        AnswerIndex p = lastAction;
        do {
            auto &nd = nodes[p.first][p.second];
            answer.push_back(nd.action);
            p = nd.parent;
        }
        while(p != AnswerSentinel);

        std::reverse(answer.begin(), answer.end());
        return answer;
    }

    std::vector<std::vector<AnswerNode>> nodes;
};