#include "board.h"

#include <iostream>
#include <set>
#include <memory>

#include <nlohmann/json.hpp>
using nlohmann::json;

std::shared_ptr<Problem> Problem::fromJson(std::istream &stream, bool calculateLegalAction)
{
    auto data = json::parse(stream);
    auto &board = data["board"];
    int width = board["width"],
        height = board["height"];
    std::vector<std::string> start = board["start"],
        goal = board["goal"];
    std::shared_ptr<Problem> prob = std::make_shared<Problem>(width, height);

    for(int i = 0; i < height; i++) {
        for(int j = 0; j < width; j++) {
            prob->start.cells[i][j] = start[i][j] - '0';
            prob->goal.cells[i][j] = goal[i][j] - '0';
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
        Stencil stenc(id, cells, prob.get());
        prob->stencils.emplace(id, stenc);
    }

    if(calculateLegalAction) {
        prob->calculateLegalActions();
    }

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

void Stencil::calculateLegalActions(std::set<CellsType<int>> &excludedBoards, bool onlyLR)
{
    // 前に計算した合法手があればそれを使う
    static std::map<std::tuple<int, int, int, int, bool, bool>, std::vector<Action>> legalActionCache;
    decltype(legalActionCache)::key_type cache_key = 
        {problem->width, problem->height, problem->id, id, problem->oy != 0, onlyLR};
    if(legalActionCache.count(cache_key)) {
        std::cerr << "cached" << std::endl;
        _legalActions = &legalActionCache[cache_key];
        return;
    }

    auto prob = this->problem;
    BoardBase<int> test_board(prob->width, prob->height);
    for(int i = 0; i < prob->height; i++) {
        for(int j = 0; j < prob->width; j++) {
            test_board.cells[i][j] = i * prob->width + j;
        }
    }

    excludedBoards.emplace(test_board.cells);
    auto &legalActions = legalActionCache[cache_key];
    _legalActions = &legalActions;

    // 問題がcropされていたらyを0から始める
    int y_start = problem->oy == 0 ?
        1 - this->height : 0;
    for(int y = y_start; y < this->problem->height; y++) {
        for(int x = 1 - this->width; x < this->problem->width; x++) {
            std::vector<StencilDirection> directs;
            if(onlyLR) {
                directs = {
                    StencilDirection::LEFT,
                    StencilDirection::RIGHT
                };
            }
            else {
                directs = {
                    StencilDirection::UP,
                    StencilDirection::DOWN,
                    StencilDirection::LEFT,
                    StencilDirection::RIGHT
                };
            }
            for(const StencilDirection &s : directs) {
                auto new_board = test_board;
                new_board.advance(*this, x, y, s);
                if(excludedBoards.count(new_board.cells) == 0) {
                    Action act{this->id, x, y, s};
                    excludedBoards.emplace(new_board.cells);
                    legalActions.emplace_back(act);
                }
            }
        }
    }
}

void Problem::calculateLegalActions(bool onlyLR) {
    std::set<BoardBase<int>::CellsType> excludedBoards;
    std::cerr << "calculating legal boards..." << std::endl;

    for(auto it = stencils.begin(); it != stencils.end(); it++) {
        it->second.calculateLegalActions(excludedBoards, onlyLR);
        std::cerr << std::distance(stencils.begin(), it) << "/" << stencils.size() << std::endl;
    }
}

std::shared_ptr<Problem> Problem::crop(int x, int y, int width, int height) const
{
    auto res = std::make_shared<Problem>(*this);
    res->ox = x;
    res->oy = y;
    res->width = width;
    res->height = height;

    auto &start = res->start;
    start.width = width;
    start.height = height;
    start.cells = {start.cells.begin() + y, start.cells.begin() + y + height};
    for(auto it = start.cells.begin(); it != start.cells.end(); it++) {
        *it = {it->begin() + x, it->begin() + x + width};
    }

    auto &goal = res->goal;
    goal.width = width;
    goal.height = height;
    goal.cells = {goal.cells.begin() + y, goal.cells.begin() + y + height};
    for(auto it = goal.cells.begin(); it != goal.cells.end(); it++) {
        *it = {it->begin() + x, it->begin() + x + width};
    }

    for(auto it = res->stencils.begin(); it != res->stencils.end(); it++) {
        it->second.problem = res.get();
    }

    return res;
}