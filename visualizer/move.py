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
                    if cells[b][a] == 1:
                        if not(y + b < 0 or x + a < 0 or y+b >= len(self.start_board) or x+a >= len(self.start_board[0])):
                            self.basic_move(x,y,s,a,b,cells)



        elif s == 1:
            for a in range(len(cells[0])):
                if  not(x + a < 0  or x+a >= len(self.start_board[0])) :#抜き型が場外
                    first_board = [row[x+a] for row in self.start_board]
                for b in range(len(cells)-1,-1,-1):
                    count+=1
                    if cells[b][a] == 1:
                        if not(y + b < 0 or x + a < 0 or y+b >= len(self.start_board) or x+a >= len(self.start_board[0])):
                            self.basic_move(x,y,s,a,b,cells)


        elif s == 2:
            for a in range(len(cells)):
                if not(  y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    first_board = [i for i in self.start_board[y+a]]
                for b in range(len(cells[0])):
                    count+=1
                    if cells[a][b] == 1:
                        if  not(y + a < 0 or x + b < 0 or y+a >= len(self.start_board) or x+b >= len(self.start_board[0])):#抜き型が場外
                            self.basic_move(x,y,s,a,b,cells)



        elif s == 3:
            for a in range(len(cells)):
                # one_count= -1
                if  not(y + a < 0  or y+a >= len(self.start_board))  :#抜き型が場外
                    first_board = [i for i in self.start_board[y+a]]
                for b in range(len(cells[0])-1,-1,-1):
                    count+=1
                    if cells[a][b] == 1:
                        if  not(y + a < 0 or x + b < 0 or y+a >= len(self.start_board) or x+b >= len(self.start_board[0])):#抜き型が場外
                            self.basic_move(x,y,s,a,b,cells)





    def basic_move(self,x,y,s,a,b,cells):
            true_count = 0
            remove = 0
            pre_x = -1 #座標を保存するための変数
            pre_y = -1
            first_board = []


            if s == 0:


                for i in range(y+b,len(self.start_board)-1):#動かそうとしているますの座標〜下端
                    if i-y+1 >= 0 and i-y+1 < len(cells):
                        if cells[i-y+1][a] == 1:
                            if pre_y == -1:
                                pre_y = i #前に動かす予定のますがあったら移動しない今動かそうとしているますの座標を保存する



                        else:
                            if pre_y != -1:
                                self.start_board[pre_y][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[pre_y][x+a]#上方向にずらす#保存していた座標と交換する
                                pre_y = -1
                            else:
                                # pre_y = -1
                                self.start_board[i][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[i][x+a]#上方向にずらす#座標が保存されず抜き型内で移動をする場合
                    else:
                        if pre_y != -1:
                            self.start_board[pre_y][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[pre_y][x+a]#上方向にずらす#保存していた座標と交換する
                            pre_y = -1

                        else:
                            self.start_board[i][x+a],self.start_board[i+1][x+a] = self.start_board[i+1][x+a],self.start_board[i][x+a]#上方向にずらす#抜き型外で移動を行う場合い
            elif s == 1:

                first_board = [row[x+a] for row in self.start_board]
                for i in range(y+b,0,-1):
                    if i-y-1 >= 0 and i-y-1 < len(cells):
                        if cells[i-y-1][a] == 1:
                            if pre_y == -1:
                                pre_y = i
                        else:
                            if pre_y != -1:
                                self.start_board[i-1][x+a],self.start_board[pre_y][x+a] = self.start_board[pre_y][x+a],self.start_board[i-1][x+a]
                                pre_y = -1
                            else:
                                # pre_y = -1
                                self.start_board[i][x+a],self.start_board[i-1][x+a] = self.start_board[i-1][x+a],self.start_board[i][x+a]
                    else:
                        if pre_y != -1:
                            self.start_board[i-1][x+a],self.start_board[pre_y][x+a] = self.start_board[pre_y][x+a],self.start_board[i-1][x+a]
                            pre_y = -1
                        else:
                            self.start_board[i][x+a],self.start_board[i-1][x+a] = self.start_board[i-1][x+a],self.start_board[i][x+a]

            elif s == 2:
                first_board = [i for i in self.start_board[y+a]]
                for i in range(x+b,len(self.start_board[0])-1):
                    if i-x+1 >= 0 and i-x+1 < len(cells[0]):
                        if cells[a][i-x+1] == 1:
                            if pre_x == -1:
                                pre_x = i
                        else:
                            if pre_x != -1:
                                self.start_board[y+a][pre_x],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][pre_x]#左方向にずらす
                                pre_x = -1

                            else:
                                self.start_board[y+a][i],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][i]#左方向にずらす
                    else:
                        if  pre_x != -1:
                            self.start_board[y+a][pre_x],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][pre_x]
                            pre_x = -1
                        else:
                            self.start_board[y+a][i],self.start_board[y+a][i+1] = self.start_board[y+a][i+1],self.start_board[y+a][i]#左方向にずらす

            elif s == 3:
                first_board = [i for i in self.start_board[y+a]]
                for i in range(x+b,0,-1):
                    if i-x-1 >= 0 and i-x-1 < len(cells[0]):
                        if cells[a][i-x-1] == 1:
                            if pre_x == -1:
                                pre_x = i
                        else:
                            if pre_x != -1:
                                self.start_board[y+a][pre_x],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][pre_x]
                                pre_x = -1
                            else:
                                # pre_x = -1
                                self.start_board[y+a][i],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][i]#右方向にずらす

                    else:
                        if pre_x != -1:
                            self.start_board[y+a][pre_x],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][pre_x]
                            pre_x = -1

                        else:
                            self.start_board[y+a][i],self.start_board[y+a][i-1] = self.start_board[y+a][i-1],self.start_board[y+a][i]#右方向にずらす


