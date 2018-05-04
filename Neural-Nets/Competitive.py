import numpy as np
import pygame
from pygame.locals import *

w = 500
h = 500
screen = pygame.display.set_mode((w, h))


sigmoidsquish = lambda x: 1 / (1 + np.exp(-x))


class NeuralNet:
    def __init__(self, *sizes):
        self.sizes = sizes
        self.synno = len(sizes) - 1
        self.synweights = []
        self.synbiases = []
        for i in range(self.synno):
            self.synweights.append(2 * np.random.random((sizes[i], sizes[i + 1])) - 1)
            self.synbiases.append(2 * np.random.random(sizes[i + 1]) - 1)
    
    def use(self, inputdata):
        layer = np.array(inputdata.copy())
        layers = [layer]
        for i in range(self.synno):
            layer = sigmoidsquish(layer.dot(self.synweights[i]) + self.synbiases[i])
            layers.append(layer)
        return layers
    
    def train(self, trainingdata):
        if len(trainingdata) > 0:
            np.random.shuffle(trainingdata)
            for training in trainingdata:
                prediction = self.use(training[0])
                cost = costfunction(prediction[-1], training[1])
                nudge = -costfunction(prediction[-1], training[1], True)
                for i in range(-1, -(self.synno + 1), -1):
                    self.synbiases[i] += nudge
                    newnudge = np.dot(self.synweights[i], nudge)
                    self.synweights[i] += (np.array([prediction[i - 1]]).T.dot(np.array([nudge])))
                    nudge = newnudge

while True:
    screen.fill(0)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
