import random
import copy
from time import sleep
import json
import copy

def out(board):
    """
    ボードの状態をコンソールに出力する関数
    """
    for i in board[::-1]:
        for j in i:
            print(j, end="")
        print()
    print()


def read():
    """
    JSONファイルからボード情報を読み込む関数
    """
    with open('field.json', encoding="utf-8") as f:
        global jin
        jin = json.load(f)


def move(cboard, ii, jj, act):
    """
    指定された方向にボードのパーツを移動させる関数

    Parameters:
        cboard: 現在のボードの状態
        ii, jj: 移動するパーツの位置
        act: 移動方向（上: -1、下: 1、左: -2、右: 2）
    """
    u = act % 2 * act // abs(act)
    r = (act + 1) % 2 * act // abs(act)
    m = copy.copy(act)

    if m == -1:
        m = 1

    elif m == 1:
        m = 0

    elif m == -2:
        m = 3

    elif m == 2:
        m = 2

    ans_act.append({"p": 0,
                    "x": jj,
                    "y": ii,
                    "s": m
                    })
    # print(ii,jj,act)
    if u != 0:
        for i in range(ii, 0 if u < 0 else len(cboard), -1 if u < 0 else 1):
            try:
                cboard[i][jj], cboard[i +
                                      u][jj] = cboard[i + u][jj], cboard[i][jj]
            except:
                pass

    else:
        for j in range(jj, 0 if r < 0 else len(cboard[0]), -1 if r < 0 else 1):
            try:
                cboard[ii][j], cboard[ii][j +
                                          r] = cboard[ii][j + r], cboard[ii][j]
            except:
                pass


def s_r(cboard, i, I, j, J, count):
    """
    指定された位置からパーツを移動させる関数

    Parameters:
        cboard: 現在のボードの状態
        i, I, j, J: 移動するパーツの開始位置と目標位置
        count: 移動回数のカウント

    Returns:
        更新されたボードの状態とカウント
    """
    while J != 0 or I != 0:

        if J != 0:
            move(cboard, i + I, j + J - 1, 2)
            count += 1
            J -= 1

        else:
            move(cboard, i + I - 1, j + J, 1)
            count += 1
            I -= 1
        # out(cboard)

    return cboard, i, I, j, J, count

def set_board():
    """
    ボードの初期設定を行う関数

    Returns:
        初期ボード、現在のボード、高さ、幅
    """
    i = jin["board"]["width"]
    j = jin["board"]["height"]
    cboard = [[" " for _ in range(i)] for _ in range(j)]
    for K, k in enumerate(jin["board"]["start"]):
        for L, l in enumerate(k):
            cboard[K][L] = l

    board = [[" " for _ in range(i)] for _ in range(j)]
    for K, k in enumerate(jin["board"]["goal"]):
        for L, l in enumerate(k):
            board[K][L] = l
    return board, cboard, j, i


# ボード情報の読み込み
read()

# ボードの初期設定
board, cboard, a, b = set_board()

# print(jin)

# 移動回数のカウント初期化
count = 0

# print(board)

h = len(cboard)
w = len(cboard[0])

ans_json = open('ans.json', 'w')
ans_act = []

# out(cboard)
# ゴールの状態になるまでボードの状態を更新
while cboard != board:
    for i in range(a):
        score = []
        for j in range(b):
            for k in [-1,1,2,-2]:
                test = copy.deepcopy(cboard)
                move(test,i,j,k)
                ichi=0
                if cboard != test:
                    for I in range(a):
                        for J in range(b):
                            if test[I][J] == board[I][J]:
                                ichi+=1
                    score.append([ichi,[i,j],k])
        MAX = -1
        point=0
        score.sort(key = lambda v:v[0],reverse=True)
        print(score)
        I,J = score[point][1]
        ac = score[point][2]
        # print(I,J)
        # print(I)
        # print(J)
        move(cboard,I,J,ac)
        count += 1
        out(cboard)
        out(board)
        # print("---------------------")

# 最終結果を出力
print(count, "count")
answer = {"n":count,"ops":ans_act}
json.dump(answer,ans_json)
ans_json.close()