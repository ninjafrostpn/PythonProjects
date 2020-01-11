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

nx = 10
pos = np.int32([[*np.tile(np.arange(0, nx, 1, "int32"), 50), *np.tile(np.arange(300 - nx, 300, 1, "int32"), 50)],
                [*np.repeat(np.arange(0, 50, 1, "int32"), nx), *np.repeat(np.arange(0, 50, 1, "int32"), nx)]]).T
mass = np.ones(pos.shape[0], "int32")
vel = np.zeros(pos.shape, "int32")
vel[:pos.shape[0] // 2] = 20
mass[pos.shape[0] // 2:] = 10
force = np.zeros(pos.shape, "int32")

while True:
    screen.fill(0)
    screengrid[pos[:, 0], pos[:, 1], 0] = 255 - ((mass - 1) * 10)
    # try:
    #     screengrid[collpos[:, 0], collpos[:, 1], 1] = 255
    # except NameError:
    #     pass
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
    # time.sleep(mousepos[0] / (10 * w))

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
    uniquev = np.unique(np.abs(vel))
    tickdiv = np.max(uniquev)
    # print(uniquev, tickdiv)
    # https://stackoverflow.com/a/42472824
    for v in uniquev[(tickdiv % uniquev) != 0]:
        # print(v, tickdiv, np.gcd(tickdiv, v))
        tickdiv = int(tickdiv * v / np.gcd(tickdiv, v))
    # print("F", tickdiv)
    i = 1
    while i < tickdiv:
        movers = ((tickdiv / i) % np.abs(vel)) == 0
        # print(i, tickdiv, vel[movers])
        pos[movers] += np.sign(vel[movers])
        vel[((pos == 0) & (vel < 0)) | ((pos == (w, h)) & (vel > 0))] *= -1
        pos = np.minimum(np.maximum(0, pos), (w - 1, h - 1))
        # https://stackoverflow.com/q/11528078
        a = np.lexsort([*pos.T])
        coll = np.all(pos[a[:-1]] == pos[a[1:]], axis=1)
        # print(sum(coll))
        if np.any(coll):
            collpos = pos[a[:-1][coll]]
            # print(pos[a[0]], pos[a[-1]])
            # Assume that there are only 2 parties to each collision, and that all masses are equal...
            oppcoll = (vel[a[:-1][coll]] * vel[a[1:][coll]]) < 0
            # print(sum(oppcoll))
            newvel = vel.copy()
            # print(vel.shape, a.shape, oppcoll.shape)
            newvel[a[:-1][coll][oppcoll[:, 0]], 0] = vel[a[1:][coll][oppcoll[:, 0]], 0]
            newvel[a[:-1][coll][oppcoll[:, 1]], 1] = vel[a[1:][coll][oppcoll[:, 1]], 1]
            newvel[a[1:][coll][oppcoll[:, 0]], 0] = vel[a[:-1][coll][oppcoll[:, 0]], 0]
            newvel[a[1:][coll][oppcoll[:, 1]], 1] = vel[a[:-1][coll][oppcoll[:, 1]], 1]

            newvel[a[:-1][coll][~oppcoll[:, 0]], 0] = vel[a[1:][coll][~oppcoll[:, 0]], 0]
            newvel[a[:-1][coll][~oppcoll[:, 1]], 1] = vel[a[1:][coll][~oppcoll[:, 1]], 1]
            newvel[a[1:][coll][~oppcoll[:, 0]], 0] = vel[a[:-1][coll][~oppcoll[:, 0]], 0]
            newvel[a[1:][coll][~oppcoll[:, 1]], 1] = vel[a[:-1][coll][~oppcoll[:, 1]], 1]
            # print(time.time(), np.all(newvel == vel), newvel is vel)
            vel[:, :] = newvel[:, :]
            if not np.all((tickdiv % vel) == 0):
                p = i / tickdiv
                uniquev = np.unique(np.abs(vel))
                for v in uniquev[(tickdiv % uniquev) != 0]:
                    tickdiv = int(tickdiv * v / np.gcd(tickdiv, v))
                # print(tickdiv)
                i = np.floor(p * tickdiv)
        i += 1
    # vel -= np.int32(np.ceil(vel / 100))
