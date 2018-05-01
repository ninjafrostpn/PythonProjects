import numpy as np
import pygame
from pygame.locals import *
from random import shuffle
from time import sleep

pygame.init()

# Plan:
# Two balls, one controlled by player, one controlled by AI
# Player moves ball with arrow keys, and data are recorded as follows:
# - relative (x,y) position of AI ball in past n cycles up to and including present, as 2n values
# - which of four arrow keys are currently pressed
# The former 2n data points are fed to the inputs, and the latter four as outputs, for training the neural net
# (This could perhaps be done at regular intervals, if it can't be done continuously)
# The neural net is fed the relative (x,y) position of the player ball over the last n cycles
# The output of said neural net is interpreted as keypresses
# We dance!


def sigmoidsquish(x):
    return 1 / (1 + np.exp(-x))


def costfunction(predicted, actual, deriv=False):
    if deriv:
        return 2 * (predicted - actual)
    return np.sum((predicted - actual) ** 2)


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
        # print(layer)
        return layers
    
    def train(self, trainingdata):
        if len(trainingdata) > 0:
            np.random.shuffle(trainingdata)
            for training in trainingdata:
                prediction = self.use(training[0])
                # print(inputdata, "->", prediction[-1])
                # print("Should be:", outputdata)
                cost = costfunction(prediction[-1], training[1])
                nudge = -costfunction(prediction[-1], training[1], True)
                # print("How bad? {} bad.".format(cost))
                for i in range(-1, -(self.synno + 1), -1):
                    # print("Nudges required:", nudge)
                    self.synbiases[i] += nudge
                    newnudge = np.dot(self.synweights[i], nudge)
                    self.synweights[i] += (np.array([prediction[i - 1]]).T.dot(np.array([nudge])))
                    nudge = newnudge


screen = pygame.display.set_mode((1000, 500))
w = screen.get_width()
h = screen.get_height()
size = (w, h)
screenrect = screen.get_rect()

white = (255, 255, 255)
turquoise = (0, 255, 255)
pink = (255, 0, 255)

recordlength = 1
recordslength = 50

trainingdata = [[0,0,0,1],
                [0,0,1,0],
                [0,0,1,1],
                [0,1,0,0],
                [0,1,0,1],
                [0,1,1,0],
                [0,1,1,1],
                [1,0,0,0],
                [1, 0, 0, 1],
                [1, 0, 1, 0],
                [1, 0, 1, 1],
                [1, 1, 0, 0],
                [1, 1, 0, 1],
                [1, 1, 1, 0],
                [1, 1, 1, 1]]

trainingdata = [[i * recordlength, i] for i in trainingdata]

gravity = np.float32([0, 0.5])

balls = []


class Ball:
    def __init__(self, pos, mass=50, col=white):
        self.pos = np.float32(pos)
        self.vel = np.zeros(2, 'float32')
        self.acc = np.zeros(2, 'float32')
        self.inversemass = 1/mass
        self.col = col
        balls.append(self)
    
    def kick(self, force):
        self.acc += np.float32(force) * self.inversemass
    
    def show(self):
        pygame.draw.circle(screen, self.col, np.uint(self.pos), 10)


class PlayerBall(Ball):
    def __init__(self, pos, keys=(K_UP, K_LEFT, K_DOWN, K_RIGHT), mass=50, col=pink):
        self.keys = np.array(keys)
        pos = np.float32(pos)
        self.posrecord = []
        super(PlayerBall, self).__init__(pos, mass, col)
        self.posrecord += [False] * recordlength * 4
    
    def move(self, keys, opposition):
        # print(keys)
        keycheck = [(key in keys) for key in self.keys]
        rightforce = keycheck[3] - keycheck[1]
        downforce = keycheck[2] - keycheck[0]
        self.kick((rightforce, downforce))
        # self.kick(gravity)
        self.vel += self.acc
        self.pos += self.vel
        if self.pos[0] < 0 or self.pos[0] >= w:
            self.vel[0] = 0
        if self.pos[1] < 0 or self.pos[1] >= h:
            self.vel[1] = 0
        self.pos = np.clip(self.pos, np.zeros(2), np.array([w, h]))
        self.acc = np.zeros(2, 'float32')
        self.posrecord.append(opposition.pos[1] <= self.pos[1])
        self.posrecord.append(opposition.pos[0] <= self.pos[0])
        self.posrecord.append(opposition.pos[1] >= self.pos[1])
        self.posrecord.append(opposition.pos[0] >= self.pos[0])
        while len(self.posrecord) > (recordlength * 4):
            self.posrecord.pop(0)
        # print(self.posrecord)
        # print(keycheck)
        return self.posrecord, keycheck


class AIBall(PlayerBall):
    def __init__(self, pos, mass=50, col=turquoise):
        self.brain = NeuralNet(recordlength * 4,
                               recordlength * 8,
                               4)
        super(AIBall, self).__init__(pos, mass=mass, col=col)
    
    def move(self, opposition):
        activations = self.brain.use(self.posrecord)[-1] > 0.5
        # print(activations)
        return super(AIBall, self).move(self.keys[activations], opposition)


AIs = [AIBall((w/4, h/4)) for i in range(5)]
# for i in range(5000):
#     for AI in AIs:
#         AI.brain.train(trainingdata)
Player = PlayerBall((w/2, h/2))
keyset = set()
istraining = True
records = []
record = trainingdata[0]

cycles = -1
while True:
    screen.fill(0)
    cycles += 1
    Player.move(keyset, AI)
    if istraining:
        records.append(record)
    if len(records) > recordslength:
        AI.brain.train(records)
        if istraining:
            records.pop(0)
    for AI in AIs:
        if istraining:
            AI.brain.train([record])
        record = AI.move(Player)
    for B in balls:
        B.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keyset.add(e.key)
            if e.key == K_ESCAPE:
                quit()
            if e.key == K_SPACE:
                istraining = not istraining
        elif e.type == KEYUP:
            keyset.remove(e.key)
    sleep(0.01)
