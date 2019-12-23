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
attractorgrid = np.zeros(screensize)
screengrid = pygame.surfarray.pixels3d(screen)
windowgrid = pygame.surfarray.pixels3d(window)
# print("W", sandgrid[tuple((adjvecs + (10, 10)).T)])

sandgrid[:, -100:] = 5
sandgrid[:, :100] = 1
print(sandgrid[200, 100])


def drawin(cent, checked=None, depth=0, threshold=0, debug=False):
    if debug:
        print(depth, ": ", cent, sep="")
    if checked is None:
        checked = []
    if tuple(cent) not in checked:
        checked.append(tuple(cent))
    adj = np.int32(cent) + adjvecs
    np.random.shuffle(adj)
    adj = sorted(adj, key=lambda x: np.sum(np.abs(np.int32(x) - cent)))
    nextchecks = []
    for a in adj:
        if tuple(a) not in checked:
            checked.append(tuple(a))
            aval = sandgrid[tuple(a)]
            if ((aval > threshold)):  # and (attractorgrid[tuple(a)] == 0)) or (aval > threshold + 1):
                if debug:
                    print(depth + 0.5, ": ", a, sep="")
                return a
            elif aval > 0:
                nextchecks.append(a)
    if len(nextchecks) > 0:
        np.random.shuffle(nextchecks)
        nextchecks = sorted(nextchecks, key=lambda x: np.sum(np.abs(np.int32(x) - cent)))
        for a in nextchecks:
            b = drawin(a, checked, depth + 1, threshold, debug)
            if b is not None:
                if debug:
                    print(depth + 0.5, ": ", b, sep="")
                return b
    # TODO: Do something more useful here
    return None


keys = set()
movemode = 0
enough = 100
threshold = 0

while True:
    screen.fill(0)
    # print("WERP")
    attractors = np.argwhere(attractorgrid < 0)
    np.random.shuffle(attractors)
    nostealpls = [tuple(pos) for pos in attractors]
    for pos in attractors:
        if sandgrid[tuple(pos)] >= enough:
            continue
        # North: -1, East: -2, South: -3, West: -4
        val = attractorgrid[tuple(pos)]
        # print(pos, val)
        availablemask = (sandgrid > 0)
        availablemask &= ((attractorgrid == 0) | ((attractorgrid < 0) & (sandgrid > sandgrid[tuple(pos)])))
        if val == -1:
            check = np.argwhere(availablemask[pos[0], pos[1]-1::-1])
        if val == -2:
            check = np.argwhere(availablemask[pos[0]-1::-1, pos[1]])
        if val == -3:
            check = np.argwhere(availablemask[pos[0], pos[1]+1:])
        if val == -4:
            check = np.argwhere(availablemask[pos[0]+1:, pos[1]])
        if len(check) > 0:
            found = check[0][0] * (-1 if val in [-1, -2] else 1)
            # print(found, str(check)[:10])
            if val in [-1, -3]:
                tocell = pos + [0, found]
            else:
                tocell = pos + [found, 0]
            # print("ZHOOP", tocell)
            fromcell = drawin(tocell, threshold=threshold)
            if fromcell is not None:
                if movemode == 0:
                    sandgrid[tuple(fromcell)] -= 1
                    sandgrid[tuple(tocell)] += 1
                elif movemode == 1:
                    splitdiff = np.ceil((sandgrid[tuple(fromcell)] - sandgrid[tuple(tocell)]) / 2)
                    sandgrid[tuple(fromcell)] -= splitdiff
                    sandgrid[tuple(tocell)] += splitdiff
            nostealpls.append(tuple(tocell))
    screengrid[attractorgrid < 0, 0] = 100
    screengrid[sandgrid > 0, 1] = 100
    screengrid[sandgrid > 0, 2] = 255 - (20 * sandgrid[sandgrid > 0])
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
            if e.key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
                clickpos = tuple(np.int32(mousepos / 2))
                print(clickpos, sandgrid[clickpos])
                attractorgrid[attractorgrid < 0] = 0
                attractorgrid[clickpos[0] - 2: clickpos[0] + 3,
                clickpos[1] - 2: clickpos[1] + 3] = [-1, -3, -4, -2][e.key - 273]
                # sandgrid[clickpos] = [-1, -3, -4, -2][e.key - 273]
