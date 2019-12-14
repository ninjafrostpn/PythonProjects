import numpy as np
import pygame
from pygame.locals import *
from time import sleep

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
axes = screen.copy()
screensize = np.int32((w, h))
span = w * h

weights = (np.random.sample(3) - 0.5) * (100, 1, 1)
N = 5
input_given = np.ones((N, 3), "float32")
input_given[:, 1:] = (np.random.sample((N, 2)) - 0.5) * screensize
output_given = np.ones(N, "float32")
output_given[::2] *= -1
print(output_given)

stepsize = (1, 0.1, 0.1)
hingewidth = 1

keys = set()

i = 0
satisfied = True
modifications = 0
pygame.draw.line(axes, [255, 255, 255], (0, h/2), (w, h/2))
pygame.draw.line(axes, [255, 255, 255], (w/2, 0), (w/2, h))
while True:
    if i > -1:
        pos = input_given[i, :]
        loss = max(0, hingewidth - (output_given[i] * np.dot(weights, pos)))
        output_obtained = [-1, 1][int(loss == 0)]
        if output_obtained * output_given[i] == -1:
            weights += output_given[i] * pos * stepsize
            pygame.draw.rect(axes, [255, 0, 0], (*(pos[1:] - 1 + screensize/2), 2, 2))
            satisfied = False
            modifications += 1
        else:
            pygame.draw.rect(axes, [0, 255, 0], (*(pos[1:] - 1 + screensize/2), 2, 2))
        if output_given[i] == -1:
            pygame.draw.rect(axes, [255, 0, 255], (*(pos[1:] - 5 + screensize/2), 10, 10), 1)
        else:
            pygame.draw.circle(axes, [255, 0, 255], np.int32(pos[1:] + screensize/2), 5, 1)
        screen.blit(axes, (0, 0))
        norm = np.linalg.norm(weights[1:])
        normdir = weights[1:] / norm
        perpdir = normdir[::-1] * (1, -1)
        cent = screensize/2 + normdir * (-weights[0] / norm)
        pygame.draw.circle(screen, [0, 255, 255],
                           np.int32(cent), 10, 1)
        pygame.draw.polygon(screen, [0, 255, 255],
                            np.float32([perpdir, perpdir - normdir, -perpdir - normdir, -perpdir]) * 10 + cent)
        pygame.draw.line(screen, [255, 255, 0],
                         cent + span * perpdir + (hingewidth/norm) * normdir,
                         cent - span * perpdir + (hingewidth/norm) * normdir)
        pygame.draw.line(screen, [255, 255, 0],
                         cent + span * perpdir - hingewidth * normdir/norm,
                         cent - span * perpdir - hingewidth * normdir/norm)
        i += 1
        if i == N:
            if satisfied:
                print("DONE after {} modifications: (b, w_x, w_y) = ({}, {}, {})".format(modifications, *weights))
                i = -1
            else:
                i = 0
                satisfied = True
                pygame.draw.circle(screen, [255, 255, 255], np.int32(pos[1:] + screensize / 2), 8, 1)
        else:
            pygame.draw.circle(screen, [255, 255, 255], np.int32(pos[1:] + screensize / 2), 8, 1)
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
            if e.key == K_SPACE:
                weights = (np.random.sample(3) - 0.5) * (100, 1, 1)
                input_given[:, 1:] = (np.random.sample((N, 2)) - 0.5) * screensize
                output_given = np.random.choice([-1, 1], N)
                axes.fill(0)
                pygame.draw.line(axes, [255, 255, 255], (0, h / 2), (w, h / 2))
                pygame.draw.line(axes, [255, 255, 255], (w / 2, 0), (w / 2, h))
                i = 0
                satisfied = True
                modifications = 0
