import numpy as np
import pygame
from pygame.locals import *
import random
from time import sleep

pygame.init()

w, h = 500, 500
screensize = np.int32([w, h])
screen = pygame.display.set_mode(screensize)

particleno = 100
particles = []
particlepos = np.zeros((particleno, 2), dtype='float32')
particleradius = np.zeros(particleno, dtype='int32')


class Particle:
    def __init__(self, pos, radius=-1):
        self.pos = np.float32(pos)
        if radius <= 0:
            self.r = int(random.random() * 10)
        else:
            self.r = int(radius)
        self.id = len(particles)
        particlepos[self.id, :] = self.pos[:]
        particleradius[self.id] = self.r
        particles.append(self)
    
    def collide(self):
        pygame.draw.circle(screen, 255, self.pos, self.r)
        dists = np.linalg.norm(particlepos - self.pos, axis=1) - (particleradius + self.r)
        collisions = dists < 0
        if np.sum(collisions) > 1:
            print(np.sum(collisions))
            diffs = particlepos[collisions] - self.pos
            angs = np.arctan2(diffs[:, 1], diffs[:, 0])
            units = np.float32([np.cos(angs), np.sin(angs)]).reshape(-1, 2)
            print(diffs.shape, angs.shape, units.shape, dists[collisions].shape)
            self.pos -= np.sum(dists[collisions] * units[:], axis=1)


for i in range(particleno):
    Particle((random.randrange(0, w), random.randrange(0, h)), 10)

while True:
    screen.fill(0)
    random.shuffle(particles)
    for P in particles:
        P.collide()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            quit()
    sleep(0.5)
