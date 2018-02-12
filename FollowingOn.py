from math import sqrt
from time import sleep
import pygame
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

colours = [(255, 255, 255), (0, 100, 50), (100, 0, 50),
                            (0, 200, 100), (200, 0, 100)]

blocks = []
playerturn = 0
totalturns = 0
takenspace = []


def dist(x1, y1, x2, y2):
    return sqrt(((x1 - x2)**2) + ((y1 - y2)**2))


class InvalidOperation(Exception):
    pass


class InvalidIndex(Exception):
    pass


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return dist(0, 0, self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (type(3), type(0.3))):
            return Vector(self.x * other, self.y * other)
        elif isinstance(other, type(Vector(0, 0))):
            return (self.x * other.x) + (self.y * other.y)
        else:
            raise InvalidOperation

    def __truediv__(self, other):
        if isinstance(other, (type(3), type(0.3))):
            return Vector(self.x / other, self.y / other)
        else:
            raise InvalidOperation

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise InvalidIndex

    def __iter__(self):
        yield int(self.x)
        yield int(self.y)
    
    def __str__(self):
        return "Vector({}, {})".format(self.x, self.y)

    def norm(self):
        if abs(self) == 0:
            return Vector(0, 0)
        else:
            return self / abs(self)


instructiondex = {K_w: Vector(0, -100),
                  K_a: Vector(-100, 0),
                  K_s: Vector(0, 100),
                  K_d: Vector(100, 0)}


class Block:
    def __init__(self, pos, leader=-1, cursor=0):
        # Vectors, pls
        self.pos = pos
        self.targ = pos
        if leader == -1:
            self.isleader = True
            self.instructions = []
        else:
            self.isleader = False
            self.instructions = leader.instructions
        self.cursor = cursor
        self.moved = False
        self.crashed = False
        self.followers = []
        self.id = len(blocks)
        blocks.append(self)
        takenspace.append(tuple(self.pos))
        
    def show(self, turn):
        #print(self.id, turn)
        turnfinished = 0
        if turn == self.id:
            if self.targ == self.pos:
                if not self.moved:
                    if self.cursor < len(self.instructions):
                        self.targ = self.pos + instructiondex[self.instructions[self.cursor]]
                        outside = self.targ.x >= w or self.targ.x < 0 or self.targ.y >= h or self.targ.y < 0
                        if tuple(self.targ) in takenspace or outside:
                            self.targ = self.pos
                            self.crashed =
                        else:
                            takenspace.remove(tuple(self.pos))
                            takenspace.append(tuple(self.targ))
                        self.moved = True
                    elif not self.isleader:
                        self.moved = True
                else:
                    turnfinished = 1
                    self.cursor += 1
                    self.moved = False
            else:
                diff = (self.targ - self.pos).norm()
                if abs(diff) < 0.1:
                    self.pos = self.targ
                else:
                    self.pos += diff
        screen.fill(colours[0], (self.pos.x + 5, self.pos.y + 5, 90, 90))
        pygame.draw.circle(screen, colours[1 + self.isleader + (self.crashed * 2)],
                           (int(self.pos.x) + 50, int(self.pos.y) + 50),
                           30)
        for b in self.followers:
            turnfinished += b.show(turn)
        return turnfinished

firstblock = Block(Vector(0, 0))
addedblock = True

while True:
    screen.fill(0)
    #print(playerturn)
    turninc = firstblock.show(playerturn)
    print(turninc)
    totalturns += turninc * (playerturn == 0)
    playerturn = (playerturn + turninc) % len(blocks)
    if totalturns % 10 == 0:
        if not addedblock:
            firstblock.followers.append(Block(Vector(0, 0), firstblock))
            addedblock = True
    else:
        addedblock = False
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
            elif e.key in list(instructiondex.keys()):
                firstblock.instructions.append(e.key)
            elif e.key == K_SPACE:
                firstblock.followers.append(Block(Vector(0, 0), firstblock))
