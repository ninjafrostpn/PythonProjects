import csv
import numpy as np
import pygame
from pygame.locals import *

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

with open(r"Neural-Nets/Brilliant Course/flag.data") as datacsv:
    csvreader = csv.reader(datacsv)
    flagdata = np.array([row for row in csvreader])


# Weights applied to x and y positions when determining activation of r,g,b respectively
xweight = [0.1, -0.1, 0.1]
yweight = [0.3, -0.01, -0.1]
# Bias toward activation for r,g,b respectively
bias = [-75, 25, 0]

# Vector of weights
weights = np.float32([bias, xweight, yweight])
# Number of input values
N = 5000
# Vectors of input values with 1 standing in as the "weight" of the perceptron's bias
# x and y (the 2nd and 3rd values in each vector) set to 1 to begin with
values = np.ones((N, 3), "float32")

keys = set()

while True:
    # Randomly selected point to test boundary condition
    pos = np.random.sample([N, 2]) * screensize
    # Point put into input vector
    values[:, 1:] = pos[:]
    # Vector dot multiplication used to determine whether perceptron activates
    output = np.dot(values, weights)
    # Coloured point is displayed accordingly
    for i in range(N):
        pygame.draw.rect(screen,
                         (output[i] >= 0) * 255,
                         (*(pos[i] - 1), 2, 2))
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
