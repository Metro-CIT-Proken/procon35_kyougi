#include <memory>
#include <iostream>
#include <queue>
#include <array>
#include <unordered_set>
#include <mutex>
#include <optional>

#include <tbb/global_control.h>
#include <tbb/task.h>
#include <tbb/parallel_sort.h>
#include <tbb/parallel_for_each.h>

#include "board.h"
#include "bitboard.h"
#include "BeamSolver.h"
#include "SpinMutex.h"
#include "BeamEvaluator.h"

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

std::vector<Action> BeamSolver::solve(const Problem &prob)
{
    using std::cout, std::cerr, std::endl;

    // 並列数
    int concurrency = tbb::this_task_arena::max_concurrency();

    Problem_bitboard bprob(&prob);
    std::vector<std::vector<BeamState>> q(concurrency), next_q(concurrency);
    SpinMutex mutex_complete_state;
    std::optional<AnswerIndex> completed_answer;
    AnswerTree answer_tree(concurrency);
    BeamEvaluator evaluator(&bprob);

    std::vector<int> eval_depth_max(concurrency);
    std::vector<int> eval_threshold(concurrency);

    BeamState state_start(bprob.start, 0, AnswerSentinel);
    q[0].push_back(state_start);

    // tbb::concurrent_unordered_set<Board_bitboard, Board_bitboard::hash> visited_nodes;

    // ビーム深さで探索する
    for(int di = 0; di < this->beamD; di++) {
        std::fill(eval_depth_max.begin(), eval_depth_max.end(), 0);
        std::fill(eval_threshold.begin(), eval_threshold.end(), 0);

        std::vector<std::pair<int, const BeamState *>> states;
        for(int i = 0; i < concurrency; i++) {
            for(int j = 0; j < q[i].size(); j++) {
                states.emplace_back(q[i][j].eval, &q[i][j]);
            }
        }

        if(states.size() > this->beamW) {
            tbb::parallel_sort(states.begin(), states.end(), std::greater<decltype(states)::value_type>());
            states.erase(states.begin() + this->beamW, states.end());
        }

        tbb::parallel_for_each(states.begin(), states.end(), [
            this,
            &q, &next_q, &eval_depth_max, &mutex_complete_state, &completed_answer,
            &bprob, &prob, &di, &answer_tree, &evaluator, &eval_threshold
        ] (const std::pair<int, const BeamState *> &s) {
            const auto thread = tbb::this_task_arena::current_thread_index();
            auto now_state = s.second;

            // すべての抜き型を試す
            for(auto it_p = bprob.stencils.cbegin(); it_p != bprob.stencils.cend(); it_p++) {

                // 抜き型が有効なすべての位置を列挙する
                auto acts = prob.stencils.at(it_p->first).legalActions();
                for(auto it_act = acts.cbegin(); it_act != acts.cend(); it_act++) {
                    // if(tbb::is_current_task_group_canceling()) {
                    //     return;
                    // }

                    // 盤面をコピーして、次の盤面を生成する
                    BeamState &new_state = next_q[thread].emplace_back(now_state->board, -1, AnswerSentinel);
                    new_state.board.advance(it_p->second, it_act->x, it_act->y, it_act->s);

                    // if(visited_nodes.count(*new_board)) {
                    //     continue;
                    // }
                    // visited_nodes.insert(*new_board);

                    auto answer_index = answer_tree.add(thread, now_state->answer_index, 
                        {it_p->first, it_act->x, it_act->y, it_act->s});
                    auto eval = evaluator.evaluate(new_state.board);
                    new_state.eval = eval.value;
                    new_state.answer_index = answer_index;
                    eval_depth_max[thread] = std::max(eval_depth_max[thread], eval.value);

                    // if(q.size() >= this->beamW * 2) {
                    //     std::sort(next_q[thread].begin(), next_q[thread].end(), std::greater<BeamState>());
                    //     eval_threshold[thread] = q[thread].back().eval;
                    // }

                    // if(new_state.eval <= eval_threshold[thread]) {
                    //     q.pop_back();
                    // }
                    
                    // 盤面が完成しているかどうか判定する
                    if(eval.first_line_restored) {
                        // 完成なら解答をまとめてreturnする
                        cerr << "goal: " << di << endl;

                        tbb::task::current_context()->cancel_group_execution();
                        {
                            std::lock_guard<SpinMutex> guard(mutex_complete_state);
                            if(!completed_answer) {
                                completed_answer = new_state.answer_index;
                            }
                        }

                        return;
                    }
                }
            }
        });

        if(completed_answer) {
            break;
        }

        int eval_max = 0;
        for(int i = 0; i < concurrency; i++) {
            q[i].clear();
            q[i].swap(next_q[i]);

            eval_max = std::max(eval_max, eval_depth_max[i]);
        }

        cerr << "depth " << di << " eval " << eval_max << endl;
    }

    return answer_tree.build(completed_answer.value());
}

// std::vector<Action> BeamSolver::solve(const Problem &prob)
// {
//     using std::cout, std::cerr, std::endl;

//     Problem_bitboard bprob(&prob);
//     std::priority_queue<BeamState> q, next_q;
//     auto board_start = std::make_shared<Board_bitboard>(bprob.start);
//     q.emplace(board_start, 0, 0, 0, 0, StencilDirection::UP, nullptr);
//     int eval_max = -1;

//     std::unordered_set<Board_bitboard, Board_bitboard::hash> visited_nodes;

//     // ビーム深さで探索する
//     for(int di = 0; di < this->beamD; di++) {
//         cerr << di << endl;
//         int eval_depth_max = -1;
        
//         // ビーム幅の分だけキューから取り出して探索する
//         for(int wi = 0; wi < this->beamW; wi++) {
//             if(q.empty()) {
//                 break;
//             }

//             // キューから状態を取り出す
//             std::shared_ptr<BeamState> now_state(new BeamState(q.top()));
//             q.pop();

//             // 盤面が省略されているなら生成する
//             if(!now_state->board) {
//                 auto prev_state = now_state->prevState;
//                 auto new_board = std::make_shared<Board_bitboard>(*prev_state->board);
//                 new_board->advance(bprob.stencils.at(now_state->p), now_state->x, now_state->y, now_state->s);
//                 now_state->board = new_board;
//             }

//             // すべての抜き型を試す
//             for(auto it_p = bprob.stencils.begin(); it_p != bprob.stencils.end(); it_p++) {

//                 // 抜き型が有効なすべての位置を列挙する
//                 auto acts = prob.stencils.at(it_p->first).legalActions();
//                 for(auto it_act = acts.begin(); it_act != acts.end(); it_act++) {
//                     // 行で揃えてるので左右の抜き型だけやる
//                     if(it_act->s != StencilDirection::LEFT &&
//                         it_act->s != StencilDirection::RIGHT) {
//                         continue;
//                     }

//                     // 盤面をコピーして、次の盤面を生成する
//                     auto new_board = std::make_shared<Board_bitboard>(*now_state->board);
//                     new_board->advance(it_p->second, it_act->x, it_act->y, it_act->s);

//                     if(visited_nodes.count(*new_board)) {
//                         continue;
//                     }
//                     visited_nodes.insert(*new_board);

//                     int eval = evaluateBoard(bprob, *new_board);
//                     BeamState new_state(nullptr, eval, it_p->first, it_act->x, it_act->y, it_act->s, now_state);

//                     // 評価値が更新されたら表示する
//                     if(eval > eval_max) {
//                         cerr << "improved " << eval << endl;
//                         eval_max = eval;
//                     }

//                     eval_depth_max = std::max(eval, eval_depth_max);
                    
//                     // 盤面が完成しているかどうか判定する
//                     if(eval != prob.width * prob.height * 1000000) {
//                         // 未完成ならキューにいれて、次の探索へ
//                         next_q.emplace(new_state);
//                     }
//                     else {
//                         // 完成なら解答をまとめてreturnする
//                         cerr << "goal: " << di << endl;

//                         auto cur_state = &new_state;
//                         std::vector<Action> answer;
//                         while(cur_state->prevState != nullptr) {
//                             answer.push_back({cur_state->p, cur_state->x, cur_state->y, cur_state->s});
//                             cur_state = cur_state->prevState.get();
//                         }

//                         return std::vector(answer.rbegin(), answer.rend());
//                     }
//                 }
//             }
//         }

//         cerr << "depth max: " << eval_depth_max << endl;

//         q = std::move(next_q);
//         decltype(next_q)().swap(next_q);
//     }

//     return {};
// }