import json
import sys
import queue

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
            # 左づめだから2
            answer.extend([Act(0, px, swapy, 2) for px in reversed(range(x, swapx))])
            start[swapy][x:swapx + 1] = reversed(start[swapy][x:swapx + 1])
        else:
            # 右詰めだから3
            answer.extend([Act(0, px, swapy, 3) for px in range(swapx, x)])
            start[swapy][swapx:x + 1] = reversed(start[swapy][swapx:x + 1])
        
        # 上詰めだから0
        answer.extend([Act(0, x, py, 0) for py in reversed(range(y, swapy))])
        for i in range((swapy - y + 2) // 2):
            start[y + i][x], start[swapy - i][x] = start[swapy - i][x], start[y + i][x]
        
        # 整数値の個数を再計算する
        start_cnt.clear()
        for sy in range(height):
            start_cnt.append({c: 0 for c in range(4)})
            for sx in range(width):
                start_cnt[sy][start[sy][sx]] += 1

# 行ごとに復元する
for y in range(height):
    for x in range(width):
        if goal[y][x] == start[y][x]:
            continue
        
        # 自分より右のセルから交換対象のセルを見つける
        for sx in range(x + 1, width):
            # 交換先のセルを見つけたなら
            if start[y][sx] == goal[y][x]:
                # 左詰め
                answer.extend([Act(0, px, y, 2) for px in reversed(range(x, sx))])
                start[y][x:sx + 1] = reversed(start[y][x:sx + 1])
                break

print(len(answer))
print("\n".join(map(str, start)))
print()
print("\n".join(map(str, goal)))
print()
for ops in answer:
    print("%d %d %d %d" % (ops.p, ops.x, ops.y, ops.s))