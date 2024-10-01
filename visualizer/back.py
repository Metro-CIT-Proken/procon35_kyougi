from termcolor import colored

class Back():
    def __init__(self,x,y,s,p,cells,start_board,goal_board):
        self.start_board = start_board
        self.goal_board = goal_board
        print("back")
        pre_start = [[ self.start_board[i][j]  for j in range(0,len(self.start_board[i]))] for i in range(0,len(self.start_board))]
        first_board = []
        one_counts = {}
        one_index_dic = {}
        one_index_list = []
        if s == 0 or s==1:
            for j in range(len(cells[0])):
                one_count = 0
                one_index_list = []
                for i in range(len(cells)):
                    if cells[i][j] == 1:
                        if  not(y + i < 0 or x + j < 0 or y+i >= len(self.start_board) or x+j >= len(self.start_board[0])):#抜き型が場外
                            one_count+=1
                            one_index_list.append(i+y)
                one_counts[j+x] = one_count
                one_index_dic[j+x] = one_index_list

        elif s == 2 or s == 3:
            for i in range(len(cells)):
                one_count = 0
                one_index_list = []
                for j in range(len(cells[0])):
                    if cells[i][j] == 1:
                        if  not(y + i < 0 or x + j < 0 or y+i >= len(self.start_board) or x+j >= len(self.start_board[0])):#抜き型が場外
                            one_count+=1
                            one_index_list.append(j+x)
                one_counts[i+y] = one_count
                one_index_dic[i+y] = one_index_list
        if s == 1 or s == 3:
            one_index_list.reverse

        counts = 0
        if s == 0:
            print("s=0")
            for j in range(x,x+len(cells[0])):
                print(f"j:{j}")
                counts = one_counts[j]
                first_board = [[self.start_board[b][a] for a in range(len(self.start_board[b])) if a == j] for b in range(len(self.start_board))]
                # first_board = [row[j] for row in self.start_board]
                for i in range(y,y+len(cells)):
                    print(f"j:{j} i:{i}")
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            print(f"i-y {i-y} j-x {j-x}")
                            if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                counts-=1


        elif s == 1:
            print("s=1")
            for j in range(x,x+len(cells[0])):
                print(f"i:{i}")
                counts = one_counts[j]
                first_board = [[self.start_board[b][a] for a in range(len(self.start_board[b])) if a == j] for b in range(len(self.start_board))]
                # if j in one_counts:
                for i in range(y+len(cells)-1,y-1,-1):
                    print(f"j:{j} i:{i}")
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            print(f"i-y {i-y} j-x {j-x}")
                            if cells[i-y][j-x] == 1:
                            # if i >= 0 and i < len(cells) and j >= 0 and j < len(cells[0]):
                            #     if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                counts-=1

        elif s == 2:
            print("s=2")
            for i in range(y,y+len(cells)):
                print(f"i:{i}")
                # if i in one_counts:
                print(f"back x start {x}")
                print(f"back x end {x+len(cells[0])}")
                print(f"back start: {y}")
                print(f"back end: {y+len(cells)}")
                counts = one_counts[i]
                if i >= 0 and i < len(self.start_board):
                    first_board = [ retu for retu in self.start_board[i]]
                # for j in range(len(self.start_board[0])-one_counts[i],len(self.start_board)):
                for j in range(x,x+len(cells[0])):
                        print(f"j:{j} i:{i}")
                        if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                            if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                                print(f"i-y {i-y} j-x {j-x}")
                                if cells[i-y][j-x] == 1:
                            # if i-y >= 0 and i-y < len(cells) and one_index_dic[i]-x >= 0 and one_index_dic[i]-x < len(cells[0]):
                            #     print("safe")
                            #     if cells[i-y][one_index_dic[i]-x] == 1:
                                    self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                    counts-=1
                print("最初")
                print(first_board)
                print("最後")
                if i >= 0 and i < len(self.start_board):
                    print([ retu for retu in self.start_board[i]])


        elif s == 3:
            print("s=3")
            for i in range(y,y+len(cells)):
                print(f"i:{i}")
                # if i in one_counts:
                # for j in range(one_counts[i]-1,-1,-1):
                print(f"back x start {x+len(cells[0])-1}")
                print(f"back x end {x-2}")
                print(f"back y start: {y}")
                print(f"back y end: {y+len(cells)}")
                counts = one_counts[i]
                if i >= 0 and i < len(self.start_board):
                    first_board = [ retu for retu in self.start_board[i]]
                for j in range(x+len(cells[0])-1,x-1,-1):
                    print(f"j:{j} i:{i}")
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        print(f"i-y {i-y} j-x {j-x}")
                        print("bbbbbbbbbbbbbbbbbbbbbbb")
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            print(f"i-y {i-y} j-x {j-x}")
                            if cells[i-y][j-x] == 1:
                            # if i >= 0 and i < len(cells) and one_index_dic[i]-x >= 0 and one_index_dic[i]-x < len(cells[0]):
                            #     if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_dic,i,j,counts)
                                counts-=1
                print("最初")
                print(first_board)
                print("最後")
                if i >= 0 and i < len(self.start_board):
                    print([ retu for retu in self.start_board[i]])

        print(f"s: {s}")
        print("cells:")
        for i in range(len(cells)):
            print(cells[i])

        print("変更前")
        for i in range(len(pre_start)):
            print()
            for j in range(len(pre_start[0])):
                if (i >= y and j >= x) and (i < y+len(cells) and j < x+len(cells[0])):
                    if s == 0 or s == 1:
                        print(colored(str(pre_start[i][j])+'*', "red"))
                        print()
                    else:
                        print(colored(str(pre_start[i][j])+'*', "red"),end=" ")
                else:
                    if s == 0 or s == 1:
                        print(str(pre_start[i][j])+'+')
                        print()
                    else:
                        print(str(pre_start[i][j])+'+',end=" ")
        print()
        print("変更後")
        for i in range(len(self.start_board)):
            print()
            for j in range(len(self.start_board[0])):
                if (i >= y and j >= x) and (i < y+len(cells) and j < x+len(cells[0])):
                    print(colored(str(self.start_board[i][j])+'*', "red"),end=" ")
                else:
                    print(str(self.start_board[i][j])+'+',end=" ")
        print()




    def basic_back(self,x,y,s,p,cells,one_counts,one_index_dic:dict,i,j,counts):
        print("basic_back")
        print(f"basic_back:  i {i},j {j}")
        print(f"counts: {counts}")


        if s == 0:
            print(f"start: {len(self.start_board)-1-counts} end: {i+1}")
            for a in range(len(self.start_board)-counts,i,-1):
                self.start_board[a][j],self.start_board[a-1][j] = self.start_board[a-1][j],self.start_board[a][j]
                print(f"move!:  {self.start_board[i]}")
        elif s== 1:
            print(f"start: {len(self.start_board)-1+counts} end: {i-1}")
            for a in range(counts-1,i):
                self.start_board[a][j],self.start_board[a+1][j] = self.start_board[a+1][j],self.start_board[a][j]
                print(f"move!:  {self.start_board[i]}")
        elif s == 2:
            print(f"直前 {self.start_board[i]}")
            print(f"start: {len(self.start_board[0])-counts} end: {j+1}")
            for a in range(len(self.start_board[0])-counts,j,-1):
                print(f"a: {a}")

                self.start_board[i][a],self.start_board[i][a-1] = self.start_board[i][a-1],self.start_board[i][a]
                print(f"move!: {a} & {a-1} :{self.start_board[i]}")
        elif s == 3:
            print(f"直前 {self.start_board[i]}")
            print(f"start: {counts-1} end: {j-2}")
            for a in range(counts-1,j):
                self.start_board[i][a],self.start_board[i][a+1] = self.start_board[i][a+1],self.start_board[i][a]
                print(f"move!: {a} & {a+1}: {self.start_board[i]}")



