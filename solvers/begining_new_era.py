import json
from collections import Counter
import numpy as np
import copy

commands = []


def load_problem(file_path):
    with open(file_path) as f:
        form = json.load(f)
    return form


def save_answer(file_path, answer):
    with open(file_path, "w") as f:
        f.write(json.dumps(answer))


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


def log_move(p, x, y, s):
    return {"p": p, "x": x, "y": y, "s": s}


def one_row_slide(board_np):  # 行の要素を一つずらす
    dif, sorted_board_np, nboard_np, go_data, s_logs = sakujo_row(board_np)
    print("one_row_slide")
    print(f"Differences: {dif}")
    logs = []
    board_np = nboard_np
    to_list = []
    for col in range(board_np.shape[1]):
        for element, kazu in dif['1行目'].items():
            row = 0
            if board_np[row][col] == element and kazu > 0:
                to_list.append((row, col))
    from_list = []
    for row in range(1, board_np.shape[0]):  # 最初の一行めは数えない
        for col in range(board_np.shape[1]):
            for element, kazu in dif['1行目'].items():
                if board_np[row][col] == element and kazu < 0:
                    from_list.append((row, col))

    if not from_list:
        return board_np, logs

    from_y = from_list[0][0]
    for i in range(board_np.shape[1], 1, -1):  # 横移動
        board_np[from_y][i-1], board_np[from_y][i -
                                                2] = board_np[from_y][i-2], board_np[from_y][i-1]

    logs.append(log_move(0, board_np.shape[1]-1, from_y, 2))
    return np.concatenate((sorted_board_np, nboard_np), axis=0), logs


def sakujo_row(board_np):

    l_board = []
    logs = []
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

    return dif, sorted_board_np, board_np, goal_data, logs


def first_row(board_np):
    print("first_row")
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
    print("other_rows")
    logs = []
    dif, sorted_board_np, nboard_np, go_data, s_logs = sakujo_row(board_np)
    logs.extend(s_logs)

    if not dif['1行目']:
        return board_np, logs
    to_list = []
    for col in range(nboard_np.shape[1]):
        for element, kazu in dif['1行目'].items():
            row = 0
            if nboard_np[row][col] == element and kazu > 0:
                to_list.append((row, col))
    from_list = []
    for row in range(nboard_np.shape[0]):
        for col in range(nboard_np.shape[1]):
            for element, kazu in dif['1行目'].items():
                if nboard_np[row][col] == element and kazu < 0:
                    from_list.append((row, col))

    if not from_list or not to_list:
        return board_np, logs

    original_board_np = nboard_np.copy()
    for i in range(len(to_list)):
        for f in range(len(from_list)):
            if to_list[i][1] == from_list[f][1]:
                to_x, to_y = to_list[i][1], to_list[i][0]
                from_x, from_y = from_list[f][1], from_list[f][0]
                while to_y < nboard_np.shape[0]-1:
                    nboard_np[to_y+1][to_x], nboard_np[to_y][from_x] = nboard_np[to_y][from_x], nboard_np[to_y+1][to_x]
                    to_y += 1
                if not np.array_equal(original_board_np, nboard_np):
                    logs.append(
                        log_move(0, from_list[f][1], from_list[f][0], 1))
                return np.concatenate((sorted_board_np, nboard_np), axis=0), logs
    return board_np, logs


def last_side_slide(board_np):  # これ全ての行が揃っていていることが前提
    print("last_side_slide")
    logs = []
    original_board_np = board_np.copy()
    for col in range(board_np.shape[0]):
        for row in range(board_np.shape[1]):
            focus_value = goal_data[col][row]
            for np_y in range(board_np.shape[0]):
                for np_x in range(board_np.shape[1]):
                    if board_np[np_y][np_x] == focus_value:
                        most_right_coord = board_np.shape[1]-1
                        coord_x = np_x
                        while coord_x != most_right_coord:
                            board_np[np_y][coord_x], board_np[np_y][coord_x +
                                                                    1] = board_np[np_y][coord_x + 1], board_np[np_y][coord_x]
                            coord_x += 1
                        if not np.array_equal(original_board_np, board_np):
                            logs.append(log_move(0, np_x, np_y, 3))
    return board_np, logs


def sort_board(board_np):
    print("sort_board")
    total_logs = []
    iteration = 0
    while not np.array_equal(board_np, np.array(goal_data)):
        iteration += 1
        print(f"Iteration {iteration}: Current board state:")
        print(board_np)
        dif = calculate_differences(board_np.tolist(), goal_data)

        if dif['1行目']:
            zenkai_board_np = board_np
            board_np, logs = first_row(board_np)
            total_logs.extend(logs)
            if np.array_equal(board_np, zenkai_board_np):
                board_np, logs = one_row_slide(board_np)
                total_logs.extend(logs)
        elif dif[f'{board_np.shape[0]}行目']:
            zenkai_board_np = board_np
            board_np, logs = other_rows(board_np)
            if np.array_equal(board_np, zenkai_board_np):
                board_np, logs = one_row_slide(board_np)
                total_logs.extend(logs)
        else:
            board_np, logs = last_side_slide(board_np)
            total_logs.extend(logs)
    return board_np, total_logs


def main():
    problem_file = "problem_youkou.json"
    answer_file = "answer.json"

    problem = load_problem(problem_file)

    global start_data, goal_data
    start = problem["board"]["start"]
    goal = problem['board']['goal']

    start_data = [[int(char) for char in item] for item in start]
    goal_data = [[int(char) for char in item] for item in goal]

    board_np = np.array(start_data)
    sorted_board, logs = sort_board(board_np)

    print("Final sorted board:")
    print(sorted_board)
    answer = {"n": len(logs), "ops": logs}
    print(answer)

    save_answer(answer_file, answer)


if __name__ == "__main__":
    main()
