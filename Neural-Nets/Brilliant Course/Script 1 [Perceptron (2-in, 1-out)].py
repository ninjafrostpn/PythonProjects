import numpy as np
import pygame
from pygame.locals import *

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

# Weights applied to x and y positions when determining activation
xweight = 0.2
yweight = 0.3
# Bias toward activation
bias = -100

# Vector of weights
weights = np.float32([bias, xweight, yweight])
# Vector of input values with 1 standing in as the "weight" of the perceptron's bias
# x and y (the 2nd and 3rd values) set to 1 to begin with
values = np.ones(3, "float32")

keys = set()

while True:
    # Randomly selected point to test boundary condition
    pos = np.random.sample(2) * screensize
    # Point put into input vector
    values[1:] = pos[:]
    # Vector dot multiplication used to determine whether perceptron activates
    # Coloured point is displayed accordingly
    if np.dot(values, weights) >= 0:
        pygame.draw.rect(screen, [0, 255, 0], (*(pos - 1), 2, 2))
    else:
        pygame.draw.rect(screen, [0, 0, 255], (*(pos - 1), 2, 2))
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
