import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()


class Predator:
    def __init__(self, homepos):
        self.homepos = np.float32(homepos)
        self.pos = self.homepos.copy()
        self.state = 0

    def show(self):
        if self.state == 0:

        pygame.draw.circle(screen, (255, 0, 0), np.int32(self.homepos), 10)
        pygame.draw.circle(screen, (0, 255, 0), np.int32(self.pos), 5)


class Prey:
    def __init__(self, homepos, population=10, spread=50, regen=500):
        self.homepos = np.float32(homepos)
        self.population = population
        self.spread = spread
        self.regen = regen
        self.counter = 0
        self.preylist = []

    def show(self):
        if len(self.preylist) < self.population:
            self.counter += 1
            if self.counter % self.regen == 0:
                self.counter = 0
                r = np.random.random() * np.pi * 2
                newpos = self.homepos + (np.float32([np.cos(r), np.sin(r)]) * self.spread * np.random.random())
                newpos = np.minimum(np.maximum(newpos, (0, 0)), screensize)
                self.preylist.append(pygame.Rect(*(newpos - (2, 2)), 4, 4))
        for R in self.preylist:
            pygame.draw.rect(screen, (0, 0, 255), R)


P = Predator((0, h/2))
Q = Prey((w * 0.75, h/2))

while True:
    screen.fill(0)
    P.show()
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
    sleep(0.001)
