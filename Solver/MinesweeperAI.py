# December 7, 2022
# Jaeyoon Lee

import random

# Constant: delta x&y around the position
DXDY = ((1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1))

class MinesweeperAI:
    def __init__(self, w:int, h:int, n_mines:int, start=0):
        """w: width, h: height, n_mines: number of mines, start: start position"""
        self.w = w
        self.h = h
        self.flags = [] # list of positions of flags
        self.processed = [] # list of positions that already processed
        self.n_mines = n_mines # number of mines
        # start position (default: center of the board)
        self.start = start if isinstance(start, tuple) else (w//2, h//2)
        self.tiles:dict = {self.start:0} # Open tiles

    # Add new open tiles
    def input(self, new_tiles:dict):
        for pos in new_tiles:
            if not pos in self.tiles.keys():
                self.tiles[pos] = new_tiles[pos]

    # main method
    def next_move(self):
        to_open = [] # tiles to open this turn
        flaged = []  # tiles to put flags this turn
        for x,y in list(set(self.tiles)-set(self.processed)): # for loop without processed tiles
            if self.tiles[(x,y)]>0:
                ds = [] # list of nearby positions that aren't open without flags
                n_flag = 0 # number of flags around the position
                for dx,dy in DXDY:
                    if self.not_in_opens(x+dx, y+dy):
                        if self.not_in_flags(x+dx, y+dy):
                            ds.append((x+dx, y+dy))
                        else:
                            n_flag += 1

                if len(ds)+n_flag == self.tiles[(x,y)]:
                    for pos in ds:
                        # if number of unopened tiles == tile number 
                        # flag all unopened tiles around the position
                        self.flag(pos)
                    # flaged += ds
                    self.processed.append((x,y))
                elif n_flag == self.tiles[(x,y)]:
                    # if number of flags == tile number
                    # Open all unopened tiles around the position
                    to_open += ds
                    self.processed.append((x,y))
    
        to_open = list(set(to_open))

        while len(to_open)==0:
            # if cannot open anymore,
            newx,newy = random.randint(0,self.w-1), random.randint(0,self.h-1)
            # pick a random location and open it
            if self.not_in_flags(newx,newy) and self.not_in_opens(newx,newy):
                to_open.append((newx, newy))

        return to_open, flaged

    # put a flag on the position
    def flag(self, pos:tuple[int,int]):
        if self.not_in_flags(pos[0],pos[1]):
            self.flags.append(pos)

    # check win
    def is_win(self):
        return len(self.flags)==self.n_mines

    # check position is in board
    def is_in_board(self, x, y):
        return (0 <= x < self.w) and (0 <= y < self.h)

    # check position is not in an opens list
    def not_in_opens(self, x, y):
        if self.is_in_board(x, y):
            return not (x,y) in self.tiles.keys()
    
    # check position is not in a flags list
    def not_in_flags(self, x, y):
        if self.is_in_board(x, y):
            return not(x, y) in self.flags

    # print the board on a terminal
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
