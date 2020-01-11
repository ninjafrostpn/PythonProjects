# Basic idea:
# Physicsy sandy sand (pixel-perfect collisions, run simulation to keep up with real time)
# Character moving around
# Tap direction (WASD) to choose stuff to pick up, tap next to throw
# Hold direction to choose stuff to morph, press other keys to morph it


import pygame
from pygame.locals import *
import numpy as np
import time

pygame.init()

coltonum = lambda r, g, b: (((r << 8) + g) << 8) + b

adjvecs = np.int32([[i, j]
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if 0 < abs(i + j) < 2])

w, h = 500, 250
screensize = np.int32((w, h))
screen = pygame.Surface(screensize)
window = pygame.display.set_mode(screensize * 2)

screengrid = pygame.surfarray.pixels3d(screen)
windowgrid = pygame.surfarray.pixels3d(window)

keys = set()
movemode = 0
enough = 100
threshold = 0

x = np.tile(np.arange(0, 100, 1, "int32"), 100)
y = np.repeat(np.arange(0, 100, 1, "int32"), 100)
m = np.random.randint(1, 3, x.shape)
vx = np.zeros(x.shape, "int32")
vy = np.ones(x.shape, "int32")
fx = np.zeros(x.shape, "int32")
fy = np.zeros(x.shape, "int32")

while True:
    screen.fill(0)
    screengrid[x, y, 0] = 255 - ((m - 1) * 10)
    for i in range(2):
        for j in range(2):
            windowgrid[i::2, j::2] = screengrid
    pygame.display.flip()
    mousepos = np.int32(pygame.mouse.get_pos())
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type == KEYUP:
            keys.discard(e.key)

    order = np.arange(0, x.shape[0])
    np.random.shuffle(order)
    order = list(order)
    while len(order) > 0:
        i = order[0]
        # print(i)
        collided = False
        for dy in range(1, vy[i] + 1):
            coll = (x[i] == x) & ((y[i] + dy) == y)
            if np.any(coll):
                # print("BUMPS", *np.argwhere(coll)[0])
                order.remove(*np.argwhere(coll)[0])
                order.insert(0, *np.argwhere(coll)[0])
                collided = True
                break
        if not collided:
            y[i] += vy[i]
            order.remove(i)
