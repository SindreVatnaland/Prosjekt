import random

class Sudoku:
    def __init__(self):
        self.locked = []
        self.table = []
        self.comfirm = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.win = 0
    def make_table(self):
        row = [0]*9
        for i in range(9):
            self.table.append(row.copy())

    def update_table(self):
        print("y", "_"*24)
        for i in range(9):
            row = (self.table[i])
            print(f"{i+1}|", end=" ")
            if (i+1)%3 == 0:
                for j in range(9):
                    print(f"{row[j]}\u0332", end=" \u0332")
                    if j>0:
                        if (j+1)%3 == 0 and j+1 != 9:
                            print("|\u0332", end=" \u0332")
            else:
                for j in range(9):
                    print(row[j], end=" ")
                    if j>0:
                        if (j+1)%3 == 0 and j+1 != 9:
                            print("|", end=" ")

            print("|")
        print("   1 2 3   4 5 6   7 8 9  x")

    def check_win(self):
        vertical = []
        for i in range(9):
            if len(set(self.table[i]).intersection(self.comfirm)) == 9:
                for j in range(9):
                    vertical.append(self.table[j][i])
                if len(set(vertical).intersection(self.comfirm)) == 9:
                    vertical = []
                else:
                    return
            else:
                return
        self.win = 1



    def do_move(self):
        while True:
            try:
                x = int(input("Input x:\n> "))
                y = int(input("Input y:\n> "))
                if [y-1, x-1] in self.locked or x == 0 or y == 0:
                    print("Invalid location, try again!")
                    continue
                value = int(input("Enter a number trough 0 and 9:\n> "))
                if value == 2020:
                    self.solve()
                    break
                if value not in self.comfirm:
                    print("Invalid number, try again")
                    continue
                self.table[y-1][x-1] = value
                self.check_win()
                break
            except:
                print("Both inputs must be an int")
                continue



    def set_difficulty(self):
        self.make_table()
        while True:
            try:
                level = int(input("Choose difficulty\n1: Easy\n2: Medium\n3: Hard\n> "))
                break
            except:
                print("Invalid input, try again!")
                continue
        with open(f"{str(level)}.txt", "r") as f:
            list = []
            for lines in f:
                temp = lines.split(" ")
                list.append(temp)
            rand = list[random.randint(0,len(list)-1)]
            x = 0
            for i in range(9):
                for j in range(9):
                    self.table[i][j] = int(rand[i*9+j])
                    if int(rand[i*9+j]) != 0:
                        self.locked.append([i, j])
                x += 1

    def if_possible(self, x, y, n):
        for i in range(9):
            if self.table[y-1][i] == n or self.table[i][x-1] == n:
                return False
        x0 = ((x-1)//3)*3
        y0 = ((y-1)//3)*3
        for i in range(3):
            for j in range(3):
                if self.table[y0+i][x0+j] == n:
                    return False
        return True

    def solve(self):
        for x in range(1,10):
            for y in range(1, 10):
                if self.table[y-1][x-1] == 0:
                    for n in range(1, 10):
                        if self.if_possible(x, y, n):
                            self.table[y-1][x-1] = n
                            self.solve()
                            self.table[y-1][x-1] = 0

                    return

        self.update_table()
        pause = input("Enter to continue:\n> ")

    def play_game(self):
        self.set_difficulty()
        while self.win == 0:
            self.update_table()
            self.do_move()
        self.update_table()
        print("Gratulerer du vant!")

    def solve_game(self):
        self.set_difficulty()
        self.update_table()
        self.solve()
        print("Gratulerer du vant!")

if __name__ == '__main__':
    game = Sudoku()
    game.play_game()