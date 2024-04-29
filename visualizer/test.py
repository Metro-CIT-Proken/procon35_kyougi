#盤面の操作をテストする
import json

with open ('./problem.json') as f:
    problem = json.load(f)
with open('./answer.json') as f:
    answer = json.load(f)
b_wid = problem['board']['width']
b_hei = problem['board']['height']
start_board =  [[ 0 for x in range(b_wid)]for y in range(b_hei)]#スタート盤面
goal_board = [[ 0 for x in range(b_wid)]for y in range(b_hei)]#完成盤面



print(type(start_board))

for i in range(0,b_hei):
    for j in range(0,b_wid):
        start_board[i][j]=int(problem['board']['start'][i][j])#int*intのリストにする
        goal_board[i][j]=int(problem['board']['start'][i][j])#goalも同様


xys = []
n = True
mes = ['上','下','左','右']
#ボードの操作
for i in range(0,answer["n"]):
    xys.append([answer["ops"][i]["x"],answer["ops"][i]["y"],answer["ops"][i]["s"]])
# for i in range(0,len(xys)):
#     print(xys)

for i in range(0,len(xys)):
    x = xys[i][0]
    y = xys[i][1]
    s = xys[i][2]
    print(f"方向{mes[s]}:座標{x},{y}")
    for i in range(0,len(start_board)):
        print(start_board[i])
    print("==========================")
    if s == 0:
        for i in range(y,b_hei-1):
            start_board[i][x],start_board[i+1][x] = start_board[i+1][x],start_board[i][x]#上方向にずらす
    elif s == 1:
        for i in range(y,0,-1):
            start_board[i][x],start_board[i-1][x] = start_board[i-1][x],start_board[i][x]#下方向にずらす
    elif s == 2:
        for i in range(x,b_wid-1):
            start_board[y][i],start_board[y][i+1] = start_board[y][i+1],start_board[y][i]#左方向にずらす
    else:
        for i in range(x,0,-1):
            start_board[y][i],start_board[y][i-1] = start_board[y][i-1],start_board[y][i]#右方向にずらす

for i in range(0,len(start_board)):
    for j in range(0,len(start_board[0])):
        if goal_board[i][j] != start_board[i][j]:
            n = 0
if(n):
    print("######成功######")
else:
    print("######失敗######")


print("#######元に戻す#######")


for i in range(len(xys)-1,0,-1):
    board_y_size = len(start_board)
    board_x_size = len(start_board[0])

    if s == 0:
            for i in range(board_y_size-1,y,-1):
                start_board[i-1][x],start_board[i][x] = start_board[i][x],start_board[i-1][x]
    elif s == 1:
            for i in range(0,y):
                start_board[i][x],start_board[i+1][x] = start_board[i+1][x],start_board[i][x]

    elif s == 2:
            for i in range(board_x_size-1,x,-1):
                start_board[y][i],start_board[y][i-1] = start_board[y][i-1],start_board[y][i]

    else:
            for i in range(0,x):
                start_board[y][i],start_board[y][i+1] = start_board[y][i+1],start_board[y][i]
    for i in range(0,len(start_board)):
        print(start_board[i])
    print("==========================")
