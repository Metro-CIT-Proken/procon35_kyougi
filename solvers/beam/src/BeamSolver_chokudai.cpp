#include <memory>
#include <iostream>
#include <queue>

#include "board.h"
#include "bitboard.h"
#include "BeamSolver.h"

using std::cout, std::cerr, std::endl;

static int evaluateBoard(const Problem_bitboard &prob, const Board_bitboard &board)
{
    int eval = 0;
    bool end = false;
    for(int y = 0; y < prob.prob->height; y++) {
        // 最適化のためのコード
        // const int words_count = (CELL_BITS * prob.prob->width + WORD_BITS - 1) / WORD_BITS;
        // for(int w = 0; w < words_count; w++) {
        //     if(board.cells[y][w] != prob.goal.cells[y][w]) {

        //     }
        // }

        for(int x = 0; x < prob.prob->width; x++) {
            if(board.getCell(x, y) != prob.goal.getCell(x, y)) {
                int tx = x;
                int c = prob.goal.getCell(x, y);
                while(++x <= prob.prob->width) {
                    if(c == board.getCell(x, y)) {
                        eval += prob.prob->width - (x - tx);
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

std::vector<Action> ChokudaiBeamSolver::solve(const Problem &prob_normal)
{
    using std::cout, std::cerr, std::endl;

    Problem_bitboard prob(&prob_normal);
    int beam_count = 50;
    std::vector<std::priority_queue<BeamState, std::vector<BeamState>, BeamState::Comp>> beam(this->beamD + 1);
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
                    if(prob_normal.stencils.at(it_p->first).isDefault() && it_p->second.width > prob.prob->width * 2) {
                        continue;
                    }

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

std::vector<Action> InboundChokudaiBeamSolver::solve(const Problem &prob_normal)
{
    using std::cout, std::cerr, std::endl;

    Problem_bitboard prob(&prob_normal);
    int beam_count = 50;
    std::vector<std::priority_queue<BeamState, std::vector<BeamState>, BeamState::Comp>> beam(this->beamD + 1);
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