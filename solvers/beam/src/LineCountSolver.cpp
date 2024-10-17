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
        for (int i = 0; i < 4; i++)
        {
            if (lans[i] > 0)
                count += lans[i];
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

                                int sizei = biti.count();

                                if (sizei >= 3)
                                {
                                    int y = 0;
                                    int s = 0;
                                    for (int x = 1; x < 257; x *= 2)
                                    {
                                        if (x >= i - l - 1)
                                        {
                                            y = h - x - l - 2;
                                            // std::cerr << "x " << x << " y " << y << std::endl;
                                            break;
                                        }
                                    }
                                    // if (i - l - 1 + y > y)
                                    // {
                                    sizei = 2;
                                    if (j != v.second)
                                        sizei += 1;
                                    if (a == -1 || a > sizei)
                                    {
                                        a = sizei;
                                        // std::cerr << a << std::endl;
                                        ij = {{-i, j}, v};
                                    }
                                    continue;
                                }

                                if (j != v.second)
                                    sizei += 1;
                                if (a == -1 || a > sizei)
                                {
                                    a = sizei;
                                    ij = {{i, j}, v};
                                }
                            }
                            pic.push_back({a, {ij}});
                        }
                    }
                }
            }

            std::sort(pic.begin(), pic.end());
            // auto q = pic[0];
            auto chose = pic[0].second;
            int i, j;
            int I;
            std::tie(I, j) = chose.first;
            i = abs(I);
            // std::cerr << "count " << pic[0].first << "i y " << I << " " << j << std::endl;

            std::bitset<8> biti(i - chose.second.first - 1);
            // int get = sboard.cells[i][j];
            // lans[sboard.cells[i][j]] += 1;

            // for (auto q : pic)
            // {
            // std::cerr << q.first << " " << q.second.first.first << " " << q.second.first.second << std::endl;
            // }
            auto q = pic[0];

            // std::cerr << q.first << " " << q.second.first.first << " " << q.second.first.second << std::endl;
            // std::cin.get();
            if (j != chose.second.second)
            {
                int s = -1;
                int rm = 1;
                for (int w = 0; w < 9; w++)
                {
                    if (j < chose.second.second)
                    {
                        if (sboard.width - chose.second.second <= rm)
                        {
                            s = w;
                            break;
                        }
                    }
                    else
                    {
                        if (chose.second.second + 1 <= rm)
                        {
                            s = w;
                            break;
                        }
                    }
                    rm *= 2;
                }
                // s += 1;
                auto &stenc = prob.stencils.at(std::max(0, -1 + 3 * s));
                if (j < chose.second.second)
                {
                    sboard.advance(stenc, j - stenc.height + sboard.width - chose.second.second, i, StencilDirection::LEFT);
                    act.push_back({stenc.id, j - stenc.height + sboard.width - chose.second.second, i, StencilDirection::LEFT});
                }
                else
                {
                    sboard.advance(stenc, j - chose.second.second, i, StencilDirection::RIGHT);
                    act.push_back({stenc.id, j - chose.second.second, i, StencilDirection::RIGHT});
                }
            }
            int ii = i;
            if (l != 0 && I > 0)
            {
                for (int y = 0; y < 9; y++)
                {
                    if (biti[y])
                    {
                        auto &stenc = prob.stencils.at(3 * y);
                        if (ii == chose.second.first + 1)
                            break;

                        sboard.advance(stenc, chose.second.second, ii - stenc.height, StencilDirection::UP);
                        act.push_back({stenc.id, chose.second.second, ii - stenc.height, StencilDirection::UP});
                        std::cout << "up " << stenc.height << " ";
                        ii -= stenc.height;
                    }
                }
                auto &stenc = prob.stencils.at(0);
                sboard.advance(stenc, chose.second.second, chose.second.first, StencilDirection::UP);
                act.push_back({stenc.id, chose.second.second, chose.second.first, StencilDirection::UP});
            }
            else if (I < 0)
            {
                i = std::abs(i);
                int y = 0;
                int s = 0;
                int z = 0;
                // int Z = 0;
                for (int x = 1; x < 257; x *= 2)
                {
                    if (x >= i - l - 1)
                    {
                        y = h - x - l - 2;
                        break;
                    }
                    z++;
                }
                for (int x = 1; x < 257; x *= 2)
                {
                    if (x >= y + 1)
                    {
                        break;
                    }
                    s++;
                }
                for (auto q : sboard.cells)
                {
                    for (auto p : q)
                        std::cerr << int(p) << "";
                    std::cout << std::endl;
                }
                // std::bitset<8> bits(s);
                auto &stenc = prob.stencils.at(3 * s);
                std::cout << "s " << s << " " << stenc.height << std::endl;
                sboard.advance(stenc, chose.second.second, i + y + 1 - stenc.height, StencilDirection::UP);
                act.push_back({stenc.id, chose.second.second, i + y + 1 - stenc.height, StencilDirection::UP});
                // for (auto q : sboard.cells)
                // {
                //     for (auto p : q)
                //         std::cerr << int(p) << "";
                //     std::cout << std::endl;
                // }
                // std::cout << "s " << s << std::endl;
                auto &stenc2 = prob.stencils.at(3 * z);
                sboard.advance(stenc2, chose.second.second, l + 1, StencilDirection::UP);
                act.push_back({stenc2.id, chose.second.second, l + 1, StencilDirection::UP});
                // for (auto q : sboard.cells)
                // {
                //     for (auto p : q)
                //         std::cerr << int(p) << "";
                //     std::cout << std::endl;
                // }
                // std::cout << "s " << s << std::endl;
                auto &stenc3 = prob.stencils.at(0);
                sboard.advance(stenc3, chose.second.second, chose.second.first, StencilDirection::UP);
                act.push_back({stenc3.id, chose.second.second, chose.second.first, StencilDirection::UP});
                // for (auto q : sboard.cells)
                // {
                //     for (auto p : q)
                //         std::cerr << int(p) << "";
                //     std::cout << std::endl;
                // }
                // std::cout << std::endl;
                // std::cin.get();
                std::cerr << "use y_lian_fast_seter " ;
            }
            else
            {
                auto &stenc = prob.stencils.at(0);
                sboard.advance(stenc, chose.second.second, i, StencilDirection::DOWN);
                act.push_back({stenc.id, chose.second.second, i, StencilDirection::DOWN});
            }
        }
        std::cerr << "line" << l << "finshed" << std::endl;
    }
    std::cerr << act.size() << std::endl;
    std::cerr << "count" << count << std::endl;
    return act;
}
// auto &stenc = prob.stencils.at(0);
// sboard.advance(stenc, 3, 3, StencilDirection::DOWN);
// act.push_back({stenc.id, 3, 3, StencilDirection::DOWN});
