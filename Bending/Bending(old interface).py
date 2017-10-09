import pygame
from pygame.locals import *
from random import randint as rand

pygame.init()
screen = pygame.Surface((500, 100))
window = pygame.display.set_mode((screen.get_width() * 2, screen.get_height() * 2))


def constrain(val, lo, hi):
    # Because these things are useful :)
    if val <= lo:
        return lo
    elif val >= hi:
        return hi
    else:
        return val

blank = pygame.Surface((20, 20))
blank.set_colorkey((255, 255, 255))

logopath = "C:\\Users\\Charles Turvey\\PycharmProjects\\Stuff\\Simulator\\fakerobotapi\\Resources\\LogoSmall.png"
srlogo = pygame.image.load_extended(logopath)
srlogo = pygame.transform.scale(srlogo, (20, 20))
srlogo.set_colorkey((0, 0, 0))
srlogo.convert()

FIST = pygame.image.load_extended("D:\\Users\\Charles Turvey\\Documents\\Python\\FIST.png")
FIST = pygame.transform.scale(FIST, (20, 20))
FIST.set_colorkey((255, 255, 255))
FIST.convert()
rightFIST = pygame.transform.rotate(FIST, -90)
leftFIST = pygame.transform.flip(rightFIST, True, False)

leftDRAGON = pygame.image.load_extended("D:\\Users\\Charles Turvey\\Documents\\Python\\DRAGON.png")
leftDRAGON = pygame.transform.scale(leftDRAGON, (40*int(leftDRAGON.get_width()/leftDRAGON.get_height()), 40))
leftDRAGON.set_colorkey((255, 255, 255))
leftDRAGON.convert()
rightDRAGON = pygame.transform.flip(leftDRAGON, True, False)

pieces = []
grid = [[0 for j in range(screen.get_height())] for i in range(screen.get_width())]
players = dict()


class Piece:
    def __init__(self, xin, yin, col=(100, 100, 100)):
        self.x = xin
        self.y = yin
        self.col = col
        self.target = (-1, -1)
        self.focus = 0
        pieces.append(self)
        grid[xin][yin] = self

    def show(self):
        if self.focus > 0:
            self.focus -= 1
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
        elif xmuch > 0:
            if self.x + 2 < screen.get_width():
                if grid[self.x + 2][self.y] == 0:
                    self.move(1, 0)
                elif not isinstance(grid[self.x + 2][self.y], Piece):
                    if players[grid[self.x + 2][self.y]].kick(1, 0):
                        self.move(1, 0)
                        moved = True

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

    def dragon(self, x, y):
        if x < 0:
            generate(leftDRAGON, self.x - int(leftDRAGON.get_width()/2) + x, self.y + y)
        else:
            generate(rightDRAGON, self.x - int(rightDRAGON.get_width()/2) + x, self.y + y)

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


groundx = int(screen.get_width())
groundy = int(screen.get_height()/3)
for i in range(groundx):
    for j in range(groundy):
        Piece(i, (2 * groundy) + j, (0, 100, j * 7))
for i in range(100, 120):
    for j in range(0, 50):
        Piece(i, j, (255, 255, 0))

P1 = Player("George", 400, 10, (0, 255, 0))
P1go = 0
P2 = Player("Goatee", 498, 10, (200, 0, 0))

while True:
    screen.fill((0, 0, 0))
    for p in pieces:
        p.show()
    P1.side(P1go)
    if abs(P1.x - P2.x) > 10:
        P2.side(P1.x - P2.x)
        P2.jump()
    for P in players.values():
        P.show()
    window.blit(pygame.transform.scale2x(screen, window), (0, 0))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            mousepos = pygame.mouse.get_pos()
            mousex = int(mousepos[0] / 2)
            mousey = int(mousepos[1] / 2)
            if e.unicode == "w":
                # generate(rightFIST, mousex, mousey)
                P1.fist(0, -20)
            elif e.unicode == "e":
                # chunk(rightFIST, mousex, mousey, mousex + 250, mousey, 300)
                P1.fist(20, -20)
            elif e.unicode == "q":
                # chunk(leftFIST, mousex, mousey, mousex - 250, mousey, 300)
                P1.fist(-20, -20)
            elif e.unicode == "s":
                P1.unbury()
            elif e.unicode == "d":
                P1.punch(100, -20)
            elif e.unicode == "a":
                P1.punch(-100, -20)
            elif e.unicode == "z":
                P1.undertow(20)
            elif e.unicode == "c":
                P1. undertow(-20)
            elif e.unicode == "x":
                P1.raisin()
            elif e.key == K_UP:
                P1.jump()
            elif e.key == K_LEFT:
                P1go -= 1
            elif e.key == K_RIGHT:
                P1go += 1
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                P1go += 1
            elif e.key == K_RIGHT:
                P1go -= 1
