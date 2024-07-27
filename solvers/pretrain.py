import json
from collections import Counter
import numpy as np
import copy
import time
import sys
# from_listは動かす要素の位置（指定する要素の位置）
# to_listは動かし先の要素の位置
# 例外もあり

file = sys.argv[1]

with open(file) as f:
    form = json.load(f)

# startとgoalの盤面を取得
start = form["board"]["start"]
goal = form['board']['goal']

# startとgoalのそれぞれの行を整数のリストに変換
start_data = [[int(char) for char in item] for item in start]
goal_data = [[int(char) for char in item] for item in goal]

# 行ごとの不足している要素と余っている要素を保存する辞書
action_log = []


def calculate_differences(start_board, goal_board):
    all_differences = {}
    for i in range(len(start_board)):
        start_counter = Counter(start_board[i])
        goal_counter = Counter(goal_board[i])
        differences = {}
        for num in set(start_counter.keys()).union(set(goal_counter.keys())):
            start_count = start_counter.get(num, 0)
            goal_count = goal_counter.get(num, 0)
            diff = start_count - goal_count
            if diff != 0:
                differences[num] = diff
        all_differences[f"{i+1}行目"] = differences
    return all_differences


# NumPy 配列に変換
board_np = np.array(start_data)


def log_move(p, x, y, s):
    return {"p": p, "x": x, "y": y, "s": s}


def one_row_slide(board_np):  # 行の要素を一つずらす
    dif, sorted_board_np, nboard_np, go_data, s_logs = sakujo_row(board_np)

    logs = []
    board_np = nboard_np
    to_list = []
    for col in range(board_np.shape[1]):
        for element, kazu in dif['1行目'].items():
            row = 0
            if board_np[row][col] == element and kazu > 0:
                to_list.append((row, col))  # 一行目の余っている要素をto_list
    from_list = []
    for row in range(1, board_np.shape[0]):  # 最初の一行めは数えない
        for col in range(board_np.shape[1]):
            for element, kazu in dif['1行目'].items():
                if board_np[row][col] == element and kazu < 0:
                    from_list.append((row, col))  # 1行目の足りない要素の位置をfrom_listに保存

    if not from_list:
        return board_np, logs

    from_y = from_list[0][0]
    for i in range(board_np.shape[1], 1, -1):  # 横移動
        board_np[from_y][i-1], board_np[from_y][i -
                                                2] = board_np[from_y][i-2], board_np[from_y][i-1]

    # 一番右の要素を左に移動させる
    logs.append(
        log_move(0, board_np.shape[1]-1, from_y+sorted_board_np.shape[0], 2))
    return np.concatenate((sorted_board_np, nboard_np), axis=0), logs


def sakujo_row(board_np):

    l_board = []
    tukawanai_logs = []
    board = board_np.tolist()
    dif = calculate_differences(board, goal_data)
    goal_data_copy = copy.deepcopy(goal_data)
    # Initialize sorted_board_np
    sorted_board_np = np.empty((0, board_np.shape[1]), int)
    while not dif['1行目']:
        a_0, a_1 = np.split(board_np, [1])
        l_board.append(a_0)
        l_1 = a_1.tolist()
        del goal_data_copy[0]
        dif = calculate_differences(l_1, goal_data_copy)
        board_np = np.array(l_1)
        sorted_board_np = np.concatenate(
            (sorted_board_np, a_0), axis=0)  # Accumulate sorted rows
    return dif, sorted_board_np, board_np, goal_data, tukawanai_logs


def first_row(board_np):

    logs = []
    board = board_np.tolist()
    dif = calculate_differences(board, goal_data)
    if not dif['1行目']:
        return board_np, logs
    to_list = []
    for col in range(board_np.shape[1]):
        for element, kazu in dif['1行目'].items():
            row = 0
            if board_np[row][col] == element and kazu > 0:
                to_list.append((row, col))
    from_list = []
    for row in range(1, board_np.shape[0]):
        for col in range(board_np.shape[1]):
            for element, kazu in dif['1行目'].items():
                if board_np[row][col] == element and kazu < 0:
                    from_list.append((row, col))

    if not from_list or not to_list:
        return board_np, logs

    original_board_np = board_np.copy()
    for i in range(len(to_list)):
        for f in range(len(from_list)):
            if to_list[i][1] == from_list[f][1]:
                to_x, to_y = to_list[i][1], to_list[i][0]
                from_x, from_y = from_list[f][1], from_list[f][0]
                # 縦移動
                while from_y > to_y:
                    board_np[from_y][from_x], board_np[from_y -
                                                       1][from_x] = board_np[from_y - 1][from_x], board_np[from_y][from_x]
                    from_y -= 1
                if not np.array_equal(original_board_np, board_np):
                    logs.append(
                        log_move(0, from_list[f][1], from_list[f][0], 0))
                return board_np, logs
    return board_np, logs


def other_rows(board_np):
    logs = []
    dif, sorted_board_np, nboard_np, go_data, tuka = sakujo_row(board_np)

    if not dif['1行目']:
        # 全ての行に間違いがなければそのまま返す
        return np.concatenate((sorted_board_np, nboard_np), axis=0), logs

    to_list = []
    # to_listは現在の行の余っている要素の位置を保存する
    for col in range(nboard_np.shape[1]):
        for element, kazu in dif['1行目'].items():
            row = 0
            if nboard_np[row][col] == element and kazu > 0:
                to_list.append((row, col))

    from_list = []
    # nboard_np.shape[0]の長さが1以下になることはない(長さが１になった時点で全て揃っているため)
    # from_listは不足している要素を見つけてくる
    for row in range(1, nboard_np.shape[0]):  # 1行目は含めない
        for col in range(nboard_np.shape[1]):
            for element, kazu in dif['1行目'].items():
                if nboard_np[row][col] == element and kazu < 0:
                    from_list.append((row, col))
    original_board_np = nboard_np.copy()
    for i in range(len(to_list)):
        for f in range(len(from_list)):
            if to_list[i][1] == from_list[f][1]:  # 余っている要素の列で不足している要素がある場合
                to_x, to_y = to_list[i][1], to_list[i][0]  # 余っている要素のx,y
                # 不足している要素のx,y
                from_x, from_y = from_list[f][1], from_list[f][0]

                # 縦移動
                while to_y < nboard_np.shape[0]-1:
                    nboard_np[to_y+1][to_x], nboard_np[to_y][from_x] = nboard_np[to_y][from_x], nboard_np[to_y+1][to_x]
                    to_y += 1

                if not np.array_equal(original_board_np, nboard_np):
                    logs.append(
                        log_move(0, to_list[i][1], to_list[i][0]+sorted_board_np.shape[0], 1))

                return np.concatenate((sorted_board_np, nboard_np), axis=0), logs
    return np.concatenate((sorted_board_np, nboard_np), axis=0), logs


def same_y_skip(board_np, now_y):
    goal_data_np = np.array(goal_data)
    if (board_np[now_y] == goal_data_np[now_y]).all():
        return True
    return False


def last_side_slide(board_np):
    print("last_side_slide")
    logs = []
    same_value = False
    previous_value = 100
    original_board_np = board_np.copy()
    for col in range(board_np.shape[0]):
        previous_value = 100

        if same_y_skip(board_np, col):
            print(f'{col+1}行目をスキップ')
            continue
        for row in range(board_np.shape[1]):
            focus_value = goal_data[col][row]
            if previous_value == focus_value:
                same_value = True
            else:
                same_value = False
            previous_value = focus_value

            for np_x in range(board_np.shape[1] - 1):

                if board_np[col][np_x] == focus_value:
                    if board_np[col][-1] == focus_value and same_value:
                        most_right_coord = board_np.shape[1] - 1
                        coord_x = np_x
                        while coord_x != most_right_coord:
                            board_np[col][coord_x], board_np[col][coord_x +
                                                                  1] = board_np[col][coord_x + 1], board_np[col][coord_x]
                            coord_x += 1
                        logs.append(log_move(0, np_x, col, 3))
                        break

                    elif board_np[col][-1] != focus_value:
                        print(f'Right most value is not the same: col: {
                              col}, row: {row}, np_x: {np_x}')
                        most_right_coord = board_np.shape[1] - 1
                        coord_x = np_x
                        while coord_x != most_right_coord:
                            board_np[col][coord_x], board_np[col][coord_x +
                                                                  1] = board_np[col][coord_x + 1], board_np[col][coord_x]
                            coord_x += 1
                        logs.append(log_move(0, np_x, col, 3))
                        break

                    print(board_np)
                    logs.append(log_move(0, np_x, col, 3))
                    break
    return board_np, logs


def is_other_row(board_np):

    dif = calculate_differences(board_np.tolist(), goal_data)
    for n in dif:
        if dif[n]:

            return True
    return False  # まだ違いがある場合Trueを返す


def sort_board(board_np):
    log1 = []
    log2 = []
    total_logs = []
    while not np.array_equal(board_np, np.array(goal_data)):
        dif = calculate_differences(board_np.tolist(), goal_data)
        if dif['1行目']:  # １行目が整理されていない
            zenkai_board_np = board_np.copy()
            board_np, logs = first_row(board_np)
            if np.array_equal(board_np, zenkai_board_np):
                board_np, logs = one_row_slide(board_np)
                total_logs.extend(logs)
                log1.extend(logs)
            else:
                total_logs.extend(logs)
                log1.extend(logs)
            print(board_np)
        # １行めが整理されている状態で、最後の行がまだ整理されていない
        # 途中の行をスキップしているからform.jsonではエラーが発生している
        elif is_other_row(board_np):
            zenkai_board_np = board_np.copy()
            board_np, logs = other_rows(board_np)
            if np.array_equal(board_np, zenkai_board_np):
                board_np, logs = one_row_slide(board_np)
                total_logs.extend(logs)
                log1.extend(logs)
            else:
                total_logs.extend(logs)
                log1.extend(logs)
            print(board_np)
        else:
            print("ここからlast_side_slide")
            board_np, logs = last_side_slide(board_np)
            total_logs.extend(logs)
            log2.extend(logs)
    return board_np, total_logs, log1, log2


sorted_board, logs, log1, log2 = sort_board(board_np)


rev_y_logs = []
for n in logs:
    # abs_y = n["y"] - (board_np.shape[0]-1)
    # abs_y = abs(abs_y)
    if n["s"] == 0:
        rev_y_logs.append(log_move(n["p"], n["x"], n["y"], 1))  # １を上移動として
    elif n["s"] == 1:
        rev_y_logs.append(log_move(n["p"], n["x"], n["y"], 0))  # 0 を下移動として
    elif n["s"] == 2:
        rev_y_logs.append(log_move(n["p"], n["x"], n["y"], 3))  # 3 を左移動として
    elif n["s"] == 3:
        rev_y_logs.append(log_move(n["p"], n["x"], n["y"], 2))  # 2 を右移動として送る

rev_log1 = []
for n in log1:
    # abs_y = n["y"] - (board_np.shape[0]-1)
    # abs_y = abs(abs_y)
    if n["s"] == 0:
        rev_log1.append(log_move(n["p"], n["x"], n["y"], 1))  # １を上移動として
    elif n["s"] == 1:
        rev_log1.append(log_move(n["p"], n["x"], n["y"], 0))  # 0 を下移動として
    elif n["s"] == 2:
        rev_log1.append(log_move(n["p"], n["x"], n["y"], 3))  # 3 を左移動として
    elif n["s"] == 3:
        rev_log1.append(log_move(n["p"], n["x"], n["y"], 2))  # 2 を右移動として送る

rev_log2 = []
for n in log2:
    # abs_y = n["y"] - (board_np.shape[0]-1)
    # abs_y = abs(abs_y)
    if n["s"] == 0:
        rev_log2.append(log_move(n["p"], n["x"], n["y"], 1))  # １を上移動として
    elif n["s"] == 1:
        rev_log2.append(log_move(n["p"], n["x"], n["y"], 0))  # 0 を下移動として
    elif n["s"] == 2:
        rev_log2.append(log_move(n["p"], n["x"], n["y"], 3))  # 3 を左移動として
    elif n["s"] == 3:
        rev_log2.append(log_move(n["p"], n["x"], n["y"], 2))  # 2 を右移動として送る


print(sorted_board)


# ここから答えのテスト
problem_json = file


with open(problem_json) as f:
    problem = json.loads(f.read())

width = problem["board"]["width"]
height = problem["board"]["height"]
start = np.array([[int(x) for x in line]
                 for line in problem["board"]["start"]], dtype=np.int8)
goal = np.array([[int(x) for x in line]
                for line in problem["board"]["goal"]], dtype=np.int8)
ops = rev_log1
for i in range(len(ops)):
    op = ops[i]
    x = op["x"]
    y = op["y"]
    s = op["s"]
    p = op["p"]

    assert p == 0, "1x1の抜き型のみ対応しています"

    # print("==========")
    # print(y, x, "上下左右"[s])
    # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
    # print()

    tmp = start[y:y+1, x:x+1].copy()
    if s == 0:  # 上
        start[y:height-1, x:x+1] = start[y+1:height, x:x+1]
        start[height-1:height, x:x+1] = tmp
    elif s == 1:  # 下
        start[1:y+1, x:x+1] = start[0:y, x:x+1]
        start[0:1, x:x+1] = tmp
    elif s == 2:  # 右
        start[y:y+1, x:width-1] = start[y:y+1, x+1:width]
        start[y:y+1, width-1:width] = tmp
    elif s == 3:  # 左
        start[y:y+1, 1:x+1] = start[y:y+1, 0:x]
        start[y:y+1, 0:1] = tmp


print("rev_log1実行後", start)
ops = rev_log2
change_rev_log2 = []
goal_np = np.array(goal_data)
before_side_slide = start.copy()
itiji = []

for op in ops:
    x = op["x"]
    y = op["y"]
    s = op["s"]
    p = op["p"]
    assert p == 0, "1x1の抜き型のみ対応しています"

    tmp = start[y:y+1, x:x+1].copy()
    if s == 0:  # 上
        start[y:height-1, x:x+1] = start[y+1:height, x:x+1]
        start[height-1:height, x:x+1] = tmp
    elif s == 1:  # 下
        start[1:y+1, x:x+1] = start[0:y, x:x+1]
        start[0:1, x:x+1] = tmp
    elif s == 2:  # 右
        start[y:y+1, x:width-1] = start[y:y+1, x+1:width]
        start[y:y+1, width-1:width] = tmp
    elif s == 3:  # 左
        start[y:y+1, 1:x+1] = start[y:y+1, 0:x]
        start[y:y+1, 0:1] = tmp

    # 実行したログを一時リストに保存する
    if not (start[y] == before_side_slide[y]).all():  # 盤面が変わった場合のみログを保存
        itiji.append(op)
        before_side_slide = start.copy()  # 盤面を更新
    else:  # 盤面が変わらなかった場合は一時ログをクリア
        itiji = []

    # ゴールのy行と同じになったら一時ログを合計ログに保存し、次の行へ進む
    if (start[y] == goal_np[y]).all():
        change_rev_log2.extend(itiji)
        itiji = []
        continue

print(len(rev_log1))
print(len(rev_log2))
print(len(change_rev_log2))
print(change_rev_log2)
print(start)
answer = {"n": len(logs),
          "ops": rev_log1+change_rev_log2}
with open("answer.json", "w") as f:
    f.write(json.dumps(answer))
