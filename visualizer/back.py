from termcolor import colored

class Back():
    def __init__(self,x,y,s,p,cells,start_board,goal_board):
        self.start_board = start_board
        self.goal_board = goal_board
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
            for j in range(x,x+len(cells[0])):
                counts = one_counts[j]
                first_board = [[self.start_board[b][a] for a in range(len(self.start_board[b])) if a == j] for b in range(len(self.start_board))]
                # first_board = [row[j] for row in self.start_board]
                for i in range(y,y+len(cells)):
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                counts-=1


        elif s == 1:
            for j in range(x,x+len(cells[0])):
                counts = one_counts[j]
                first_board = [[self.start_board[b][a] for a in range(len(self.start_board[b])) if a == j] for b in range(len(self.start_board))]
                # if j in one_counts:
                for i in range(y+len(cells)-1,y-1,-1):
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                counts-=1

        elif s == 2:
            for i in range(y,y+len(cells)):
                counts = one_counts[i]
                if i >= 0 and i < len(self.start_board):
                    first_board = [ retu for retu in self.start_board[i]]
                # for j in range(len(self.start_board[0])-one_counts[i],len(self.start_board)):
                for j in range(x,x+len(cells[0])):
                        if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                            if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                                if cells[i-y][j-x] == 1:
                                    self.basic_back(x,y,s,p,cells,one_counts,one_index_list,i,j,counts)
                                    counts-=1


        elif s == 3:
            for i in range(y,y+len(cells)):
                counts = one_counts[i]
                if i >= 0 and i < len(self.start_board):
                    first_board = [ retu for retu in self.start_board[i]]
                for j in range(x+len(cells[0])-1,x-1,-1):
                    if i >= 0 and j >= 0 and i < len(self.start_board) and j < len(self.start_board[0]):
                        if i-y >= 0 and j-x >= 0 and i-y < len(cells) and j-x < len(cells[0]):
                            if cells[i-y][j-x] == 1:
                                self.basic_back(x,y,s,p,cells,one_counts,one_index_dic,i,j,counts)
                                counts-=1







    def basic_back(self,x,y,s,p,cells,one_counts,one_index_dic:dict,i,j,counts):


        if s == 0:

            for a in range(len(self.start_board)-counts,i,-1):
                self.start_board[a][j],self.start_board[a-1][j] = self.start_board[a-1][j],self.start_board[a][j]
        elif s== 1:
            for a in range(counts-1,i):
                self.start_board[a][j],self.start_board[a+1][j] = self.start_board[a+1][j],self.start_board[a][j]
        elif s == 2:
            for a in range(len(self.start_board[0])-counts,j,-1):

                self.start_board[i][a],self.start_board[i][a-1] = self.start_board[i][a-1],self.start_board[i][a]
        elif s == 3:
            for a in range(counts-1,j):
                self.start_board[i][a],self.start_board[i][a+1] = self.start_board[i][a+1],self.start_board[i][a]



