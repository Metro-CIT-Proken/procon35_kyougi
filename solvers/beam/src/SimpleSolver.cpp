#include "SimpleSolver.h"
#include "bitset"
#include <iostream>
#include <vector>
#include <algorithm>
SimpleSolver::SimpleSolver()
{
}

std::vector<Action> SimpleSolver::solve(const Problem &prob)
{
    Board sboard = prob.start;
    Board gboard = prob.goal;
    std::vector<Action> act;
    int h = sboard.height;
    int w = sboard.width;
    int count = 0;
    for (int l = 0; l < h; l++)
    {
        for (int g = 0; g < w; g++)
        {
            if (sboard.cells[l][g] == gboard.cells[l][g])
            {
                continue;
            }
            count += 1;
            std::vector<std::pair<int, std::pair<int, int>>> pic;
            for (int j = g + 1; j < w; j++)
            {
                if (sboard.cells[l][j] == gboard.cells[l][g])
                {
                    std::bitset<8> bitj(j - g);
                    int sizej = bitj.count();
                    // if (bitj.count() >= 3)
                    if (false)
                    {
                        int y = 0;
                        int s = 0;
                        for (int x = 1; x < 257; x *= 2)
                        {
                            if (x >= w || w - x - g - 1 < 0)
                            {
                                pic.push_back({bitj.count(), {l, j}});
                                break;
                            }
                            if (x >= j - g)
                            {
                                y = w - x - g - 1;
                                std::cerr << y << std::endl;
                                sizej = 2;
                                pic.push_back({sizej, {std::min(-1, -l), j}});
                                break;
                            }
                        }

                        continue;
                    }
                    pic.push_back({bitj.count(), {l, j}});
                }
            }
            for (int i = l + 1; i < h; i++)
            {
                for (int j = 0; j < w; j++)
                {

                    if (sboard.cells[i][j] == gboard.cells[l][g])
                    {
                        std::pair<int, int> ij;
                        std::bitset<8> biti(i - l);

                        int sizei = biti.count();

                        if (l == 0)
                        {
                            sizei = 0;
                        }

                        if (j != g)
                            sizei += 1;

                        int a = sizei;
                        ij = {i, j};
                        pic.push_back({a, {ij}});
                    }
                }
            }

            std::sort(pic.begin(), pic.end());
            auto q = pic[0];
            if (q.first > 2)
            {
                std::cerr << "over 2 count" << q.first << std::endl;
            }
            auto chose = pic[0].second;
            int i, j, I;
            std::tie(I, j) = chose;
            i = abs(I);
            std::bitset<8> biti(i - l);
            int get = sboard.cells[i][j];
            if (i == l)
            {
                if (i == I)
                {
                    std::bitset<8> bitj(j - g);
                    int jj = j - g;

                    for (int x = 0; x < 9; x++)
                    {
                        if (bitj[x])
                        {
                            auto &stenc = prob.stencils.at(std::max(0, -1 + 3 * x));

                            sboard.advance(stenc, g + jj - stenc.width, l, StencilDirection::LEFT);
                            act.push_back({stenc.id, g + jj - stenc.width, l, StencilDirection::LEFT});

                            jj -= stenc.height;
                        }
                    }
                }
                else
                {
                    int y = 0;
                    int s = 0;
                    int z = 0;
                    for (int x = 1; x < 257; x *= 2)
                    {
                        if (x >= j - g)
                        {
                            y = w - x - g - 1;
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

                    auto &stenc = prob.stencils.at(std::max(0, -1 + 3 * s));
                    sboard.advance(stenc, j + y + 1 - stenc.height, l, StencilDirection::LEFT);
                    act.push_back({stenc.id, j + y + 1 - stenc.height, l, StencilDirection::LEFT});

                    auto &stenc2 = prob.stencils.at(std::max(0, -1 + 3 * z));
                    sboard.advance(stenc2, g, l, StencilDirection::LEFT);
                    act.push_back({stenc2.id, g, l, StencilDirection::LEFT});

                    std::cerr << "use X_lian_fast_seter " << std::endl;
                }
            }
            else if (j != g)
            {
                int s = -1;
                int rm = 1;
                for (int w = 0; w < 9; w++)
                {
                    if (j < g)
                    {
                        if (sboard.width - g <= rm)
                        {
                            s = w;
                            break;
                        }
                    }
                    else
                    {
                        if (g + 1 <= rm)
                        {
                            s = w;
                            break;
                        }
                    }
                    rm *= 2;
                }
                auto &stenc = prob.stencils.at(std::max(0, -1 + 3 * s));
                if (j < g)
                {
                    sboard.advance(stenc, j - stenc.height + sboard.width - g, i, StencilDirection::LEFT);
                    act.push_back({stenc.id, j - stenc.height + sboard.width - g, i, StencilDirection::LEFT});
                }
                else
                {
                    sboard.advance(stenc, j - g, i, StencilDirection::RIGHT);
                    act.push_back({stenc.id, j - g, i, StencilDirection::RIGHT});
                }
            }
            int ii = i;
            if (l != 0)
            {
                for (int y = 0; y < 9; y++)
                {
                    if (biti[y])
                    {
                        auto &stenc = prob.stencils.at(3 * y);
                        if (ii == l)
                            break;

                        sboard.advance(stenc, g, ii - stenc.height, StencilDirection::UP);
                        act.push_back({stenc.id, g, ii - stenc.height, StencilDirection::UP});
                        ii -= stenc.height;
                    }
                }
                // auto &stenc = prob.stencils.at(0);
                // sboard.advance(stenc,g, l, StencilDirection::UP);
                // act.push_back({stenc.id, g, l, StencilDirection::UP});
            }
            else
            {
                auto &stenc = prob.stencils.at(0);
                sboard.advance(stenc, g, i, StencilDirection::DOWN);
                act.push_back({stenc.id, g, i, StencilDirection::DOWN});
            }
            if (sboard.cells[l][g] != gboard.cells[l][g])
                std::cerr << "error" << l << " " << g << std::endl;
        }
        std::cerr << "line" << l << "finshed" << std::endl;
    }
    std::cerr << act.size() << std::endl;
    std::cerr << "count" << count << std::endl;
    for (int i = 0; i < h; i++)
    {
        if (sboard.cells[i] != gboard.cells[i])
            std::cerr << i << " ";
    }
    return act;
}
// auto &stenc = prob.stencils.at(0);
// sboard.advance(stenc, 3, 3, StencilDirection::DOWN);
// act.push_back({stenc.id, 3, 3, StencilDirection::DOWN});
