import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()

w, h = 500, 600
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

border = 60
edge = w - (border * 2)
edgevecs = np.float32([(1, 0),
                       (-np.cos(np.pi / 3), -np.sin(np.pi / 3)),
                       (np.cos(np.pi * (2 / 3)), np.sin(np.pi * (2 / 3)))])
trianglepts = border + np.int32([(0, 0),
                                 edge * -edgevecs[1],
                                (edge, 0)])
edgecols = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

keys = set()

while True:
    screen.fill(0)
    pygame.draw.line(screen, (255, 0, 255), (0, border), (w, border))
    pygame.draw.line(screen, (255, 0, 255), (0, trianglepts[1, 1]), (w, trianglepts[1, 1]))
    pygame.draw.polygon(screen, (255, 255, 255), trianglepts, 2)
    mousepos = np.int32(pygame.mouse.get_pos())
    edgedist = []
    perpdist = []
    edgepos = []
    for i in range(3):
        edgedist.append(np.dot(mousepos - trianglepts[i], edgevecs[i]))
        edgepos.append(trianglepts[i] + (edgedist[-1] * edgevecs[i]))
        perpdist.append(np.linalg.norm(mousepos - edgepos[-1]))
        pygame.draw.line(screen, edgecols[i], mousepos, edgepos[-1])
        pygame.draw.line(screen, (255, 255, 255), trianglepts[i], edgepos[-1])
    for i in range(3):
        pygame.draw.line(screen, edgecols[i],
                         (border / 2, border + sum(perpdist[:i])),
                         (border / 2, border + sum(perpdist[:i + 1])),
                         2)
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
