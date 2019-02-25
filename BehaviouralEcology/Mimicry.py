import pygame
from pygame.locals import *
import numpy as np
from math import pi, sin, cos
from time import sleep

pygame.init()

w, h = 1000, 500
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
        if not self.edible:
            pygame.draw.circle(screen, 0, np.int32(self.pos), 2)


class Predator:
    def __init__(self, pos, vel):
        self.pos = np.float32(pos)
        self.vel = np.float32(vel)
        self.randacc = np.float32([0, 0])
        self.badmemories = []
        self.goodmemories = []
        self.timer = -10

    def update(self):
        chasing = False
        eaten = False
        for P in prey:
            diffvec = np.float32(self.pos - P.pos)
            diff = np.linalg.norm(diffvec)
            if len(self.goodmemories) == 0:
                pros = 0
            else:
                pros = sum(np.max(np.abs(np.int32(self.goodmemories) - P.col), axis=1) < 50)
            if len(self.badmemories) == 0:
                cons = 0
            else:
                cons = sum(np.max(np.abs(np.int32(self.badmemories) - P.col), axis=1) < 50)
            bias = pros - cons + 2
            if 0 < diff < 100:
                # print(P.col, bias, pros, cons)
                self.vel -= (diffvec / (diff ** 2)) * (min(max(bias, -2), 2) / 2)
                chasing = True
            if np.random.random() > 0.5 - (min(max(bias, -4), 4) / 10) and not eaten:
                if diff < 15:
                    if P.edible:
                        self.goodmemories.append(P.col)
                    else:
                        self.badmemories.append(P.col)
                    prey.remove(P)
                    eaten = True
        self.randacc += np.random.randint(-1, 2, 2)
        self.randacc = np.minimum(np.maximum(self.randacc, -1), 1)
        self.vel += self.randacc / 10
        self.pos += self.vel
        if self.pos[0] < 0 or self.pos[0] >= w:
            self.pos[0] = np.minimum(np.maximum(self.pos[0], 0), w)
            self.vel[0] *= -0.5
        if self.pos[1] < 0 or self.pos[1] >= h:
            self.pos[1] = np.minimum(np.maximum(self.pos[1], 0), h)
            self.vel[1] *= -0.5
        self.vel *= 0.995
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                predators.remove(self)
        else:
            self.timer += 1
            if self.timer == 0:
                self.timer = 7500

    def show(self):
        if self.timer > 0:
            pygame.draw.circle(screen, COL_RED, np.int32(self.pos), min(10, self.timer))
        elif self.timer < 0:
            pygame.draw.circle(screen, COL_RED, np.int32(self.pos), max(11 + self.timer, 1))


prey = [Prey(np.random.random_sample(2) * screensize, (0, 0), True, COL_RED) for i in range(20)]
prey += [Prey(np.random.random_sample(2) * screensize, (0, 0), False, COL_GREEN) for i in range(20)]
prey += [Prey(np.random.random_sample(2) * screensize, (0, 0), True, COL_GREEN) for i in range(10)]
predators = [Predator(np.random.randint(0, w, 2), (0, 0))]

cycles = 0
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
    cycles += 1
    if cycles % 2500 == 0:
        predators.append(Predator(np.random.randint(0, w, 2), (0, 1)))
        for i in range(0, len(prey), 2):
            P = prey[i]
            prey.append(Prey(P.pos.copy(), -P.vel.copy() + np.random.randint(-5, 5, 2), P.edible, P.col))
