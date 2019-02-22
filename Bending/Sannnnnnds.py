# For making images appear out of the sands

import pygame
from pygame.locals import *
from random import randint, shuffle
from math import sin

pygame.init()
screen = pygame.Surface((120, 250))                                                  # The actual screen for playing
window = pygame.display.set_mode((screen.get_width() * 2, screen.get_height() * 2))  # The scaled-up screen for viewing


def constrain(val, lo, hi):
    # Because these things are useful :)
    if val <= lo:
        return lo
    elif val >= hi:
        return hi
    else:
        return val


# A filled-in block
blank = pygame.Surface((20, 20))
blank.set_colorkey((255, 255, 255))

# A large fist in a number of orientations
FIST = pygame.image.load_extended("D:\\Users\\Charles Turvey\\Documents\\Python\\FIST.png")
FIST = pygame.transform.scale(FIST, (20, 20))
FIST.set_colorkey((255, 255, 255))
FIST.convert()
rightFIST = pygame.transform.rotate(FIST, -90)
leftFIST = pygame.transform.flip(rightFIST, True, False)

# A large dragon, facing left or right
leftDRAGON = pygame.image.load_extended("D:\\Users\\Charles Turvey\\Documents\\Python\\DRAGON.png")
leftDRAGON = pygame.transform.scale(leftDRAGON, (40*int(leftDRAGON.get_width()/leftDRAGON.get_height()), 40))
leftDRAGON.set_colorkey((255, 255, 255))
leftDRAGON.convert()
rightDRAGON = pygame.transform.flip(leftDRAGON, True, False)

# SANS
SANS = pygame.image.load_extended(r"D:\Users\Charles Turvey\Pictures\Art\Wah\WahFaceSans.png")
SANS.set_colorkey((0, 0, 0))
SANS.convert()

# A list of all the grains
pieces = []
# The game grid with references to the grains and players at their relevant positions
grid = [[0 for j in range(screen.get_height())] for i in range(screen.get_width())]
# A dictionary of the players with their names as keys
players = dict()

# The class for the sand grains
class Piece:
    def __init__(self, xin, yin, col=(100, 100, 100)):
        # The x,y position of the grain
        self.x = xin
        self.y = yin
        # The grain colour
        self.col = col
        # The position to which the grain is trying to move; (-1, -1) represents staying put
        self.target = (-1, -1)
        # A timer indicating for how long, in cycles, it will attempt to get to its target
        self.focus = 0
        # Adds itself to the list of grains and the grid in the relevant position
        pieces.append(self)
        grid[xin][yin] = self

    def show(self):
        if self.focus > 0:   # If it's still striving to reach its target
            self.focus -= 1  # ...decrement the focus counter, as it has used up one cycle of doing so
            if self.y != self.target[1]:
                if self.y < self.target[1]:
                    if self.y + 1 < screen.get_height():
                        if isinstance(grid[self.x][self.y + 1], Piece):
                            if grid[self.x][self.y + 1].focus == 0:
                                grid[self.x][self.y + 1].settarget(self.target[0], self.target[1], self.focus)
                                self.focus = 0
                        elif grid[self.x][self.y + 1] != 0:
                            if players[grid[self.x][self.y + 1]].kick(0, 1):
                                self.move(0, 1)
                        else:
                            self.move(0, 1)
                else:
                    if self.y > 0:
                        if isinstance(grid[self.x][self.y - 1], Piece):
                            if grid[self.x][self.y - 1].focus == 0:
                                grid[self.x][self.y - 1].settarget(self.target[0], self.target[1], self.focus)
                                self.focus = 0
                        elif grid[self.x][self.y - 1] != 0:
                            if players[grid[self.x][self.y - 1]].kick(0, -1):
                                self.move(0, -1)
                        else:
                            self.move(0, -1)
            elif self.x != self.target[0]:
                if self.x < self.target[0]:
                    if self.x + 1 < screen.get_width():
                        if isinstance(grid[self.x + 1][self.y], Piece):
                            if grid[self.x + 1][self.y].focus == 0:
                                grid[self.x + 1][self.y].settarget(self.target[0], self.target[1], self.focus)
                                self.focus = 0
                        elif grid[self.x + 1][self.y] != 0:
                            if players[grid[self.x + 1][self.y]].kick(1, 0):
                                self.move(1, 0)
                        else:
                            self.move(1, 0)
                else:
                    if self.x > 0:
                        if isinstance(grid[self.x - 1][self.y], Piece):
                            if grid[self.x - 1][self.y].focus == 0:
                                grid[self.x - 1][self.y].settarget(self.target[0], self.target[1], self.focus)
                                self.focus = 0
                        elif grid[self.x - 1][self.y] != 0:
                            if players[grid[self.x - 1][self.y]].kick(-1, 0):
                                self.move(-1, 0)
                        else:
                            self.move(-1, 0)
        elif self.y + 1 < screen.get_height():
            if grid[self.x][self.y + 1] == 0:
                self.move(0, 1)
        # Draws itself on the game screen
        screen.fill(self.col, (self.x, self.y, 1, 1))

    def move(self, xmuch, ymuch):
        grid[self.x][self.y] = 0
        self.x += xmuch
        self.y += ymuch
        grid[self.x][self.y] = self

    def destroy(self):
        pieces.remove(self)
        grid[self.x][self.y] = 0

    def settarget(self, x, y, focin=100, replace=False):
        x = constrain(x, 0, screen.get_width() - 1)
        y = constrain(y, 0, screen.get_height() - 1)
        self.target = (x, y)
        self.focus = focin
        if replace:
            if self.x + 1 < screen.get_width():
                if isinstance(grid[self.x + 1][self.y], Piece):
                    if grid[self.x + 1][self.y].focus == 0:
                        grid[self.x + 1][self.y].settarget(self.x, self.y, 10)
                        return 0
            if self.x > 0:
                if isinstance(grid[self.x - 1][self.y], Piece):
                    if grid[self.x - 1][self.y].focus == 0:
                        grid[self.x - 1][self.y].settarget(self.x, self.y, 10)
                        return 0
            if self.y + 1 < screen.get_height():
                if isinstance(grid[self.x][self.y + 1], Piece):
                    if grid[self.x][self.y + 1].focus == 0:
                        grid[self.x][self.y + 1].settarget(self.x, self.y, 10, True)
                        return 0


class Player:
    def __init__(self, playerid, xin, yin, col=(100, 100, 100)):
        self.x = xin
        self.y = yin
        self.vx = 0
        self.vy = 0
        self.col = col
        if playerid == 0:
            playerid = 1
        self.id = playerid
        grid[xin][yin] = playerid
        grid[xin][yin - 1] = playerid
        grid[xin + 1][yin] = playerid
        grid[xin + 1][yin - 1] = playerid
        players[self.id] = self
        self.jumping = 0

    def show(self):
        if self.jumping > 0:
            self.jumping -= 1
            if grid[self.x][self.y - 2] == 0 and grid[self.x + 1][self.y - 2] == 0:
                self.move(0, -1)
        elif self.y + 1 < screen.get_height():
            if grid[self.x][self.y + 1] == 0 and grid[self.x + 1][self.y + 1] == 0:
                self.move(0, 1)
        screen.fill(self.col, (self.x, self.y - 1, 2, 2))

    def move(self, xmuch, ymuch):
        grid[self.x][self.y] = 0
        grid[self.x][self.y - 1] = 0
        grid[self.x + 1][self.y] = 0
        grid[self.x + 1][self.y - 1] = 0
        self.x += xmuch
        self.y += ymuch
        grid[self.x][self.y] = self.id
        grid[self.x][self.y - 1] = self.id
        grid[self.x + 1][self.y] = self.id
        grid[self.x + 1][self.y - 1] = self.id

    def jump(self, ymuch=10):
        if self.y + 1 == screen.get_height():
            if grid[self.x][self.y - 2] == 0 and grid[self.x + 1][self.y - 2] == 0:
                self.jumping = ymuch
        elif grid[self.x][self.y + 1] != 0 or grid[self.x + 1][self.y + 1] != 0:
            if grid[self.x][self.y - 2] == 0 and grid[self.x + 1][self.y - 2] == 0:
                self.jumping = ymuch

    def side(self, xmuch):
        if xmuch < 0:
            if self.x > 0:
                if grid[self.x - 1][self.y] == 0:
                    self.move(-1, 0)
                elif not isinstance(grid[self.x - 1][self.y], Piece):
                    if players[grid[self.x - 1][self.y]].kick(-1, 0):
                        self.move(-1, 0)
                        moved = True
                elif self.y - 2 > 0:
                    if grid[self.x - 1][self.y - 1] == 0 and grid[self.x - 1][self.y - 2] == 0:
                        self.move(-1, -1)
        elif xmuch > 0:
            if self.x + 2 < screen.get_width():
                if grid[self.x + 2][self.y] == 0:
                    self.move(1, 0)
                elif not isinstance(grid[self.x + 2][self.y], Piece):
                    if players[grid[self.x + 2][self.y]].kick(1, 0):
                        self.move(1, 0)
                        moved = True
                elif self.y - 2 > 0:
                    if grid[self.x + 3][self.y - 1] == 0 and grid[self.x + 3][self.y - 2] == 0:
                        self.move(1, -1)

    def kick(self, xmuch, ymuch):
        moved = False
        if xmuch < 0:
            if self.x > 0:
                if grid[self.x - 1][self.y] == 0:
                    self.move(-1, 0)
                    moved = True
                elif not isinstance(grid[self.x - 1][self.y], Piece):
                    if players[grid[self.x - 1][self.y]].kick(-1, 0):
                        self.move(-1, 0)
                        moved = True
        elif xmuch > 0:
            if self.x + 2 < screen.get_width():
                if grid[self.x + 2][self.y] == 0:
                    self.move(1, 0)
                    moved = True
                elif not isinstance(grid[self.x + 2][self.y], Piece):
                    if players[grid[self.x + 2][self.y]].kick(1, 0):
                        self.move(1, 0)
                        moved = True
        if ymuch < 0:
            if self.y - 1 > 0:
                if grid[self.x][self.y - 2] == 0:
                    self.move(0, -1)
                    moved = True
                elif not isinstance(grid[self.x][self.y - 2], Piece):
                    if players[grid[self.x][self.y - 2]].kick(0, -1):
                        self.move(0, -1)
                        moved = True
        elif ymuch > 0:
            if self.y + 1 < screen.get_width():
                if grid[self.x][self.y + 1] == 0:
                    self.move(0, 1)
                    moved = True
                    self.jumping = 0
                elif not isinstance(grid[self.x][self.y + 1], Piece):
                    if players[grid[self.x][self.y + 1]].kick(0, 1):
                        self.move(0, 1)
                        moved = True
        return moved

    def chunk(self, structure, origx, origy, targx, targy, focin=100):
        chunk(structure, origx + self.x, origy + self.y, targx + self.x, targy + self.y, focin)

    def generate(self, structure, x, y, focin=100):
        generate(structure, x + self.x, y + self.y, focin)

    def fist(self, x, y):
        if x < -5:
            generate(leftFIST, self.x - 10 + x, self.y + y)
        elif x > 5:
            generate(rightFIST, self.x - 10 + x, self.y + y)
        else:
            generate(FIST, self.x - 10 + x, self.y + y, 150)

    def punch(self, x, y):
        if x > 0:
            chunk(rightFIST, self.x + 10, self.y - 20, self.x + x, self.y + y, abs(x + 10))
        if x < 0:
            chunk(leftFIST, self.x - 30, self.y - 20, self.x + x, self.y + y, abs(x + 10))

    def unbury(self):
        chunk(blank, self.x, self.y - 20, self.x + 10, self.y - 30)
        chunk(blank, self.x - 20, self.y - 20, self.x - 40, self.y - 30)

    def dragon(self, x, y, focin):
        if x < 0:
            generate(leftDRAGON, self.x - int(leftDRAGON.get_width()/2) + x, self.y + y, focin)
        else:
            generate(rightDRAGON, self.x - int(rightDRAGON.get_width()/2) + x, self.y + y, focin)

    def undertow(self, x):
        chunk(blank, self.x + x - 10, self.y + 1, self.x - 10, self.y + 1, 50)

    def raisin(self):
        grid[self.x][self.y + 1].settarget(self.x, self.y, 10, True)


def generate(structure, x, y, focin=100):
    targets = pygame.surfarray.array_colorkey(structure)
    used = [0 for i in range(screen.get_width())]
    for i in range(len(targets)):
        if x + i == constrain(x + i, 0, screen.get_width() - 1):
            for j in range(len(targets[i])):
                if y + j == constrain(y + j, 0, screen.get_height() - 1):
                    if targets[i][j] > 0:
                        p, q = x + i, y + j
                        no = used[p]
                        for k in range(y, screen.get_height()):
                            if isinstance(grid[p][k], Piece):
                                if no > 0:
                                    no -= 1
                                else:
                                    used[p] += 1
                                    grid[p][k].settarget(p, q, focin)
                                    break


def chunk(structure, origx, origy, targx, targy, focin=100):
    targets = pygame.surfarray.array_colorkey(structure)
    for i in range(len(targets)):
        if origx + i == constrain(origx + i, 0, screen.get_width() - 1):
            for j in range(len(targets[i])):
                if origy + j == constrain(origy + j, 0, screen.get_height() - 1):
                    if isinstance(grid[origx + i][origy + j], Piece):
                        if targets[i][j] > 0:
                            grid[origx + i][origy + j].settarget(targx + i, targy + j, focin)
                        else:
                            grid[origx + i][origy + j].focus = 0


groundx = screen.get_width()
groundy = 149
for i in range(groundx):
    for j in range(groundy, screen.get_height()):
        r = randint(100, 255)
        Piece(i, j, (r, r, 0))

P1 = Player("K", 50, 130, (0, 255, 0))
P1go = 0

w = False
a = False
s = False
d = False
q = False

while True:
    screen.fill((0, 0, 0))
    R = [r for r in range(len(pieces))]
    shuffle(R)
    for p in R:
        pieces[p].show()
    P1.side(P1go)
    for P in players.values():
        P.show()
    window.blit(pygame.transform.scale2x(screen, window), (0, 0))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            u = e.unicode
            if e.key == K_ESCAPE:
                exit()
            if e.key == K_UP:
                P1.jump()
            elif e.key == K_LEFT:
                P1go -= 1
            elif e.key == K_RIGHT:
                P1go += 1
            elif e.key == K_u:
                P1.generate(SANS, -59, -151, 300)
            elif e.key == K_y:
                P1.dragon(0, -30, 100)
            elif e.key == K_t:
                P1.fist(0, -30)
            elif u == "w":
                w = True
                if a:
                    P1.chunk(blank, -20, -10, -20, -30)
                elif d:
                    P1.chunk(blank, 2, -10, 2, -30)
                elif s:
                    P1.chunk(blank, -10, 0, -10, -22)
                elif q:
                    P1.chunk(blank, -10, -10, -10, -30)
            elif u == "a":
                a = True
                if w:
                    P1.chunk(blank, -10, -21, -25, -21)
                elif s:
                    P1.chunk(blank, -10, 0, -25, 0)
                elif d:
                    P1.chunk(blank, 2, -10, -10, -10)
                elif q:
                    P1.chunk(blank, -10, -10, -30, -10)
            elif u == "s":
                s = True
                if w:
                    P1.chunk(blank, -10, -22, -10, -10)
                elif a:
                    P1.chunk(blank, -20, -10, -20, 10)
                elif d:
                    P1.chunk(blank, 2, -10, 2, 10)
                elif q:
                    P1.chunk(blank, -10, -10, -10, 10)
            elif u == "d":
                d = True
                if w:
                    P1.chunk(blank, -10, -21, 5, -21)
                elif s:
                    P1.chunk(blank, -10, 0, 5, 0)
                elif a:
                    P1.chunk(blank, -20, -10, 5, 0)
                elif q:
                    P1.chunk(blank, -10, -10, 10, -10)
            elif u == " ":
                q = True
                if w:
                    P1.chunk(blank, -10, -21, -10, -41)
                elif a:
                    P1.chunk(blank, -20, -10, -40, -10)
                elif d:
                    P1.chunk(blank, 2, -10, 22, -10)
                elif s:
                    P1.chunk(blank, -10, 0, -10, 20)
        elif e.type == KEYUP:
            u = e.key
            if u == K_LEFT:
                P1go += 1
            elif u == K_RIGHT:
                P1go -= 1
            elif u == K_w:
                w = False
            elif u == K_a:
                a = False
            elif u == K_s:
                s = False
            elif u == K_d:
                d = False
            elif u == K_SPACE:
                q = False
        # print(w,a,s,d)
