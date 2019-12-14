import pygame
from pygame.locals import *
import numpy as np
from time import sleep, time

pygame.init()

manualmode = False
Kp = 0.5
Ki = 0
Kd = 0.05

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))
font = pygame.font.Font(None, 40)


class


keys = set()

while True:
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
