import cv2
import glob
import numpy as np
import pygame
from pygame.locals import *
import random

combinations = [np.int32(cv2.imread(file)/255).flatten() for file in glob.glob("Neural-Nets/Train*.png")]
for a in range(len(combinations)):
    for b in range(a + 1, len(combinations)):
        combinations.append(combinations[a] + combinations[b])
print(*combinations, sep="\n")

w = 500
h = 500
screen = pygame.display.set_mode((w, h))

sigmoidsquish = lambda x: 1 / (1 + np.exp(-x))


class CompetitiveNet:
    def __init__(self, inputno, outputno):
        self.inputno = inputno
        self.outputno = outputno
        self.weights = np.random.random((inputno, outputno))
        for i in range(outputno):
            self.weights[:, i] /= np.sum(self.weights[:, i])
        self.weights *= 1000
        self.weights = np.int32(self.weights)
    
    def __str__(self):
        return str(self.weights)
    
    def use(self, inputdata):
        outputdata = (np.float32(inputdata) - 0.5).dot(self.weights/1000)
        return outputdata, np.argmax(outputdata)
    
    def train(self, inputdata):
        outputdata, winner = self.use(inputdata)
        # print(inputdata, outputdata, winner)
        for i in range(self.weights.shape[0]):
            if inputdata[i]:
                for j in range(self.weights.shape[1]):
                    if j != winner:
                        change = np.int32(self.weights[i, j] / 5)
                        self.weights[i, j] -= change
                        self.weights[i, winner] += change
        # print(self.use(inputdata))
        
    
for a in range(10):
    C = CompetitiveNet(len(combinations[0]), len(combinations))
    # print(C)
    for k in range(100):
        random.shuffle(combinations)
        for combination in combinations:
            C.train(combination)
    for i, combination in enumerate(combinations):
        print(i, *C.use(combination))
    r = np.random.random_integers(0, 1, len(combinations[0]))
    cv2.imshow(str(a), r.reshape((5, 5, 3)))
    print(r)
    print(*C.use(r))

while False:
    screen.fill(0)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
