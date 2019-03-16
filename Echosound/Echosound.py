import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()

w, h = 200, 200
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))
screencorners = np.int32([(0, 0), (0, h), (0, w), (w, h)])

keys = set()

circles = []


class EnergyCircle:
    def __init__(self, pos, energy):
        self.r = 0
        self.pos = np.float32(pos)
        self.energy = energy
        self.maxr = np.max(np.linalg.norm(self.pos - screencorners, axis=1))
        self.update()

    def update(self):
        self.r += 1
        if self.r > self.maxr:
            circles.remove(self)
        else:
            self.spreadenergy = self.energy / (self.r ** 2)
        pygame.draw.circle(screen, (int(255 + np.log(self.spreadenergy / 1000) * 10), 0, 0), np.int32(self.pos), self.r, 1)


class CircleGenerator:
    def __init__(self, pos):
        self.pos = np.float32(pos)

    def update(self, cycles):
        pygame.draw.circle(screen, (0, 255, 0), np.int32(self.pos), 3)
        if (0 <= (cycles % 100) < 30) and (cycles % 3 == 0):
            circles.append(EnergyCircle(self.pos, 1000))


class Reflector:
    def __init__(self, pos):
        self.pos = np.float32(pos)

    def update(self):
        pygame.draw.circle(screen, (0, 0, 255), np.int32(self.pos), 3)
        for C in circles:
            if C.r - 1 < np.linalg.norm(self.pos - C.pos) < C.r + 1:
                circles.append(EnergyCircle(self.pos, C.spreadenergy))


generators = [CircleGenerator((w * i/4, h/2)) for i in range(1, 4)]
R = Reflector(screensize * 0.7)

t = 0
while True:
    screen.fill(0)
    for G in generators:
        G.update(t)
    for C in circles:
        C.update()
    R.update()
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
    sleep(0.05)
    t += 1
