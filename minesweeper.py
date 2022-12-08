

import pygame
import numpy as np
from random import randint
import os

F = 50
size = 15,15 # width, height
WHITE = (255, 251, 233)
BLUE = (127, 233, 222)
BLACK = (38, 49, 89)
RED = (220, 53, 53)


class Board:
    def __init__(self, start:tuple[int,int], size:tuple[int, int], n_mines=-1):
        self.start = start
        self.w, self.h = size
        self.n = int(self.w*self.h*0.12) if n_mines==-1 else n_mines
        self.board = np.array([[{'n':0,'open':0,'flag':False} for _ in range(self.w)] for _ in range(self.h)])
        self.mines = []
        self.n_flag = 0
        self.dxdy = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        for _ in range(self.n):
            game_start = True
            while game_start:
                x, y = randint(0,self.w-1), randint(0,self.h-1)
                if (x,y) in self.mines:
                    continue
                game_start = False
                for dx,dy in self.dxdy+[(0,0)]:
                    if (x+dx,y+dy) == start:
                        game_start = True
            self.mines.append((x,y))
            self.board[y][x]['n'] = 'mine'
            for dx,dy in self.dxdy:
                if (0 <= x+dx < self.w) and (0 <= y+dy < self.h):
                    if isinstance(self.board[y+dy][x+dx]['n'], int):
                        self.board[y+dy][x+dx]['n'] += 1
        print(f'{self.w}x{self.h}\nMines: {self.n}')
        self.data = []

    def open(self, pos:tuple[int,int], click=False):
        x,y = pos
        if self.is_flaged(x,y):
            return -1
        elif self.is_mine(x,y):
            for mx,my in self.mines:
                if not self.is_flaged(mx,my):
                    self.board[my][mx]['open'] = 1
            return 0
        elif click:
            if self.is_opened(x,y):
                count = 0
                for dx,dy in self.dxdy:
                    if self.is_in_board(x+dx,y+dy):
                        if self.is_flaged(x+dx, y+dy):
                            count += 1
                if count == self.board[y][x]['n']:
                    for dx,dy in self.dxdy:
                        if self.is_in_board(x+dx,y+dy):
                            self.open((x+dx,y+dy))
        if not self.is_opened(x,y):
            self.board[y][x]['open'] = 1
            if not self.board[y][x]['n']:
                for dx,dy in self.dxdy:
                    if self.is_in_board(x+dx,y+dy):
                        self.open((x+dx,y+dy))
        return 1

    def flag(self, pos:tuple[int,int]):
        x,y = pos
        if not self.board[y][x]['open']:
            self.board[y][x]['flag'] = not(self.board[y][x]['flag'])
            if self.board[y][x]['flag']:
                self.n_flag += 1
            else:
                self.n_flag -= 1

    def is_win(self):
        if self.n_flag==self.n:
            for row in self.board:
                for e in row:
                    if isinstance(e['n'], int) and e['flag']:
                        return False
            return True
        else:
            return False

    def text(self, n, x, y):
        number = font.render(str(n), True, BLACK)
        w,h = number.get_size()
        screen.blit(number, (x*F+(F-w)/2, y*F+(F-h)/2))

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

    def is_mine(self, x, y):
        return self.board[y][x]['n']=='mine'

    def is_opened(self, x, y):
        return self.board[y][x]['open']
    
    def is_flaged(self, x, y):
        return self.board[y][x]['flag']

    def is_in_board(self, x, y):
        return (0 <= x < self.w) and (0 <= y < self.h)

    def save(self):
        file_name = os.path.join(current_path, 'data.txt')
        txt_file = open(file_name, 'a')
        txt_file.write(self.data+'\n')
        txt_file.close()
        print("Save complete.")

class Tiles:
    def __init__(self, w, h, size:tuple[int,int]):
        self.w = w
        self.h = h
        self.row, self.col = size
        self.tiles = []
        for y in range(self.row):
            for x in range(self.col):
                self.tiles.append(pygame.Rect(w*x, h*y, w, h))

    def check_collide(self, pos):
        for idx, tile in enumerate(self.tiles):
            if tile.collidepoint(pos):
                tile_pos = [idx % self.row, idx//self.row]
                return tile_pos
        return [-1]

def main():
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
                if event.key == pygame.K_RETURN:
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
                    # Left Click
                    if event.button==1:
                        if not board.open(collide_pos,click=True):
                            game = False
                            print("BOOM")
                    # Right Click
                    elif event.button==3:
                        board.flag(collide_pos)
                if board.is_win():
                    game = False
                    print("WIN")
                    board.save()

        board.draw()

        pygame.display.update()
        fps.tick(10)


if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption("Minesweeper")
    fps = pygame.time.Clock()
    screen = pygame.display.set_mode((F*size[0],F*size[1]))
    font = pygame.font.SysFont('arial', 20)
    current_path = os.path.dirname(__file__)
    main()
