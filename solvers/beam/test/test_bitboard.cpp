#include <iostream>
#include <bitset>
#include <vector>
#include <sstream>

#include <acutest.h>

#include "../src/board.h"
#include "../src/bitboard.h"

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

void test_bitboard() {
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
    Problem prob = Problem::fromJson(ss);

    {
        Board_bitboard bboard(prob.start, &prob);
        Stencil_bitboard bstenc(prob.stencils.at(27), &prob);
        bboard.advance(bstenc, 0, 0, 2);
        auto produced = bboard.toBoard(prob).cells;

        auto board = prob.start;
        board.advance(prob.stencils.at(27), 0, 0, StencilDirection::LEFT);
        auto expected = board.cells;

        if(!TEST_CHECK(expected == produced)) {
            std::cout << std::endl;
            print_board(expected, produced);
        }
    }

    {
        Board_bitboard bboard(prob.start, &prob);
        Stencil_bitboard bstenc(prob.stencils.at(27), &prob);
        bboard.advance(bstenc, 0, 0, 3);
        auto produced = bboard.toBoard(prob).cells;

        auto board = prob.start;
        board.advance(prob.stencils.at(27), 0, 0, StencilDirection::RIGHT);
        auto expected = board.cells;

        if(!TEST_CHECK(expected == produced)) {
            std::cout << std::endl;
            print_board(expected, produced);
        }
    }

    {
        Board_bitboard bboard(prob.start, &prob);
        Stencil_bitboard bstenc(prob.stencils.at(27), &prob);
        bboard.advance(bstenc, 4, 4, 3);
        auto produced = bboard.toBoard(prob).cells;

        auto board = prob.start;
        board.advance(prob.stencils.at(27), 4, 4, StencilDirection::RIGHT);
        auto expected = board.cells;

        if(!TEST_CHECK(expected == produced)) {
            std::cout << std::endl;
            print_board(expected, produced);
        }
    }

    {
        Board_bitboard bboard(prob.start, &prob);
        Stencil_bitboard bstenc(prob.stencils.at(27), &prob);
        bboard.advance(bstenc, -2, -2, 3);
        auto produced = bboard.toBoard(prob).cells;

        auto board = prob.start;
        board.advance(prob.stencils.at(27), -2, -2, StencilDirection::RIGHT);
        auto expected = board.cells;

        if(!TEST_CHECK(expected == produced)) {
            std::cout << std::endl;
            print_board(expected, produced);
        }
    }

    {
        Board_bitboard bboard(prob.start, &prob);
        for(int y = 0; y < prob.height; y++) {
            for(int x = 0; x < prob.width; x++) {
                TEST_CHECK(bboard.getCell(x, y) == prob.start.cells[y][x]);
            }
        }
    }
}

TEST_LIST = {
    {"bitboard", test_bitboard},
    {nullptr, nullptr}
};