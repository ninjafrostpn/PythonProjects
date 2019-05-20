import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()

# The Idea
# String attached at ends, has tension
# Can be attached to any object
# Can be attached to pulley, via which it can be attached to other strings, which count as the same one
# Can be attached to free-moving objects
# Can be attached to fixed points

gravity = np.float32([0, 1])
airresist = 0.99
ropes = []
masses = []


class Rope:
    def __init__(self, end1, end2):
        self.end1 = end1
        self.end2 = end2
        self.k = 0.1  # Universal atm
        self.length = np.linalg.norm(self.end1.pos - self.end2.pos)
        ropes.append(self)

    def update(self):
        d = self.end2.pos - self.end1.pos
        dmag = np.linalg.norm(d)
        x = dmag - self.length
        # Springy when pulled, slack when released
        if x > 0:
            F = d * self.k * x / dmag
            self.end1.acc += F * self.end1.invmass
            self.end2.acc -= F * self.end2.invmass

    def show(self):
        pygame.draw.line(screen, (255, 0, 255), self.end1.pos, self.end2.pos)


class Mass:
    def __init__(self, mass, pos):
        self.mass = float(mass)
        if self.mass != 0:
            self.invmass = 1 / self.mass
        else:
            self.invmass = 0
        self.pos = np.float32(pos)
        self.vel = np.float32([0, 0])
        self.acc = np.float32([0, 0])
        masses.append(self)

    def update(self):
        if self.mass != 0:
            self.acc += gravity * self.mass
            self.vel += self.acc
            self.pos += self.vel
            self.acc[:] = 0
            self.vel *= airresist

    def show(self):
        pygame.draw.circle(screen, (255, 255, 0), self.pos, 10)


w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()

scenario = 0

if scenario == 0:
    A = Mass(0, [w/2, 0])
    B = Mass(1, [w/4, h/4])
    C = Mass(2, [w/2, h/2])
    D = Mass(0, [0, 0])
    E = Mass(0, [w, 0])
    F = Mass(1.5, [w/3, h/2])
    AB = Rope(A, B)
    BC = Rope(B, C)
    CD = Rope(C, D)
    CE = Rope(C, E)
    BF = Rope(B, F)
elif scenario == 1:
    pass

while True:
    screen.fill(0)
    for R in ropes:
        R.update()
        R.show()
    for M in masses:
        M.update()
        M.show()
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
