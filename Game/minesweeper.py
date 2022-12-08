# December 6, 2022
# Jaeyoon Lee

import pygame
import numpy as np
from random import randint
import os


# Constants
F = 50
size = 15,15 # width, height
WHITE = (255, 251, 233)
BLUE = (127, 233, 222)
BLACK = (38, 49, 89)
RED = (220, 53, 53)


class Board:
    def __init__(self, start:tuple[int,int], size:tuple[int, int], n_mines=-1):
        self.start = start # start position
        self.w, self.h = size # board size width x height
        self.n = int(self.w*self.h*0.12) if n_mines==-1 else n_mines # number of mines : 12% of board
        # board : [[{number, open, flag}, ...], ...]
        self.board = np.array([[{'n':0,'open':0,'flag':False} for _ in range(self.w)] for _ in range(self.h)])
        self.mines = [] # mines' position
        self.n_flag = 0 # number of flags
        self.dxdy = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)] # around positions
        for _ in range(self.n):
            # Create mines in random position
            game_start = True
            while game_start:
                x, y = randint(0,self.w-1), randint(0,self.h-1)
                if (x,y) in self.mines:
                    continue
                game_start = False
                for dx,dy in self.dxdy+[(0,0)]: 
                    if (x+dx,y+dy) == start: # if start position isn't zero (0)
                        game_start = True
            self.mines.append((x,y))
            self.board[y][x]['n'] = 'mine'
            for dx,dy in self.dxdy:
                # Add numbers around mines
                if (0 <= x+dx < self.w) and (0 <= y+dy < self.h):
                    if isinstance(self.board[y+dy][x+dx]['n'], int):
                        self.board[y+dy][x+dx]['n'] += 1
        # print basic info
        print(f'{self.w}x{self.h}\nMines: {self.n}')

    # This function opens a tile
    def open(self, pos:tuple[int,int], click=False):
        x,y = pos
        if self.is_flag(x,y):
            return -1
    
        elif self.is_mine(x,y):
            # Chain explosion
            for mx,my in self.mines:
                if not self.is_flag(mx,my):
                    self.board[my][mx]['open'] = 1
            return 0
    
        elif click:
            if self.is_open(x,y):
                # if user click an open tile
                count = 0
                for dx,dy in self.dxdy:
                    if self.is_in_board(x+dx,y+dy):
                        if self.is_flag(x+dx, y+dy):
                            count += 1
                if count == self.board[y][x]['n']:
                    # if number of flags == tile number
                    self.__recursion(x,y)
    
        if not self.is_open(x,y):
            self.board[y][x]['open'] = 1
            if not self.board[y][x]['n']:
                # if tile number is zero (0)
                self.__recursion(x,y)
        return 1

    # This function opens around it by using recursion
    def __recursion(self, x,y):
        for dx,dy in self.dxdy:
            if self.is_in_board(x+dx,y+dy):
                self.open((x+dx,y+dy))

    # This function puts the flag on a position
    def flag(self, pos:tuple[int,int]):
        x,y = pos
        if self.is_in_board(x,y):
            if not self.board[y][x]['open']:
                self.board[y][x]['flag'] = not(self.board[y][x]['flag'])
                if self.board[y][x]['flag']:
                    self.n_flag += 1
                else:
                    self.n_flag -= 1

    # This function checks win
    def is_win(self):
        if self.n_flag==self.n:
            for row in self.board:
                for e in row:
                    if isinstance(e['n'], int) and e['flag']:
                        return False
            return True
        else:
            return False

    # This function displays the number on tiles
    def text(self, n, x, y):
        number = font.render(str(n), True, BLACK)
        w,h = number.get_size()
        screen.blit(number, (x*F+(F-w)/2, y*F+(F-h)/2))

    # This Function draws the board
    def draw(self):
        for y, row in enumerate(self.board):
            for x, e in enumerate(row):
                if e['open']:
                    pygame.draw.rect(screen, WHITE, (x*F, y*F, F, F))
                    if isinstance(e['n'], int):
                        if e['n']!=0:
                            self.text(e['n'], x, y)
                    else:
                        pygame.draw.circle(screen, BLACK, ((x+0.5)*F, (y+0.5)*F), 15)
                else:
                    pygame.draw.rect(screen, BLUE, (x*F, y*F, F, F))
                    if e['flag']:
                        pygame.draw.polygon(screen, RED, [(x*F+17,y*F+15),(x*F+17,y*F+36),(x*F+36,y*F+25)])
                pygame.draw.rect(screen, BLACK, (x*F, y*F, F, F), 5)

    # This function checks mine on a position
    def is_mine(self, x, y):
        if self.is_in_board(x,y):
            return self.board[y][x]['n']=='mine'

    # This function checks the tile is open
    def is_open(self, x, y):
        if self.is_in_board(x,y):
            return self.board[y][x]['open']
    
    # This function checks flag is on a position
    def is_flag(self, x, y):
        if self.is_in_board(x,y):
            return self.board[y][x]['flag']

    # This function checks a position is in the board
    def is_in_board(self, x, y):
        return (0 <= x < self.w) and (0 <= y < self.h)

class Tiles:
    def __init__(self, w, h, size:tuple[int,int]):
        self.w = w
        self.h = h
        self.row, self.col = size
        self.tiles = []
        for y in range(self.row):
            for x in range(self.col):
                self.tiles.append(pygame.Rect(w*x, h*y, w, h))

    # check position is on any tiles, then return position of a tile
    def check_collide(self, pos):
        for idx, tile in enumerate(self.tiles):
            if tile.collidepoint(pos):
                tile_pos = [idx % self.row, idx//self.row]
                return tile_pos
        return [-1]

def main():
    # start at the center of the board
    start = (7,7)
    board = Board(start, size)
    board.draw()
    pygame.display.update()
    pygame.time.wait(300)
    board.open(start,click=True)

    tiles = Tiles(F,F,size)
    game = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN: # if user presses the return btn
                    # Reset the game
                    game = True
                    start = (7,7)
                    board = Board(start, size)
                    board.draw()
                    pygame.display.update()
                    pygame.time.wait(300)
                    board.open(start,click=True)

            elif event.type == pygame.MOUSEBUTTONUP and game:
                pos = pygame.mouse.get_pos()
                collide_pos = tiles.check_collide(pos)
                if collide_pos[0] != -1:
                    # Left Click : Open Tile
                    if event.button==1:
                        if not board.open(collide_pos,click=True):
                            game = False
                            print("BOOM")
                    # Right Click : Put Flag
                    elif event.button==3:
                        board.flag(collide_pos)
                if board.is_win():
                    game = False
                    print("WIN")

        board.draw()

        pygame.display.update()
        fps.tick(10)


if __name__=="__main__":
    # Initialize
    pygame.init()
    pygame.display.set_caption("Minesweeper")
    fps = pygame.time.Clock()
    screen = pygame.display.set_mode((F*size[0],F*size[1]))
    font = pygame.font.SysFont('arial', 20)
    current_path = os.path.dirname(__file__)
    main()
