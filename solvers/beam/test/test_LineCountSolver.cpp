#include <sstream>
#include <string>

#include <acutest.h>

#include "../src/board.h"
#include "../src/LineCountSolver.h"

void print_board(const Board &expected)
{
    for(int i = 0; i < expected.height; i++) {
        for(int j = 0; j < expected.width; j++) {
            std::cout << (int)expected.cells[i][j] << " \n"[j + 1 == expected.cells[0].size()];
        }
    }
    std::cout << std::endl;
}

void test_LineCountSolver() {
    std::string json_str = R"(
{
    "board": {
        "width": 8,
        "height": 8,
        "start": [
            "32110012",
            "03333012",
            "10311202",
            "01013021",
            "23232032",
            "33320202",
            "33203310",
            "20120203"
        ],
        "goal": [
            "01032100",
            "23322301",
            "12321003",
            "13210230",
            "00110233",
            "23022312",
            "03333201",
            "03212230"
        ]
    },
    "general": {
        "n": 2,
        "patterns": [
            {
                "p": 26,
                "width": 4,
                "height": 4,
                "cells": [
                    "1000",
                    "1010",
                    "1011",
                    "0100"
                ]
            },
            {
                "p": 27,
                "width": 5,
                "height": 4,
                "cells": [
                    "11000",
                    "10011",
                    "11100",
                    "01001"
                ]
            }
        ]
    }
}
)";
    std::stringstream ss(json_str);
    auto prob = Problem::fromJson(ss);

    LineCountSolver solver;
    auto answer = solver.solve(*prob);

    auto board = prob->start;
    for(auto it = answer.begin(); it != answer.end(); it++) {
        board.advance(prob->stencils.at(it->p), it->x, it->y, it->s);
    }

    auto goal = prob->goal;
    for(int y = 0; y < prob->height; y++) {
        std::map<int, int> cnt_cur, cnt_goal;
        for(int x = 0; x < prob->width; x++) {
            cnt_cur[board.cells[y][x]]++;
            cnt_goal[goal.cells[y][x]]++;
        }
        if(!TEST_CHECK(cnt_cur == cnt_goal)) {
            TEST_MSG("Failed at line %d", y);
            TEST_MSG("board:");
            print_board(board);
            TEST_MSG("answer:");
            for(auto it = answer.begin(); it != answer.end(); it++) {
                TEST_MSG("p %d xy %d %d s %d",
                    it->p, it->x, it->y, it->s);
            }
            return;
        }
    }
}

TEST_LIST = {
    {"LineCountSolver", test_LineCountSolver},
    {nullptr, nullptr}
};