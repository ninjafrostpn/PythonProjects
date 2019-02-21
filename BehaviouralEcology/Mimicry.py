import pygame
from pygame.locals import *
import numpy as np
from math import pi, sin, cos
from time import sleep

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()

COL_WHITE = (255, 255, 255)
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_CYAN = (0, 255, 255)
COL_MAGENTA = (255, 0, 255)
COL_ORANGE = (255, 200, 0)


def drawspinner(pos, rad, ang):
    pygame.draw.circle(screen, COL_ORANGE, np.int32(pos), rad)
    hexcoords = np.float32([(sin((i - ang) * pi/180),
                             cos((i - ang) * pi/180)) for i in range(0, 361, ang)]) * rad * -2
    for i in hexcoords:
        pygame.draw.line(screen, COL_MAGENTA, pos - i, pos + i, 5)


a = 1000
while True:
    screen.fill(0)
    drawspinner((w/2, h/2), 10, a)
    a -= 1
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
