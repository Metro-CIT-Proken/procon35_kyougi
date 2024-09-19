#include <memory>
#include <iostream>
#include <queue>

#include "board.h"
#include "bitboard.h"
#include "BeamSolver.h"

using std::cout, std::cerr, std::endl;

void print_board(const Problem &prob, const Board &board)
{
    using std::cout;
    for(int i = 0; i < prob.height; i++) {
        for(int j = 0; j < prob.width; j++) {
            cout << (int)board.cells[i][j] << " \n"[j + 1 == prob.width];
        }
    }
}

static int evaluateBoard(const Problem_bitboard &prob, const Board_bitboard &board)
{
    int eval = 0;
    bool end = false;
    for(int y = 0; y < prob.height; y++) {
        for(int x = 0; x < prob.width; x++) {
            if(board.getCell(x, y) != prob.goal.getCell(x, y)) {
                int tx = x;
                char c = prob.goal.getCell(x, y);
                while(++tx <= prob.width) {
                    if(c == board.getCell(tx, y)) {
                        eval += prob.width - (tx - x);
                        break;
                    }
                }

                end = true;
                break;
            }
            eval += 1000;
        }
        if(end) {
            break;
        }
    }
    return eval;
}

std::vector<Action> BeamSolver::solve(const Problem &prob)
{
    using std::cout, std::cerr, std::endl;

    Problem_bitboard bprob(&prob);
    std::priority_queue<BeamState> q, next_q;
    auto board_start = std::make_shared<Board_bitboard>(bprob.start);
    q.emplace(board_start, 0, 0, 0, 0, StencilDirection::UP, nullptr);
    int eval_max = -1;

    // ビーム深さで探索する
    for(int di = 0; di < this->beamD; di++) {
        cerr << di << endl;
        
        // ビーム幅の分だけキューから取り出して探索する
        for(int wi = 0; wi < this->beamW; wi++) {
            if(q.empty()) {
                break;
            }

            // キューから状態を取り出す
            std::shared_ptr<BeamState> now_state(new BeamState(q.top()));
            q.pop();
            
            // 盤面が省略されているなら生成する
            if(!now_state->board) {
                auto prev_state = now_state->prevState;
                auto new_board = std::make_shared<Board_bitboard>(*prev_state->board);
                new_board->advance(bprob.stencils.at(now_state->p), now_state->x, now_state->y, now_state->s);
                now_state->board = new_board;
            }

            // すべての抜き型を試す
            for(auto it_p = bprob.stencils.begin(); it_p != bprob.stencils.end(); it_p++) {

                // 抜き型が有効なすべての位置を列挙する
                auto acts = prob.stencils.at(it_p->first).legalActions();
                for(auto it_act = acts.begin(); it_act != acts.end(); it_act++) {
                    // 行で揃えてるので左右の抜き型だけやる
                    if(it_act->s != StencilDirection::LEFT &&
                        it_act->s != StencilDirection::RIGHT) {
                        continue;
                    }

                    // 盤面をコピーして、次の盤面を生成する
                    auto new_board = std::make_shared<Board_bitboard>(*now_state->board);
                    new_board->advance(it_p->second, it_act->x, it_act->y, it_act->s);
                    int eval = evaluateBoard(bprob, *new_board);
                    BeamState new_state(nullptr, eval, it_p->first, it_act->x, it_act->y, it_act->s, now_state);

                    // 評価値が更新されたら表示する
                    if(eval > eval_max) {
                        cerr << "improved " << eval << endl;
                        eval_max = eval;
                    }
                    
                    // 盤面が完成しているかどうか判定する
                    if(eval != prob.width * prob.height * 1000) {
                        // 未完成ならキューにいれて、次の探索へ
                        // if(next_q.size() >= beamW && next_q.top().eval <= eval) {
                        //     continue;
                        // }
                        next_q.emplace(new_state);

                        // if(next_q.size() > beamW) {
                        //     next_q.pop();
                        // }
                    }
                    else {
                        // 完成なら解答をまとめてreturnする
                        cerr << "goal: " << di << endl;

                        auto cur_state = &new_state;
                        std::vector<Action> answer;
                        while(cur_state->prevState != nullptr) {
                            answer.push_back({cur_state->p, cur_state->x, cur_state->y, cur_state->s});
                            printf("  p %3d xy %d %d s %d\n", 
                                cur_state->p, cur_state->x, cur_state->y, cur_state->s);
                            cur_state = cur_state->prevState.get();
                        }

                        return answer;
                    }
                }
            }
        }

        q = std::move(next_q);
        decltype(next_q)().swap(next_q);
    }
}

std::vector<Action> InboundBeamSolver::solve(const Problem &prob)
{
    using std::cout, std::cerr, std::endl;

    Problem_bitboard bprob(&prob);
    std::priority_queue<BeamState> q, next_q;
    auto board_start = std::make_shared<Board_bitboard>(bprob.start);
    q.emplace(board_start, 0, 0, 0, 0, StencilDirection::UP, nullptr);
    int eval_max = -1;

    // ビーム深さで探索する
    for(int di = 0; di < this->beamD; di++) {
        cerr << di << endl;
        
        // ビーム幅の分だけキューから取り出して探索する
        for(int wi = 0; wi < this->beamW; wi++) {
            if(q.empty()) {
                break;
            }

            // キューから状態を取り出す
            std::shared_ptr<BeamState> now_state(new BeamState(q.top()));
            q.pop();
            
            // 盤面が省略されているなら生成する
            if(!now_state->board) {
                auto prev_state = now_state->prevState;
                auto new_board = std::make_shared<Board_bitboard>(*prev_state->board);
                new_board->advance(bprob.stencils.at(now_state->p), now_state->x, now_state->y, now_state->s);
                now_state->board = new_board;
            }

            // すべての抜き型を試す
            for(auto it_p = bprob.stencils.begin(); it_p != bprob.stencils.end(); it_p++) {

                // 抜き型が有効なすべての位置を列挙する
                auto acts = prob.stencils.at(it_p->first).legalActions();
                for(auto it_act = acts.begin(); it_act != acts.end(); it_act++) {
                    if(it_act->y < 0) {
                        continue;
                    }

                    // 行で揃えてるので左右の抜き型だけやる
                    if(it_act->s != StencilDirection::LEFT &&
                        it_act->s != StencilDirection::RIGHT) {
                        continue;
                    }

                    // 盤面をコピーして、次の盤面を生成する
                    auto new_board = std::make_shared<Board_bitboard>(*now_state->board);
                    new_board->advance(it_p->second, it_act->x, it_act->y, it_act->s);
                    int eval = evaluateBoard(bprob, *new_board);
                    BeamState new_state(nullptr, eval, it_p->first, it_act->x, it_act->y, it_act->s, now_state);

                    // 評価値が更新されたら表示する
                    if(eval > eval_max) {
                        cerr << "improved " << eval << endl;
                        eval_max = eval;
                    }
                    
                    // 盤面が完成しているかどうか判定する
                    if(eval != prob.width * prob.height * 1000) {
                        // 未完成ならキューにいれて、次の探索へ
                        // if(next_q.size() >= beamW && next_q.top().eval <= eval) {
                        //     continue;
                        // }
                        next_q.emplace(new_state);

                        // if(next_q.size() > beamW) {
                        //     next_q.pop();
                        // }
                    }
                    else {
                        // 完成なら解答をまとめてreturnする
                        cerr << "goal: " << di << endl;

                        auto cur_state = &new_state;
                        std::vector<Action> answer;
                        while(cur_state->prevState != nullptr) {
                            answer.push_back({cur_state->p, cur_state->x, cur_state->y, cur_state->s});
                            printf("  p %3d xy %d %d s %d\n", 
                                cur_state->p, cur_state->x, cur_state->y, cur_state->s);
                            cur_state = cur_state->prevState.get();
                        }

                        return answer;
                    }
                }
            }
        }

        q = std::move(next_q);
        decltype(next_q)().swap(next_q);
    }
}