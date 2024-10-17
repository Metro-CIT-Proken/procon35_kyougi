#include <sstream>
#include <string>

#include <acutest.h>

#include "../src/board.h"

void print_board(
    const std::vector<std::vector<char>> &expected,
    const std::vector<std::vector<char>> &produced)
{
    std::cout << "Expected:" << std::endl;
    for(int i = 0; i < expected.size(); i++) {
        for(int j = 0; j < expected[0].size(); j++) {
            std::cout << (int)expected[i][j] << " \n"[j + 1 == expected[0].size()];
        }
    }
    std::cout << "Produced:" << std::endl;
    for(int i = 0; i < produced.size(); i++) {
        for(int j = 0; j < produced[0].size(); j++) {
            std::cout << (int)produced[i][j] << " \n"[j + 1 == produced[0].size()];
        }
    }
    std::cout << std::endl;
}

void test_board() {
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

    std::vector<std::vector<char>> stencil27 = {
        {1, 1, 0, 0, 0},
        {1, 0, 0, 1, 1},
        {1, 1, 1, 0, 0},
        {0, 1, 0, 0, 1}
    };
    if(!TEST_CHECK(stencil27 == prob->stencils.at(27).cells)) {
        print_board(stencil27, prob->stencils.at(27).cells);
    }

    auto up = prob->start;
    up.advance(prob->stencils.at(27), 1, 1, StencilDirection::UP);
    std::vector<std::vector<char>> up_cells = {
        {3, 2, 1, 1, 0, 0, 1, 2},
        {0, 3, 3, 3, 3, 0, 1, 2},
        {1, 3, 3, 1, 3, 0, 0, 2},
        {0, 3, 2, 3, 2, 2, 2, 1},
        {2, 0, 1, 2, 0, 3, 3, 2},
        {3, 3, 3, 0, 3, 2, 0, 2},
        {3, 0, 0, 2, 0, 2, 1, 0},
        {2, 1, 2, 1, 1, 0, 0, 3}
    };
    if(!TEST_CHECK(up.cells == up_cells)) {
        print_board(up_cells, up.cells);
    }

    auto down = prob->start;
    down.advance(prob->stencils.at(27), 1, 1, StencilDirection::DOWN);
    std::vector<std::vector<char>> down_cells = {
        {3, 3, 3, 1, 1, 2, 1, 2},
        {0, 0, 0, 1, 0, 0, 1, 2},
        {1, 1, 2, 3, 3, 0, 0, 2},
        {0, 2, 1, 1, 3, 0, 2, 1},
        {2, 3, 3, 3, 2, 0, 3, 2},
        {3, 3, 3, 2, 0, 2, 0, 2},
        {3, 3, 2, 0, 3, 3, 1, 0},
        {2, 0, 1, 2, 0, 2, 0, 3}
    };
    if(!TEST_CHECK(down_cells == down.cells)) {
        print_board(down_cells, down.cells);
    }

    auto left = prob->start;
    left.advance(prob->stencils.at(27), 1, 1, StencilDirection::LEFT);
    std::vector<std::vector<char>> left_cells = {
        {3, 2, 1, 1, 0, 0, 1, 2},
        {0, 3, 3, 0, 1, 2, 3, 3},
        {1, 3, 1, 0, 2, 0, 1, 2},
        {0, 3, 0, 2, 1, 1, 0, 1},
        {2, 3, 3, 2, 3, 2, 2, 0},
        {3, 3, 3, 2, 0, 2, 0, 2},
        {3, 3, 2, 0, 3, 3, 1, 0},
        {2, 0, 1, 2, 0, 2, 0, 3}
    };
    if(!TEST_CHECK(left_cells == left.cells)) {
        print_board(left_cells, left.cells);
    }

    auto right = prob->start;
    right.advance(prob->stencils.at(27), 1, 1, StencilDirection::RIGHT);
    std::vector<std::vector<char>> right_cells = {
        {3, 2, 1, 1, 0, 0, 1, 2},
        {3, 3, 0, 3, 3, 0, 1, 2},
        {0, 1, 2, 1, 3, 1, 0, 2},
        {1, 0, 1, 0, 3, 0, 2, 1},
        {2, 0, 2, 3, 3, 2, 3, 2},
        {3, 3, 3, 2, 0, 2, 0, 2},
        {3, 3, 2, 0, 3, 3, 1, 0},
        {2, 0, 1, 2, 0, 2, 0, 3}
    };
    if(!TEST_CHECK(right_cells == right.cells)) {
        print_board(right_cells, right.cells);
    }

    {
        auto cropped_prob = prob->crop(1, 1, 6, 6);
        int oy = cropped_prob->oy,
            ox = cropped_prob->ox;
        for(int y = 0; y < cropped_prob->height; y++) {
            for(int x = 0; x < cropped_prob->width; x++) {
                if(!TEST_CHECK(cropped_prob->start.cells[y][x] == prob->start.cells[oy + y][ox + x])) {
                    TEST_MSG("failed at (%d, %d)", x, y);
                }
                if(!TEST_CHECK(cropped_prob->goal.cells[y][x] == prob->goal.cells[oy + y][ox + x])) {
                    TEST_MSG("failed at (%d, %d)", x, y);
                }
            }
        }
    }
}

TEST_LIST = {
    {"board", test_board},
    {nullptr, nullptr}
};