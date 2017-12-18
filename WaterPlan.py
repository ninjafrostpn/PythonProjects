import pygame, math
from pygame.locals import *

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

particles = []
particlemap = [[[] for j in range(h)] for i in range(w)]
heightmap = [[0 for j in range(h)] for i in range(w)]

class particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        particles.append(self)
        particlemap[int(x)][int(y)].append(self)
        heightmap[int(x)][int(y)] += 1
    
    def kick(self, mag, ang):
        newx = self.x + (mag * math.cos(ang))
        newy =
        particlemap[]

while True:
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()