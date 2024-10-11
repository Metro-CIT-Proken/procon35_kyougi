#include "LineCountSolver.h"
#include "bitset"
#include <iostream>
#include <vector>
#include <algorithm>
LineCountSolver::LineCountSolver()
{
}

std::vector<Action> LineCountSolver::solve(const Problem &prob)
{
    Board sboard = prob.start;
    Board gboard = prob.goal;
    std::vector<Action> act;
    int h = sboard.height;
    int w = sboard.width;
    int count = 0;
    for (int l = 0; l < h; l++)
    {
        std::vector<int> lans = {0, 0, 0, 0};
        for (int i = 0; i < w; i++)
        {
            lans[sboard.cells[l][i]] += 1;
            lans[gboard.cells[l][i]] -= 1;
        }
        while (lans != std::vector<int>{0, 0, 0, 0})
        {
            std::map<int, std::vector<std::pair<int, int>>> dic;
            std::vector<std::pair<int, std::pair<std::pair<int, int>, std::pair<int, int>>>> pic;

            lans = std::vector<int>{0, 0, 0, 0};
            for (int i = 0; i < w; i++)
            {

                lans[sboard.cells[l][i]] += 1;
                lans[gboard.cells[l][i]] -= 1;
                dic[sboard.cells[l][i]].push_back(std::make_pair(l, i));
            }

            if (lans == std::vector<int>{0, 0, 0, 0})
                break;
            for (int i = l + 1; i < h; i++)
            {
                for (int j = 0; j < w; j++)
                {
                    if (lans[sboard.cells[i][j]] < 0)
                    {
                        int a = -1;
                        std::pair<std::pair<int, int>, std::pair<int, int>> ij;
                        for (int r = 0; r < 4; r++)
                        {
                            if (lans[r] <= 0)
                                continue;

                            for (int Q = 0; Q < dic[r].size(); Q++)
                            {
                                std::pair<int, int> v = dic[r][Q];
                                int count;
                                std::bitset<8> biti(i - v.first - 1);
                                std::bitset<8> bitj(std::abs(j - v.second));
                                int sizei = biti.count();
                                int sizej = bitj.count();

                                if (a == -1 || a > sizei + sizej)
                                {
                                    a = sizei + sizej;
                                    ij = {{i, j}, v};
                                }
                            }
                            pic.push_back({a, {ij}});
                        }
                    }
                }
            }

            std::sort(pic.begin(), pic.end());

            auto q = pic[0];
            auto chose = pic[0].second;
            int i, j;
            std::tie(i, j) = chose.first;
            std::bitset<8> biti(i - chose.second.first - 1);
            std::bitset<8> bitj(std::abs(j - chose.second.second));

            lans[sboard.cells[i][j]] += 1;
            for (int x = 0; x < 9; x++)
            {
                if (bitj[x])
                {
                    auto &stenc = prob.stencils.at(std::max(0, -1 + 3 * x));
                    int jj = j - chose.second.second;
                    if (jj < 0)
                    {
                        sboard.advance(stenc, chose.second.second + jj + 1, i, StencilDirection::RIGHT);
                        act.push_back({stenc.id, chose.second.second + jj + 1, i, StencilDirection::RIGHT});
                        jj += stenc.height;
                    }
                    else if (jj > 0)
                    {
                        sboard.advance(stenc, chose.second.second + jj - stenc.width, i, StencilDirection::LEFT);
                        act.push_back({stenc.id, chose.second.second + jj - stenc.width, i, StencilDirection::LEFT});

                        jj -= stenc.height;
                    }
                    else
                        break;
                }
            }
            int ii = i;
            for (int y = 0; y < 9; y++)
            {
                if (biti[y])
                {
                    auto &stenc = prob.stencils.at(3 * y);
                    if (ii == chose.second.first + 1)
                        break;

                    sboard.advance(stenc, chose.second.second, ii - stenc.height, StencilDirection::UP);
                    act.push_back({stenc.id, chose.second.second, ii - stenc.height, StencilDirection::UP});

                    ii -= stenc.height;
                }
            }
            auto &stenc = prob.stencils.at(0);

            sboard.advance(stenc, chose.second.second, chose.second.first, StencilDirection::UP);
            act.push_back({stenc.id, chose.second.second, chose.second.first, StencilDirection::UP});

        }

        std::cout << "line" << l << "finshed" << std::endl;

    }
    std::cout << act.size() << std::endl;

    return act;
}
// auto &stenc = prob.stencils.at(0);
// sboard.advance(stenc, 3, 3, StencilDirection::DOWN);
// act.push_back({stenc.id, 3, 3, StencilDirection::DOWN});
