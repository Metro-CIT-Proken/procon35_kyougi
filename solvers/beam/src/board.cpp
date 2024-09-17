#include "board.h"

#include <iostream>
#include <set>

#include <nlohmann/json.hpp>
using nlohmann::json;

Problem Problem::fromJson(std::istream &stream)
{
    auto data = json::parse(stream);
    auto &board = data["board"];
    int width = board["width"],
        height = board["height"];
    std::vector<std::string> start = board["start"],
        goal = board["goal"];
    Problem prob(width, height);

    for(int i = 0; i < height; i++) {
        for(int j = 0; j < width; j++) {
            prob.start.cells[i][j] = start[i][j] - '0';
            prob.goal.cells[i][j] = goal[i][j] - '0';
        }
    }

    std::vector<json> patterns = data["general"]["patterns"];
    for(int i = 0; i < patterns.size(); i++) {
        int width = patterns[i]["width"],
            height = patterns[i]["height"],
            id = patterns[i]["p"];
        std::vector<std::string> cells_str = patterns[i]["cells"];
        CellsType<char> cells(height);
        for(int j = 0; j < height; j++) {
            cells[j].resize(width);
            for(int k = 0; k < width; k++) {
                cells[j][k] = cells_str[j][k] - '0';
            }
        }
        Stencil stenc(id, cells, &prob);
        prob.stencils.emplace(id, stenc);
    }

    prob.calculateLegalActions();

    return std::move(prob);
}

void Problem::createDefaultStencils()
{
    CellsType<char> cells1x1 = {
        {1}
    };
    Stencil stenc1x1(0, cells1x1, this);
    this->stencils.emplace(0, stenc1x1);

    std::vector<std::function<bool(int x, int y)>> filters = {
        [] (int x, int y) { return true; },
        [] (int x, int y) { return y % 2 == 0; },
        [] (int x, int y) { return x % 2 == 0; }
    };
    for(int e = 1; e <= 8; e++){
        // size = 2^e
        int size = 1 << e;
        for(int i = 0; i < filters.size(); i++) {
            int id = (e - 1) * 3 + i + 1;
            CellsType<char> cells(size, std::vector<char>(size));
            for(int y = 0; y < size; y++) {
                for(int x = 0; x < size; x++) {
                    cells[y][x] = filters[i](x, y);
                }
            }
            Stencil stenc(id, cells, this);
            this->stencils.emplace(id, stenc);
        }
    }
}

void Stencil::calculateLegalActions(std::set<CellsType<int>> &excludedBoards)
{
    auto prob = this->problem;
    BoardBase<int> test_board(prob->width, prob->height);
    for(int i = 0; i < prob->height; i++) {
        for(int j = 0; j < prob->width; j++) {
            test_board.cells[i][j] = i * prob->width + j;
        }
    }
    
    this->_legalActions.clear();
    for(int y = 1 - this->height; y < this->problem->start.height; y++) {
        for(int x = 1 - this->width; x < this->problem->start.width; x++) {
            for(StencilDirection s = StencilDirection::UP; s <= StencilDirection::RIGHT; ((int &)s)++) {
                auto new_board = test_board;
                new_board.advance(*this, x, y, (StencilDirection)s);
                if(excludedBoards.count(new_board.cells) == 0) {
                    Action act{this->id, x, y, (StencilDirection)s};
                    excludedBoards.emplace(new_board.cells);
                    this->_legalActions.emplace_back(act);
                }
            }
        }
    }
}

void Problem::calculateLegalActions() {
    std::set<BoardBase<int>::CellsType> legalBoards;
    std::cerr << "calculating legal boards..." << std::endl;

    for(auto it = stencils.begin(); it != stencils.end(); it++) {
        it->second.calculateLegalActions(legalBoards);
        std::cerr << std::distance(stencils.begin(), it) << "/" << stencils.size() << std::endl;
    }
}

Problem Problem::crop(int x, int y, int width, int height) const
{
    Problem res = *this;
    res.ox = x;
    res.oy = y;
    res.width = width;
    res.height = height;

    auto &start = res.start;
    start.width = width;
    start.height = height;
    start.cells = {start.cells.begin() + y, start.cells.begin() + y + height};
    for(auto it = start.cells.begin(); it != start.cells.end(); it++) {
        *it = {it->begin() + x, it->begin() + x + width};
    }

    auto &goal = res.goal;
    goal.width = width;
    goal.height = height;
    goal.cells = {goal.cells.begin() + y, goal.cells.begin() + y + height};
    for(auto it = goal.cells.begin(); it != goal.cells.end(); it++) {
        *it = {it->begin() + x, it->begin() + x + width};
    }

    return res;
}

Problem Problem::apply(std::vector<Action> acts) const
{
    auto result = *this;
    for(auto it = acts.begin(); it != acts.end(); it++) {
        result.start.advance(result.stencils.at(it->p), it->x, it->y, it->s);
        result.goal.advance(result.stencils.at(it->p), it->x, it->y, it->s);
    }

    return std::move(result);
}