import numpy as np
import pygame
from pygame.locals import *
from time import sleep

pygame.init()

w, h = 1000, 500
halfscreen = np.float32([w, h]) / 2
screen = pygame.display.set_mode((w, h))

particles = []

class Particle:
    def __init__(self, pos, fieldfunc):
        self.fieldfunc = fieldfunc
        self.pos = np.float32(pos)
        self.vel = np.float32([0, 0])
        particles.append(self)
    
    def show(self):
        acc = np.float32(self.fieldfunc(*(self.pos - halfscreen)))
        self.vel += acc
        self.pos += self.vel
        pygame.draw.circle(screen, 255, np.int32(self.pos), 2)
        pygame.draw.line(screen, 65535, np.int32(self.pos), np.int32(self.pos - acc))


def pull(x, y):
    return (y - x * 2)/1000, (-x - y * 4)/1000

for i in range(0, w + 1, 20):
    for j in range(0, h + 1, 20):
        Particle((i, j), pull)

while True:
    screen.fill(0)
    for P in particles:
        P.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    sleep(0.1)
