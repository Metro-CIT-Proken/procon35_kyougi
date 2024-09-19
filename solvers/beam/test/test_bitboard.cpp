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
        "width": 64,
        "height": 4,
        "start": [
            "1320122231212120103031233010303122012133122221020032333032113130",
            "2122122001220010102121323123131311000033120030000323232121033231",
            "1113311131233130020310020002303323300031330202003011021002323013",
            "1130032030111121322203003210323102323213223103020103100223131130"
        ],
        "goal": [
            "1320122231212120103031233010303122012133122221020032333032113130",
            "0211022001220121302121323120321311000033120030000323232121133231",
            "2233310130233111010312012000310332330003133020200301102103032301",
            "0103112102203032112230310300131032310232321322310302010310122313"
        ]
    },
    "general": {
        "n": 2,
        "patterns": [
            {
                "p": 26,
                "width": 3,
                "height": 3,
                "cells": [
                    "011",
                    "110",
                    "011"
                ]
            },
            {
                "p": 27,
                "width": 5,
                "height": 4,
                "cells": [
                    "0010",
                    "1000",
                    "0101",
                    "0001",
                    "1100"
                ]
            }
        ]
    }
}


)";
    std::stringstream ss(json_str);
    auto prob = Problem::fromJson(ss);
    Problem_bitboard bprob(prob.get());

    {
        Board_bitboard bboard(prob->start, prob.get());
        Stencil_bitboard bstenc(prob->stencils.at(27), prob.get());
        bboard.advance(bstenc, 0, 0, 2);
        auto produced = bboard.toBoard(*prob).cells;

        auto board = prob->start;
        board.advance(prob->stencils.at(27), 0, 0, StencilDirection::LEFT);
        auto expected = board.cells;

        if(!TEST_CHECK(expected == produced)) {
            std::cout << std::endl;
            print_board(expected, produced);
        }
    }

    {
        Board_bitboard bboard(prob->start, prob.get());
        Stencil_bitboard bstenc(prob->stencils.at(27), prob.get());
        bboard.advance(bstenc, 0, 0, 3);
        auto produced = bboard.toBoard(*prob).cells;

        auto board = prob->start;
        board.advance(prob->stencils.at(27), 0, 0, StencilDirection::RIGHT);
        auto expected = board.cells;

        if(!TEST_CHECK(expected == produced)) {
            std::cout << std::endl;
            print_board(expected, produced);
        }
    }

    {
        Board_bitboard bboard(prob->start, prob.get());
        Stencil_bitboard bstenc(prob->stencils.at(27), prob.get());
        bboard.advance(bstenc, 4, 4, 3);
        auto produced = bboard.toBoard(*prob).cells;

        auto board = prob->start;
        board.advance(prob->stencils.at(27), 4, 4, StencilDirection::RIGHT);
        auto expected = board.cells;

        if(!TEST_CHECK(expected == produced)) {
            std::cout << std::endl;
            print_board(expected, produced);
        }
    }

    {
        Board_bitboard bboard(prob->start, prob.get());
        Stencil_bitboard bstenc(prob->stencils.at(27), prob.get());
        bboard.advance(bstenc, -2, -2, 3);
        auto produced = bboard.toBoard(*prob).cells;

        auto board = prob->start;
        board.advance(prob->stencils.at(27), -2, -2, StencilDirection::RIGHT);
        auto expected = board.cells;

        if(!TEST_CHECK(expected == produced)) {
            std::cout << std::endl;
            print_board(expected, produced);
        }
    }

    {
        Board_bitboard bboard(prob->start, prob.get());
        for(int y = 0; y < prob->height; y++) {
            for(int x = 0; x < prob->width; x++) {
                TEST_CHECK(bboard.getCell(x, y) == prob->start.cells[y][x]);
            }
        }
    }

    {
        for(auto it_p = prob->stencils.begin(); it_p != prob->stencils.end(); it_p++) {
            auto &acts = it_p->second.legalActions();
            for(auto it_act = acts.begin(); it_act != acts.end(); it_act++) {
                if(it_act->s != StencilDirection::LEFT &&
                    it_act->s != StencilDirection::RIGHT)
                {
                    continue;
                }
                auto board = prob->start;
                board.advance(prob->stencils.at(it_act->p), it_act->x, it_act->y, it_act->s);
                Board_bitboard bboard(prob->start, prob.get());
                bboard.advance(bprob.stencils.at(it_act->p), it_act->x, it_act->y, it_act->s);

                auto produced = bboard.toBoard(*prob).cells;
                auto expected = board.cells;
                if(!TEST_CHECK(expected == produced)) {
                    TEST_MSG("p %d xy %d %d s %d", it_act->p, it_act->x, it_act->y, it_act->s);
                    print_board(expected, produced);
                    std::cout << std::endl;
                }
            }
        }
    }
}

TEST_LIST = {
    {"bitboard", test_bitboard},
    {nullptr, nullptr}
};