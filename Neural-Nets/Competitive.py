import numpy as np
import pygame
from pygame.locals import *

w = 500
h = 500
screen = pygame.display.set_mode((w, h))

sigmoidsquish = lambda x: 1 / (1 + np.exp(-x))


class CompetitiveNet:
    def __init__(self, inputno, outputno):
        self.inputno = inputno
        self.outputno = outputno
        self.weights = np.random.random((inputno, outputno))
        self.weights /= np.sum(self.weights, axis=)
    
    def use(self, inputdata):
        return np.float32(inputdata.copy()).dot(self.weights)
    
    def train(self, inputdata, targetdata):
        outputdata = self.use(inputdata)
        
    
C = CompetitiveNet(12, 4)
print(C.use([i for i in range(12)]))

while True:
    screen.fill(0)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
