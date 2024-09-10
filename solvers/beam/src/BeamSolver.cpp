#include <memory>
#include <iostream>
#include <queue>

#include "board.h"
#include "BeamSolver.h"

using std::cout, std::cerr, std::endl;

class BeamState
{
public:
    BeamState(std::shared_ptr<Board> board, int eval, int p, int x, int y, StencilDirection s, std::shared_ptr<BeamState> prevState) :
        board(board), eval(eval), p(p), x(x), y(y), s(s), prevState(prevState)
    {
    }

    struct Comp {
        bool operator()(const BeamState &left,  const BeamState &right)
        {
            return left.eval < right.eval;
        }
    };

    std::shared_ptr<Board> board;
    int eval, p, x, y;
    StencilDirection s;
    std::shared_ptr<BeamState> prevState;
};

void print_board(const Problem &prob, const Board &board)
{
    using std::cout;
    for(int i = 0; i < prob.height; i++) {
        for(int j = 0; j < prob.width; j++) {
            cout << (int)board.cells[i][j] << " \n"[j + 1 == prob.width];
        }
    }
}

int evaluateBoard(const Problem &prob, const Board &board)
{
    int eval = 0;
    bool end = false;
    for(int y = 0; y < prob.height; y++) {
        for(int x = 0; x < prob.width; x++) {
            if(board.cells[y][x] != prob.goal.cells[y][x]) {
                int tx = x;
                char c = prob.goal.cells[y][tx];
                while(++x <= prob.width) {
                    if(c == board.cells[y][x]) {
                        eval += prob.width - (x - tx);
                        break;
                    }
                }

                end = true;
                break;
            }
            eval += 1000;
        }
        // if(end) {
        //     break;
        // }
    }
    return eval;
}

std::vector<Action> BeamSolver::solve(const Problem &prob)
{
    using std::cout, std::cerr, std::endl;
    std::priority_queue<BeamState, std::vector<BeamState>, BeamState::Comp> q, next_q;
    auto board_start = std::make_shared<Board>(prob.start);
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
                auto new_board = std::make_shared<Board>(*prev_state->board);
                new_board->advance(prob.stencils.at(now_state->p), now_state->x, now_state->y, now_state->s);
                now_state->board = new_board;
            }

            // すべての抜き型を試す
            for(auto it_p = prob.stencils.begin(); it_p != prob.stencils.end(); it_p++) {
                if(it_p->second.isDefault() && it_p->second.width > prob.width * 2) {
                    continue;
                }

                // 抜き型が有効なすべての位置を列挙する
                auto acts = it_p->second.legalActions();
                for(auto it_act = acts.begin(); it_act != acts.end(); it_act++) {
                    // 行で揃えてるので左右の抜き型だけやる
                    if(it_act->s != StencilDirection::LEFT &&
                        it_act->s != StencilDirection::RIGHT) {
                        continue;
                    }

                    // 盤面をコピーして、次の盤面を生成する
                    auto new_board = std::make_shared<Board>(*now_state->board);
                    new_board->advance(it_p->second, it_act->x, it_act->y, it_act->s);
                    int eval = evaluateBoard(prob, *new_board);
                    BeamState new_state(nullptr, eval, it_p->first, it_act->x, it_act->y, it_act->s, now_state);

                    // 評価値が更新されたら表示する
                    if(eval > eval_max) {
                        cerr << "improved " << eval << endl;
                        eval_max = eval;
                    }
                    
                    // 盤面が完成しているかどうか判定する
                    if(eval != prob.width * prob.height * 1000) {
                        // 未完成ならキューにいれて、次の探索へ
                        next_q.emplace(new_state);
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

void showProblem(Problem &prob) {
    cout << "Problem:" << endl;
    cout << "  width: " << prob.width << endl;
    cout << "  height: " << prob.height << endl;
    cout << "  start:" << endl;
    for(int i = 0; i < prob.height; i++) {
        cout << "    ";
        for(int j = 0; j < prob.width; j++) {
            cout << int(prob.start.cells[i][j]);
        }
        cout << endl;
    }
    cout << "  goal:" << endl;
    for(int i = 0; i < prob.height; i++) {
        cout << "    ";
        for(int j = 0; j < prob.width; j++) {
            cout << int(prob.goal.cells[i][j]);
        }
        cout << endl;
    }
    for(auto it = prob.stencils.begin(); it != prob.stencils.end(); it++) {
        cout << "  stencil_" << it->first << ":" << endl;
        for(int i = 0; i < it->second.height; i++) {
            cout << "    ";
            for(int j = 0; j < it->second.width; j++) {
                cout << int(it->second.cells[i][j]);
            }
            cout << endl;
        }
    }
}