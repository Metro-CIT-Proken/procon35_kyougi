class Move():
    def __init__(self,x,y,s,cells,start_board,goal_board):
        self.start_board = start_board
        self.goal_board = goal_board
        count = 0
        first_board = []
        if s == 0:
            for a in range(len(cells[0])):
                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    first_board = [row[x+a] for row in self.start_board]
                for b in range(len(cells)):
                    count+=1
                    print(f"a: {a},b: {b}")
                    if cells[b][a] == 1:
                        if not(y + b < 0 or x + a < 0 or y+b >= len(self.start_board) or x+a >= len(self.start_board[0])):
                            self.basic_move(x,y,s,a,b,cells)

                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    print(f"x:{x}")
                    print(f"y:{y}")
                    print(f"s:{s}")
                    print(f"cells:")
                    for i in range(len(cells)):
                        print(cells[i])
                    print(f"{a}列目")
                    print("手最初")
                    print(first_board)
                    print("手最後")
                    print([row[x+a] for row in self.start_board])

        elif s == 1:
            for a in range(len(cells[0])):
                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    first_board = [row[x+a] for row in self.start_board]
                for b in range(len(cells)-1,-1,-1):
                    count+=1
                    print(f"a: {a},b: {b}")
                    if cells[b][a] == 1:
                        if not(y + b < 0 or x + a < 0 or y+b >= len(self.start_board) or x+a >= len(self.start_board[0])):
                            self.basic_move(x,y,s,a,b,cells)

                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    print(f"x:{x}")
                    print(f"y:{y}")
                    print(f"s:{s}")
                    print(f"cells:")
                    for i in range(len(cells)):
                        print(cells[i])
                    print(f"{a}列目")
                    print("手最初")
                    print(first_board)
                    print("手最後")
                    print([row[x+a] for row in self.start_board])
        elif s == 2:
            for a in range(len(cells)):
                if not(  y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    first_board = [i for i in self.start_board[y+a]]
                for b in range(len(cells[0])):
                    count+=1
                    print(f"a: {a},b: {b}")
                    if cells[a][b] == 1:
                        if  not(y + a < 0 or x + b < 0 or y+a >= len(self.start_board) or x+b >= len(self.start_board[0])):#抜き型が場外
                            self.basic_move(x,y,s,a,b,cells)

                if not(  y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    print(f"x:{x}")
                    print(f"y:{y}")
                    print(f"s:{s}")
                    print(f"cells:")
                    for i in range(len(cells)):
                        print(cells[i])
                    print(f"{a}行目")
                    print("手最初")
                    print(first_board)
                    print("手最終")
                    print(self.start_board[y+a])

        elif s == 3:
            for a in range(len(cells)):
                # one_count= -1
                if  not(y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    first_board = [i for i in self.start_board[y+a]]
                for b in range(len(cells[0])-1,-1,-1):
                    count+=1
                    print(f"a: {a},b: {b}")
                    if cells[a][b] == 1:
                        if  not(y + a < 0 or x + b < 0 or y+a >= len(self.start_board) or x+b >= len(self.start_board[0])):#抜き型が場外
                            self.basic_move(x,y,s,a,b,cells)

                if  not(y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    print(f"x:{x}")
                    print(f"y:{y}")
                    print(f"s:{s}")
                    print(f"cells:")
                    for i in range(len(cells)):
                        print(cells[i])
                    print(f"{a}行目")
                    print("手最初")
                    print(first_board)
                    print("手最終")
                    print(self.start_board[y+a])
        print(count)

        if self.goal_board == self.start_board:
            print("=========================== GOAL!!! ==================")



    def basic_move(self,x,y,s,a,b,cells):
            print("basic_move")
            true_count = 0
            remove = 0
            pre_x = -1 #座標を保存するための変数
            pre_y = -1
            first_board = []


            if s == 0:


                print("最初")
                print(first_board)
                for i in range(y+b,len(self.start_board)-1):#動かそうとしているますの座標〜下端
                    # print(f"s:{s} i:{i} remove:{remove}")
                    print(f"i: {i}")
                    if i-y+1 >= 0 and i-y+1 < len(cells):
                        if cells[i-y+1][a] == 1:
                            print(f"i-y+1: {i-y+1}")
                            # remove+=1
                            if pre_y == -1:
                                pre_y = i #前に動かす予定のますがあったら移動しない今動かそうとしているますの座標を保存する
                                print(f"s:{s} i:{i} pre_x: {pre_x} pre_y: {pre_y}")


                        else:
                            # self.start_board[i][x+a],self.start_board[i+1+remove][x+a] = self.start_board[i+1+remove][x+a],self.start_board[i][x+a]#上方向にずらす
                            if pre_y != -1:
                                self.start_board[pre_y][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[pre_y][x+a]#上方向にずらす#保存していた座標と交換する
                                print(f"move_pre!: {pre_y}, {i+1}")
                                print([row[x+a] for row in self.start_board])
                                pre_y = -1
                            else:
                                # pre_y = -1
                                self.start_board[i][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[i][x+a]#上方向にずらす#座標が保存されず抜き型内で移動をする場合
                                print(f"move_in!")
                                print([row[x+a] for row in self.start_board])
                            # remove = 0
                    # remove = 0
                    # pre_y = -1
                    else:
                        if pre_y != -1:
                            self.start_board[pre_y][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[pre_y][x+a]#上方向にずらす#保存していた座標と交換する
                            print(f"move_in_pre!: {pre_y}, {i+1}")
                            print([row[x+a] for row in self.start_board])
                            pre_y = -1

                        else:
                            self.start_board[i][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[i][x+a]#上方向にずらす#抜き型外で移動を行う場合い
                            print([row[x+a] for row in self.start_board])
                            print(f"move!")
                print("最初")
                print(first_board)
                print("最終")
                print([row[x+a] for row in self.start_board])

            elif s == 1:

                first_board = [row[x+a] for row in self.start_board]
                print("最初")
                print(first_board)
                for i in range(y+b,0,-1):
                    print(f"i: {i}")
                    if i-y-1 >= 0 and i-y-1 < len(cells):
                        if cells[i-y-1][a] == 1:
                            print(f"i-y-1: {i-y-1}")
                            if pre_y == -1:
                                pre_y = i
                                print(f"s:{s} i:{i} pre_x: {pre_x} pre_y: {pre_y}")
                            # remove-=1
                        else:
                            # self.start_board[i][x+a],self.start_board[i-1+remove][x+a] = self.start_board[i-1+remove][x+a],self.start_board[i][x+a]
                            if pre_y != -1:
                                self.start_board[i-1][x+a],self.start_board[pre_y][x+a] = self.start_board[pre_y][x+a],self.start_board[i-1][x+a]
                                print(f"move_pre!: {pre_y}, {i-1}")
                                print([row[x+a] for row in self.start_board])
                                pre_y = -1
                            else:
                                # pre_y = -1
                                self.start_board[i][x+a],self.start_board[i-1][x+a] = self.start_board[i-1][x+a],self.start_board[i][x+a]
                                print("move!_in")
                                print([row[x+a] for row in self.start_board])
                            # remove = 0
                    else:
                        if pre_y != -1:
                            self.start_board[i-1][x+a],self.start_board[pre_y][x+a] = self.start_board[pre_y][x+a],self.start_board[i-1][x+a]
                            (f"move_pre_in!: {pre_y}, {i-1}")
                            pre_y = -1
                            print([row[x+a] for row in self.start_board])
                        else:
                            self.start_board[i][x+a],self.start_board[i-1][x+a] = self.start_board[i-1][x+a],self.start_board[i][x+a]
                            print("move!")
                            print([row[x+a] for row in self.start_board])
                print("最初")
                print(first_board)
                print("最終")
                print([row[x+a] for row in self.start_board])

            elif s == 2:
                first_board = [i for i in self.start_board[y+a]]
                print("最初")
                print(first_board)
                for i in range(x+b,len(self.start_board[0])-1):
                    print(f"i: {i}")
                    if i-x+1 >= 0 and i-x+1 < len(cells[0]):
                        if cells[a][i-x+1] == 1:
                            print(f"i-x+1: {i-x+1}")
                            if pre_x == -1:
                                pre_x = i
                                print(f"s:{s} i:{i} pre_x: {pre_x} pre_y: {pre_y}")
                        else:
                            if pre_x != -1:
                                self.start_board[y+a][pre_x],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][pre_x]#左方向にずらす
                                print(f"move_pre!: {pre_x} {i+1}")
                                print(self.start_board[y+a])
                                pre_x = -1

                            else:
                                self.start_board[y+a][i],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][i]#左方向にずらす
                                print("move_in!")
                                print(self.start_board[y+a])
                    else:
                        if  pre_x != -1:
                            self.start_board[y+a][pre_x],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][pre_x]
                            print(f"move_pre_in!: {pre_x} {i+1}")
                            print(self.start_board[y+a])
                            pre_x = -1
                        else:
                            self.start_board[y+a][i],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][i]#左方向にずらす
                            print(self.start_board[y+a])
                        print("move!")
                print("最初")
                print(first_board)
                print("最終")
                print(self.start_board[y+a])

            elif s == 3:
                first_board = [i for i in self.start_board[y+a]]
                print("最初")
                print(first_board)
                for i in range(x+b,0,-1):
                    print(f"i: {i}")
                    if i-x-1 >= 0 and i-x-1 < len(cells[0]):
                        if cells[a][i-x-1] == 1:
                            print(f"i-x-1: {i-x-1}")
                            if pre_x == -1:
                                pre_x = i
                                print(f"s:{s} i:{i} pre_x: {pre_x} pre_y: {pre_y}")
                        else:
                            if pre_x != -1:
                                self.start_board[y+a][pre_x],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][pre_x]
                                print(f"move_pre!: {pre_x} {i-1}")
                                print(self.start_board[y+a])
                                pre_x = -1
                            else:
                                # pre_x = -1
                                self.start_board[y+a][i],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][i]#右方向にずらす
                                print("move_in!")
                                print(self.start_board[y+a])

                    else:
                        if pre_x != -1:
                            self.start_board[y+a][pre_x],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][pre_x]
                            print(f"move_pre_in!: {pre_x} {i-1}")
                            print(self.start_board[y+a])
                            pre_x = -1

                        else:
                            self.start_board[y+a][i],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][i]#右方向にずらす
                            print("move!")
                            print(self.start_board[y+a])
                print("最初")
                print(first_board)
                print("最終")
                print(self.start_board[y+a])


