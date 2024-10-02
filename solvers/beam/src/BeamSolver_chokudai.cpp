#include <memory>
#include <iostream>
#include <queue>
#include <array>
#include <unordered_set>

#include <x86intrin.h>

#include "board.h"
#include "bitboard.h"
#include "BeamSolver.h"

using std::cout, std::cerr, std::endl;

std::vector<WordType> evaluateMask = {
    0x0000000000000000, // 0000...
    0x5555555555555555, // 0101...
    0xAAAAAAAAAAAAAAAA, // 1010...
    0xFFFFFFFFFFFFFFFF  // 1111...
};

static int evaluateBoard(const Problem_bitboard &prob, const Board_bitboard &board)
{
    int eval_r = 0,
        eval_l = 0;
    bool end = false;
    for(int y = 0; y < prob.prob->height; y++) {
        // for(int w = 0; w < board.wordsPerLine; w++) {
        //     auto &test_word = board.getWord(y, w),
        //         &goal_word  = prob.goal.getWord(y, w);
        //     if(test_word != goal_word) {
        //         auto diff = test_word ^ goal_word;
        //         int diff_x = _lzcnt_u64(diff) / CELL_BITS;
        //         eval += 1000 * diff_x;


        //         for(int wj = w + 1; w < board.wordsPerLine; wj++) {

        //         }

        //         end = true;
        //         break;
        //     }

        //     eval += 1000 * (WORD_BITS / CELL_BITS);
        // }



        for(int x = 0; x < prob.prob->width; x++) {
            if(board.getCell(x, y) != prob.goal.getCell(x, y)) {
                int tx = x;
                int c = prob.goal.getCell(x, y);
                while(++x <= prob.prob->width) {
                    if(c == board.getCell(x, y)) {
                        eval_r += prob.prob->width - (x - tx);
                        break;
                    }
                }

                // int dsum = 0;
                // for(int tx = x + 1; tx < prob.width; tx++) {
                //     int c = prob.goal.getCell(tx, y);
                //     for(int sx = tx + 1; sx < prob.width; sx++) {
                //         if(board.getCell(sx, y) == c) {
                //             dsum += sx - tx;
                //             break;
                //         }
                //     }
                // }

                // eval_r -= dsum / (prob.width - x);

                end = true;
                break;
            }
            eval_r += 1000;
        }

        // {
        //     int sum_diff = 0;
        //     std::array<int, 4> x_start = {};
        //     for(int x = 0; x < prob.width; x++) {
        //         int c = board.getCell(x, y);
        //         for(int sx = x_start[c]; sx < prob.width; sx++) {
        //             if(prob.goal.getCell(sx, y) == c) {
        //                 sum_diff += std::abs(sx - x);
        //                 x_start[c] = sx + 1;
        //                 break;
        //             }
        //         }
        //     }

        //     eval_r += sum_diff;
        // }

        // if(end) {
        //     break;
        // }
    }

    return eval_r;
}

std::vector<Action> ChokudaiBeamSolver::solve(const Problem &prob_normal)
{
    using std::cout, std::cerr, std::endl;

    Problem_bitboard prob(&prob_normal);
    int beam_count = 5;
    std::vector<std::priority_queue<BeamState>> beam(this->beamD + 1);
    auto board_start = std::make_shared<Board_bitboard>(prob.start);
    beam[0].push(BeamState{board_start, 0, 0, 0, 0, StencilDirection::UP, nullptr});
    int eval_max = -1;  

    std::shared_ptr<BeamState> best_state;
    int best_ops = INT32_MAX;

    // ビームの本数
    for(int bi = 0; bi < beam_count; bi++) {
        cerr << "beam " << bi << endl;
        bool should_next = false;

        // ビーム深さで探索する
        for(int di = 0; di < this->beamD; di++) {
            if(should_next) {
                break;
            }
            
            cerr << di << endl;

            auto &q = beam[di];
            auto &next_q = beam[di + 1];
            
            // ビーム幅の分だけキューから取り出して探索する
            for(int wi = 0; wi < this->beamW; wi++) {
                if(should_next || q.empty()) {
                    break;
                }

                // キューから状態を取り出す
                std::shared_ptr<BeamState> now_state(new BeamState(q.top()));
                q.pop();
                
                // 盤面が省略されているなら生成する
                if(!now_state->board) {
                    auto prev_state = now_state->prevState;
                    auto new_board = std::make_shared<Board_bitboard>(*prev_state->board);
                    new_board->advance(prob.stencils.at(now_state->p), now_state->x, now_state->y, now_state->s);
                    now_state->board = new_board;
                }

                // すべての抜き型を試す
                for(auto it_p = prob.stencils.begin(); it_p != prob.stencils.end(); it_p++) {

                    // 抜き型が有効なすべての位置を列挙する
                    auto acts = prob_normal.stencils.at(it_p->first).legalActions();
                    for(auto it_act = acts.begin(); it_act != acts.end(); it_act++) {
                        // 行で揃えてるので左右の抜き型だけやる
                        if(it_act->s != StencilDirection::LEFT &&
                            it_act->s != StencilDirection::RIGHT) {
                            continue;
                        }

                        // 盤面をコピーして、次の盤面を生成する
                        auto new_board = std::make_shared<Board_bitboard>(*now_state->board);
                        new_board->advance(prob.stencils.at(it_act->p), it_act->x, it_act->y, it_act->s);

                        int eval = evaluateBoard(prob, *new_board);
                        BeamState new_state(nullptr, eval, it_p->first, it_act->x, it_act->y, it_act->s, now_state);

                        // 評価値が更新されたら表示する
                        if(eval > eval_max) {
                            cerr << "improved " << eval << endl;
                            eval_max = eval;
                        }
                        
                        // 盤面が完成しているかどうか判定する
                        if(eval != prob_normal.width * prob_normal.height * 1000) {
                            // 未完成ならキューにいれて、次の探索へ
                            next_q.emplace(new_state);
                        }
                        else {
                            // 完成なら解答をまとめてreturnする
                            cerr << "goal: " << di << endl;

                            if(di < best_ops) {
                                best_ops = di;
                                best_state = std::make_shared<BeamState>(new_state);
                            }

                            should_next = true;
                            break;
                        }
                    }
                }
            }
        }
    }

    auto cur_state = best_state;
    std::vector<Action> answer;
    while(cur_state->prevState != nullptr) {
        answer.push_back({cur_state->p, cur_state->x, cur_state->y, cur_state->s});
        cur_state = cur_state->prevState;
    }

    return std::vector<Action>(answer.rbegin(), answer.rend());
}