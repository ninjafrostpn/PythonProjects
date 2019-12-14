# Basic idea:
# Character moving around
# Display follows, pointing in a direction from a point near them
# Can draw out the environment sitting in the direction of the arrow toward the point
# Environment made up of pixel values representing the density of the material found there
# Lowest density is 1, 0 indicates absence of material
# (possibly negative numbers for places the environment is drawn to; might help calculation)
# Higher-density pixels can be drawn out into several lower ones

import pygame
from pygame.locals import *
import numpy as np
from time import sleep

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

sandgrid = np.zeros(screensize)
screengrid = pygame.surfarray.pixels3d(screen)
windowgrid = pygame.surfarray.pixels3d(window)
# print("W", sandgrid[tuple((adjvecs + (10, 10)).T)])

sandgrid[:, -100:] = 5
sandgrid[200, 100] = -3
print(sandgrid[200, 100])


def drawin(cent, checked=None, depth=0, debug=False):
    if debug:
        print(depth, ": ", cent, sep="")
    if checked is None:
        checked = []
    if tuple(cent) not in checked:
        checked.append(tuple(cent))
    adj = np.int32(cent) + adjvecs
    np.random.shuffle(adj)
    nextchecks = []
    for a in adj:
        if tuple(a) not in checked:
            checked.append(tuple(a))
            aval = sandgrid[tuple(a)]
            if aval > 1:
                if debug:
                    print(depth + 0.5, ": ", a, sep="")
                return a
            elif aval > 0:
                nextchecks.append(a)
    if len(nextchecks) > 0:
        np.random.shuffle(nextchecks)
        for a in nextchecks:
            b = drawin(a, checked, depth + 1, debug)
            if b is not None:
                if debug:
                    print(depth + 0.5, ": ", b, sep="")
                return b
    return None


keys = set()

while True:
    screen.fill(0)
    for pos in np.argwhere(sandgrid < 0):
        # North: -1, East: -2, South: -3, West: -4
        val = sandgrid[tuple(pos)]
        # print(pos, val)
        # if val == -1:
        #     check = np.argwhere(sandgrid[pos[0], pos[1]-1::-1] > 0)
        # if val == -2:
        #     check = np.argwhere(sandgrid[pos[0]+1:, pos[1]] > 0)
        if val == -3:
            check = np.argwhere(sandgrid[pos[0], pos[1]+1:] > 0)
        # if val == -4:
        #     check = np.argwhere(sandgrid[pos[0]-1::-1, pos[1]] > 0)
        if len(check) > 0:
            found = check[0]
            if val == -3:
                tocell = pos + [0, found]
            if np.any(tocell != pos):
                fromcell = drawin(tocell)
                if fromcell is not None:
                    sandgrid[tuple(fromcell)] -= 1
                    sandgrid[tuple(tocell)] += 1
    screengrid[sandgrid > 0, 2] = 255 - (20 * sandgrid[sandgrid > 0])
    screengrid[sandgrid < 0, :] = 255
    # pygame.transform.scale2x(screen, window)
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
        elif e.type == MOUSEBUTTONDOWN:
            clickpos = tuple(np.int32(mousepos / 2))
            print(clickpos, sandgrid[clickpos])
            if sandgrid[clickpos] == 0:
                sandgrid[sandgrid < 0] = 0
                sandgrid[clickpos] = -3
    sleep(0.1)
