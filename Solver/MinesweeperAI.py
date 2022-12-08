# December 7, 2022
# Jaeyoon Lee

import random


DXDY = ((1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1))

class MinesweeperAI:
    def __init__(self, w:int, h:int, n_mines:int, start=0):
        self.w = w
        self.h = h
        self.flags = []
        self.proceesd = []
        self.n_mines = n_mines
        self.start = start if isinstance(start, tuple) else (w//2, h//2)
        self.tiles:dict = {self.start:0}
        self.inputs = []

    def input(self, new_tiles:dict):
        for pos in new_tiles:
            if not pos in self.tiles.keys():
                self.tiles[pos] = new_tiles[pos]

    def next_move(self):
        to_open = []
        flaged = []
        for x,y in list(set(self.tiles)-set(self.proceesd)):
            if self.tiles[(x,y)]>0:
                count = 0
                n_flag = 0
                ds = []
                for dx,dy in DXDY:
                    if self.is_in_board(x+dx, y+dy) and self.not_in_opens(x+dx, y+dy):
                        count += 1
                        if self.not_in_flags(x+dx, y+dy):
                            ds.append((x+dx, y+dy))
                        else:
                            n_flag += 1
                if count == self.tiles[(x,y)]:
                    for pos in ds:
                        self.flag(pos)
                        flaged.append(pos)
                    self.proceesd.append((x,y))
                elif n_flag == self.tiles[(x,y)]:
                    for dx,dy in DXDY:
                        if (self.is_in_board(x+dx, y+dy) and self.not_in_opens(x+dx, y+dy)
                            and self.not_in_flags(x+dx, y+dy)):
                            to_open.append((x+dx,y+dy))
                    self.proceesd.append((x,y))
        while len(to_open)==0:
            newx,newy = random.randint(0,self.w-1), random.randint(0,self.h-1)
            if self.not_in_flags(newx,newy) and self.not_in_opens(newx,newy):
                to_open.append((newx, newy))
        return to_open, flaged

    def flag(self, pos:tuple[int,int]):
        if not pos in self.flags:
            self.flags.append(pos)

    def is_win(self):
        return len(self.flags)==self.n_mines

    def is_in_board(self, x, y):
        return (0 <= x < self.w) and (0 <= y < self.h)

    def not_in_opens(self, x, y):
        return not (x,y) in self.tiles.keys()
    
    def not_in_flags(self, x, y):
        return not(x, y) in self.flags

    def show(self):
        for y in range(self.h):
            for x in range(self.w):
                if (x,y) in self.tiles.keys():
                    print(self.tiles[(x,y)], end=' ')
                elif (x,y) in self.flags:
                    print('►', end=' ')
                else:
                    print('?', end=' ')
            print()
        print()
