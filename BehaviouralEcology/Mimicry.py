import pygame
from pygame.locals import *
import numpy as np
from math import pi, sin, cos
from time import sleep

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()

COL_WHITE = (255, 255, 255)
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_CYAN = (0, 255, 255)
COL_MAGENTA = (255, 0, 255)
COL_ORANGE = (255, 200, 0)


def drawspinner(pos, rad, ang):
    pygame.draw.circle(screen, COL_ORANGE, np.int32(pos), rad)
    hexcoords = np.float32([(sin((i - ang) * pi/180),
                             cos((i - ang) * pi/180)) for i in range(0, 361, ang)]) * rad * -2
    for i in hexcoords:
        pygame.draw.line(screen, COL_MAGENTA, pos - i, pos + i, 5)


class Prey:
    def __init__(self, pos, vel, edible, col):
        self.pos = np.float32(pos)
        self.vel = np.float32(vel)
        self.edible = edible
        self.col = col

    def update(self):
        chased = False
        for P in predators:
            diffvec = np.float32(self.pos - P.pos)
            diff = np.linalg.norm(diffvec)
            if 0 < diff < 40:
                self.vel += diffvec / (diff * 5)
                chased = True
        if not chased:
            self.vel += np.random.randint(-1, 2, 2) / 10
        self.pos += self.vel
        if self.pos[0] < 0 or self.pos[0] >= w:
            self.pos[0] = np.minimum(np.maximum(self.pos[0], 0), w)
            self.vel[0] *= -1
        if self.pos[1] < 0 or self.pos[1] >= h:
            self.pos[1] = np.minimum(np.maximum(self.pos[1], 0), h)
            self.vel[1] *= -1
        self.vel *= 0.9

    def show(self):
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 5)


class Predator:
    def __init__(self, pos, vel):
        self.pos = np.float32(pos)
        self.vel = np.float32(vel)
        self.badmemories = []
        self.goodmemories = []
        self.timer = 100

    def update(self):
        chasing = False
        for P in prey:
            diffvec = np.float32(self.pos - P.pos)
            diff = np.linalg.norm(diffvec)
            if 0 < diff < 50:
                self.vel -= diffvec / (diff ** 2)
                chasing = True
            if diff < 15:
                if P.edible:
                    self.goodmemories.append(P.col)
                else:
                    self.badmemories.append(P.col)
                prey.remove(P)
        if not chasing:
            self.vel += np.random.randint(-1, 2, 2) / 10
        self.pos += self.vel
        if self.pos[0] < 0 or self.pos[0] >= w:
            self.pos[0] = np.minimum(np.maximum(self.pos[0], 0), w)
            self.vel[0] *= -1
        if self.pos[1] < 0 or self.pos[1] >= h:
            self.pos[1] = np.minimum(np.maximum(self.pos[1], 0), h)
            self.vel[1] *= -1
        self.vel *= 0.995
        self.timer -= 1
        print(self.timer)
        if self.timer == 0:
            predators.remove(self)

    def show(self):
        pygame.draw.circle(screen, COL_RED, np.int32(self.pos), min(10, self.timer))


prey = [Prey(np.random.randint(0, w, 2), (1, 0), True, COL_WHITE) for i in range(20)]
predators = [Predator(np.random.randint(0, w, 2), (0, 1)) for i in range(5)]

while True:
    screen.fill(0)
    for Q in prey + predators:
        Q.update()
        Q.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type == KEYUP:
            keys.discard(e.key)
    sleep(0.01)
