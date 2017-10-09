import pygame, time
from pygame.locals import *
from random import randint as rand

pygame.init()
screen = pygame.Surface((1000, 100))
window = pygame.display.set_mode((screen.get_width() * 2, screen.get_height() * 2))


def constrain(val, lo, hi):
    # Because these things are useful :)
    if val <= lo:
        return lo
    elif val >= hi:
        return hi
    else:
        return val

conduct = 2
pieces = []
grid = [[0 for j in range(screen.get_height())] for i in range(screen.get_width())]


class Piece:
    def __init__(self, xin, yin, tin=2):
        self.x = xin
        self.y = yin
        self.temp = tin
        pieces.append(self)
        grid[xin][yin] = self

    def show(self):
        if self.x > 0:
            if isinstance(grid[self.x - 1][self.y], Piece):
                dt = grid[self.x - 1][self.y].temp - self.temp
                self.heat(dt/conduct)
                grid[self.x - 1][self.y].heat(-dt/conduct)
            elif rand(1, 2) == 2:
                self.heat(-self.temp / conduct)
                self.move(-1, 0)
            else:
                self.heat(-self.temp / conduct)
        if self.x + 1 < screen.get_width():
            if isinstance(grid[self.x + 1][self.y], Piece):
                dt = grid[self.x + 1][self.y].temp - self.temp
                self.heat(dt / conduct)
                grid[self.x + 1][self.y].heat(-dt / conduct)
            elif rand(1, 2) == 2:
                self.heat(-self.temp / conduct)
                self.move(1, 0)
            else:
                self.heat(-self.temp / conduct)
        if self.y > 0:
            if isinstance(grid[self.x][self.y - 1], Piece):
                dt = grid[self.x][self.y - 1].temp - self.temp
                self.heat(dt / conduct)
                grid[self.x][self.y - 1].heat(-dt / conduct)
                if dt < 0:
                    #swap(grid[self.x][self.y - 1], self)
                    #print("0a", self.y)
                    grid[self.x][self.y - 1], grid[self.x][self.y] = grid[self.x][self.y], grid[self.x][self.y - 1]
                    grid[self.x][self.y].y += 1
                    self.y -= 1
            else:
                self.heat(-self.temp / conduct)
        if self.y + 1 < screen.get_height():
            if isinstance(grid[self.x][self.y + 1], Piece):
                dt = grid[self.x][self.y + 1].temp - self.temp
                self.heat(dt / conduct)
                grid[self.x][self.y + 1].heat(-dt / conduct)
                if dt > 0:
                    #swap(grid[self.x][self.y + 1], self)
                    #print("0b", self.y)
                    grid[self.x][self.y + 1], grid[self.x][self.y] = grid[self.x][self.y], grid[self.x][self.y + 1]
                    grid[self.x][self.y].y -= 1
                    self.y += 1
            else:
                self.heat(-self.temp / conduct)
                self.move(0, 1)
        #print(self.x, self.y)
        screen.fill((constrain(int(self.temp * 2.55), 0, 255), constrain(255 - int(self.temp * 2.55), 0, 255), 255), (self.x, self.y, 1, 1))

    def heat(self, amt):
        self.temp += amt
        # print(amt, self.temp)

    def move(self, xmuch, ymuch):
        grid[self.x][self.y] = 0
        #print("1", self.y)
        self.x += xmuch
        self.y += ymuch
        #print("2", self.y)
        grid[self.x][self.y] = self

    def destroy(self):
        pieces.remove(self)
        grid[self.x][self.y] = 0

groundx = int(screen.get_width())
groundy = int(screen.get_height()/3)
for i in range(groundx):
    for j in range(2 * groundy, 3 * groundy): # 2 * groundy - int((groundy/2) * sin(i/30) * sin(i/60)), 3 * groundy):
        Piece(i, j + 1, (i/screen.get_width()) * 100)

while True:
    screen.fill((0, 0, 0))
    #print("NEXT")
    for p in pieces:
        p.show()
    window.blit(pygame.transform.scale2x(screen, window), (0, 0))
    pygame.display.flip()
    mousex, mousey = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        if e.type == MOUSEBUTTONDOWN:
            for i in range(-3, 4):
                for j in range(-3, 4):
                    x = int(mousex/2) + i
                    y = int(mousey/2) + j
                    if x >= 0 and x < screen.get_width() and y >= 0 and y < screen.get_height():
                        if grid[x][y] != 0:
                            grid[x][y].heat(100)
    x, y = int(mousex/2), int(mousey/2)
    if x >= 0 and x < screen.get_width() and y >= 0 and y < screen.get_height():
        if grid[x][y] != 0:
            print(grid[x][y].temp)
    for i in range(screen.get_width() - 5, screen.get_width()):
        for j in range(screen.get_height() - 5, screen.get_height()):
            if i >= 0 and i < screen.get_width() and j >= 0 and j < screen.get_height():
                if grid[i][j] != 0:
                    grid[i][j].heat(1)
