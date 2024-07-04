import json
import sys
import queue
from threading import Timer

import pdb


class Act:
    def __init__(self, p: int, x: int, y: int, s: int):
        self.p = p
        self.x = x
        self.y = y
        self.s = s

# 解答を保持する配列
answer = list[Act]()

# 問題を読み込む
with open(sys.argv[1]) as f:
    problem = json.loads(f.read())
board = problem["board"]
width = board["width"]
height = board["height"]
start = [[int(c) for c in line] for line in board["start"]]
goal = [[int(c) for c in line] for line in board["goal"]]

# 行の整数値の数を保持する配列
goal_cnt = list[dict[int, int]]()
start_cnt = list[dict[int, int]]()
for y in range(height):
    goal_cnt.append({c: 0 for c in range(4)})
    start_cnt.append({c: 0 for c in range(4)})
    for x in range(width):
        goal_cnt[y][goal[y][x]] += 1
        start_cnt[y][start[y][x]] += 1

# それぞれの行の整数値の数を揃える
# 上の行から揃えていく
for y in range(height):
    for x in range(width):
        c = start[y][x]
        # 整数値の数が同じならスキップ
        if start_cnt[y][c] == goal_cnt[y][c]:
            continue
        
        # 幅優先探索で交換先のセルを見つける
        visited = [[False for _ in range(width)] for _ in range(height  )]
        q = queue.SimpleQueue()
        q.put((x, y + 1))
        swapx = -1
        swapy = -1
        while(not q.empty()):
            sx, sy = q.get()
            if visited[sy][sx]:
                continue
            visited[sy][sx] = True
            # 交換対象の整数値がほしいやつかどうか
            cfrom = start[y][x]
            cto = start[sy][sx]
            if cfrom != cto and start_cnt[y][cto] - goal_cnt[y][cto] < 0:
                swapx = sx
                swapy = sy
                break

            for dx, dy in [(1, 0), (-1, 0), (0, 1)]:
                nx = sx + dx
                ny = sy + dy
                if nx >= 0 and nx < width and ny >= 0 and ny < height:
                    q.put((nx, ny))
        
        # 交換対象が見つからなかったらスキップ
        if swapx == -1:
            continue

        # 抜き型を実際に適用して解答を作る
        # 交換対象が元のセルより右側にある場合
        if x < swapx:
            for px in reversed(range(x, swapx)):
                # print("==========")
                # print(swapy, px, "左")
                # 左づめだから2
                answer.append(Act(0, px, swapy, 2))
                # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
                # print()
                start[swapy][px:width - 1], start[swapy][width - 1] =  start[swapy][px + 1:width], start[swapy][px]
                # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
        else:
            for px in range(swapx + 1, x + 1):
                # print("==========")
                # print(swapy, px, "右")
                # 左づめだから2
                answer.append(Act(0, px, swapy, 3))
                # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
                # print()
                start[swapy][1:px + 1], start[swapy][0] =  start[swapy][0:px], start[swapy][px]
                # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
        
        for py in reversed(range(y, swapy)):
                # print("==========")
                # print(py, x, "上")
                # 上づめだから0
                answer.append(Act(0, x, py, 0))
                # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
                # print()
                tmp = start[py][x]
                for i in range(py, height - 1):
                    start[i][x] = start[i + 1][x]
                start[height - 1][x] = tmp
                # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
        
        # 整数値の個数を再計算する
        start_cnt.clear()
        for sy in range(height):
            start_cnt.append({c: 0 for c in range(4)})
            for sx in range(width):
                start_cnt[sy][start[sy][sx]] += 1

print("行ごとに揃えました：{}".format(len(answer)))

stencils = {1: 0}
for n in range(1, 9):
    stencils[2 ** n] = n * 3 - 1

# 行ごとに復元する
for y in range(height):
    for x in range(width):
        if goal[y][x] == start[y][x]:
            continue
        
        sx = x
        # 無限大を示す定数
        bitcnt = 10000
        # 自分より右のセルから交換対象のセルを見つける
        for _sx in range(x + 1, width):
            if start[y][_sx] == goal[y][_sx]:
                dxcnt = int.bit_count(_sx - x)
                if dxcnt < bitcnt:
                    sx = _sx
                    bitcnt = dxcnt
        
            # 交換先のセルを見つけたなら
        while sx - x > 0:
            dx = -1
            for n in reversed(range(0, 9)):
                if 2 ** n <= sx - x:
                    dx = 2 ** n
                    break

            for sy in range(y, min(height, y+dx)):
                if (sy - y) % 2 == 1:
                    continue
                
                # print(len(start[sy][x:x+dx]),
                #       len(start[sy][width-dx:width]),
                #       len(start[sy][x:width-dx]),
                #       len(start[sy][x+dx:width]))
                # breakpoint()
                tmp = start[sy][x:x+dx]
                start[sy][x:width-dx] = start[sy][x+dx:width]
                start[sy][width-dx:width] = tmp
                
                
            answer.append(Act(stencils[dx], x, sy, 2))
            
            sx -= dx
        
        # for px in reversed(range(x, sx)):
        #     # print("==========")
        #     # print(y, px, "左")
        #     # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
        #     # print()
        #     tmp = start[y][px]
        #     start[y][px:width-1] = start[y][px+1:width]
        #     start[y][width-1] = tmp
        #     answer.append(Act(0, px, y, 2))
        #     # print("\n".join([" ".join([str(x) for x in line]) for line in start]))
        # break

print("復元しました：{}".format(len(answer)))

with open("answer.json", "w") as f:
    f.write(json.dumps({
        "n": len(answer),
        "ops": [
            {
                "p": ops.p,
                "x": ops.x,
                "y": ops.y,
                "s": ops.s
            }
            for ops in answer
        ]
    }))