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

pos = np.int32([np.tile(np.arange(0, 100, 1, "int32"), 100), np.repeat(np.arange(0, 100, 1, "int32"), 100)]).T
mass = np.random.randint(1, 4, pos.shape[0])
vel = np.random.randint(-5, 5, pos.shape, "int32")
force = np.zeros(pos.shape, "int32")

while True:
    screen.fill(0)
    screengrid[pos[:, 0], pos[:, 1], 0] = 255 - ((mass - 1) * 10)
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

    # In order to physics in discrete space, subdivide each tick according to lcm of integer speeds of objects
    #   Each object moves only in steps of 1 in x or y
    #   At the beginning of the appropriate subdivision of a tick, an object will move 1
    #   If, say, there are objects a and b moving at x speeds 2 and 3 (units per tick), the tick will be cut into 6:
    #       0: a  b      (this is the initial state)
    #       1: a  b
    #       2: a   b
    #       3:  a  b
    #       4:  a   b
    #       5:  a   b
    #       6:   a   b   (this is the state after the tick has passed)
    #   At each stage, collisions are checked and speeds altered, etc
    #       Which will... probably get complicated fast
    #           Each object will have to keep track of the subtick offset for its movement speed (last collision)
    #           The velocity composition (and hence lcm) may change with collisions
    #       Packed, resting objects will collide... a lot, which could be slow
    #           Maybe keep track of columns/rows locked against the sides?
    uniquev = np.unique(vel)
    tickdiv = np.max(uniquev)
    print(uniquev, tickdiv)
    # https://stackoverflow.com/a/42472824
    for v in uniquev[(tickdiv % uniquev) != 0]:
        print(v, tickdiv, np.gcd(tickdiv, v))
        tickdiv = int(tickdiv * v / np.gcd(tickdiv, v))
    print("F", tickdiv)
    for i in range(1, tickdiv + 1):
        movers = ((tickdiv / i) % np.abs(vel)) == 0
        # print(i, tickdiv, vel[movers])
        pos[movers] += np.sign(vel[movers])
        pos = np.minimum(np.maximum(0, pos), (w - 1, h - 1))
