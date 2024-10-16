#pragma once

#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <set>
#include <memory>

template<typename CellValueType>
using CellsType = std::vector<std::vector<CellValueType>>;

class Problem;

enum StencilDirection : int {
    UP = 0, DOWN, LEFT, RIGHT
};

struct Action
{
    int p, x, y;
    StencilDirection s;
};

class Stencil
{
public:
    Stencil(int id, const CellsType<char> &cells, const Problem *prob) : 
        id(id), 
        height(cells.size()),
        width(cells.size() == 0 ? 0 : cells[0].size()), 
        cells(cells), 
        problem(prob)
    {
    }

    bool isDefaultH() const
    {
        return this->id == 0 ||
            this->id < 25 && (this->id - 2) % 3 == 0;
    }

    bool isDefaultV() const
    {
        return this->id == 0 ||
            this->id < 25 && (this->id - 3) % 3 == 0; 
    }

    bool isDefaultA() const
    {
        return this->id == 0 ||
            this->id < 25 && (this->id - 1) % 3 == 0; 
    }

    bool isDefault() const
    {
        return this->id < 25;
    }

    const int width, height;
    const int id;
    const Problem *problem;
    const std::vector<std::vector<char>> cells;

    const std::vector<Action> &legalActions() const
    {
        return *this->_legalActions;
    }

    void calculateLegalActions(std::set<CellsType<int>> &excluded, bool onlyLR);

private:
    const std::vector<Action> *_legalActions;
};

template<class CellValueType>
class BoardBase
{
public:
    using CellsType = std::vector<std::vector<CellValueType>>;

    BoardBase(int w, int h) : 
        width(w), 
        height(h), 
        cells(h, std::vector<CellValueType>(w))
    {
    }

    void advance(const Stencil &stenc, int x, int y, StencilDirection direction)
    {
        int x_start = std::max(0, x),
            x_end = std::min(this->width, x + stenc.width),
            y_start = std::max(0, y),
            y_end = std::min(this->height, y + stenc.height);
        if(direction == StencilDirection::UP) {
            for(int tx = x_start; tx < x_end; tx++) {
                std::vector<CellValueType> pushed_cells, float_cells;
                for(int ty = y_start; ty < this->height; ty++) {
                    if(ty - y < stenc.height && tx - x < stenc.width && stenc.cells[ty - y][tx - x]) {
                        float_cells.push_back(this->cells[ty][tx]);
                    }
                    else {
                        pushed_cells.push_back(this->cells[ty][tx]);
                    }
                }
                int i = y_start;
                for(int j = 0; j < pushed_cells.size(); j++) {
                    this->cells[i][tx] = pushed_cells[j];
                    i++;
                }
                for(int j = 0; j < float_cells.size(); j++) {
                    this->cells[i][tx] = float_cells[j];
                    i++;
                }
            }
        }
        else if(direction == StencilDirection::DOWN) {
            for(int tx = x_start; tx < x_end; tx++) {
                std::vector<CellValueType> pushed_cells, float_cells;
                for(int ty = 0; ty < y_end; ty++) {
                    int px = tx - x,
                        py = ty - y;
                    if(py >= 0 && py < stenc.height && px >= 0 && px < stenc.width && stenc.cells[py][px]) {
                        float_cells.push_back(this->cells[ty][tx]);
                    }
                    else {
                        pushed_cells.push_back(this->cells[ty][tx]);
                    }
                }
                int i = 0;
                for(int j = 0; j < float_cells.size(); j++) {
                    this->cells[i][tx] = float_cells[j];
                    i++;
                }
                for(int j = 0; j < pushed_cells.size(); j++) {
                    this->cells[i][tx] = pushed_cells[j];
                    i++;
                }
            }
        }
        else if(direction == StencilDirection::LEFT) {
            for(int ty = y_start; ty < y_end; ty++) {
                std::vector<CellValueType> pushed_cells, float_cells;
                for(int tx = x_start; tx < this->width; tx++) {
                    int px = tx - x,
                        py = ty - y;
                    if(py < stenc.height && px < stenc.width && stenc.cells[py][px]) {
                        float_cells.push_back(this->cells[ty][tx]);
                    }
                    else {
                        pushed_cells.push_back(this->cells[ty][tx]);
                    }
                }
                int i = x_start;
                for(int j = 0; j < pushed_cells.size(); j++) {
                    this->cells[ty][i] = pushed_cells[j];
                    i++;
                }
                for(int j = 0; j < float_cells.size(); j++) {
                    this->cells[ty][i] = float_cells[j];
                    i++;
                }
            }
        }
        else if(direction == StencilDirection::RIGHT) {
            for(int ty = y_start; ty < y_end; ty++) {
                std::vector<CellValueType> pushed_cells, float_cells;
                for(int tx = 0; tx < x_end; tx++) {
                    int px = tx - x,
                        py = ty - y;
                    if(py >= 0 && px >= 0 && stenc.cells[py][px]) {
                        float_cells.push_back(this->cells[ty][tx]);
                    }
                    else {
                        pushed_cells.push_back(this->cells[ty][tx]);
                    }
                }
                int i = 0;
                for(int j = 0; j < float_cells.size(); j++) {
                    this->cells[ty][i] = float_cells[j];
                    i++;
                }
                for(int j = 0; j < pushed_cells.size(); j++) {
                    this->cells[ty][i] = pushed_cells[j];
                    i++;
                }
            }
        }
    }

    int width, height;
    CellsType cells;
};
using Board = BoardBase<char>;

class Problem
{
public:
    Problem(int w, int h) : 
        width(w), 
        height(h), 
        start(w, h), 
        goal(w, h),
        ox(0),
        oy(0)
    {
        createDefaultStencils();

        static int nextProblemId;
        id = nextProblemId;
        nextProblemId++;
    }

    void createDefaultStencils();

    static std::shared_ptr<Problem> fromJson(std::istream &, bool calculateLegalAction = true);

    void calculateLegalActions(bool onlyLR = false);

    std::shared_ptr<Problem> crop(int x, int y, int width, int height) const;

    Board start, goal;
    int width, height;
    int ox, oy;
    std::map<int, Stencil> stencils;
    int id;
};