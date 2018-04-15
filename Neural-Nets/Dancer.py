import numpy as np
import pygame
from pygame.locals import *
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


def sigmoid(x, deriv=False):
    if not deriv:
        val = 1 / (1 + np.exp(-x))
    else:
        val = x * (1 - x)
    # print(val, deriv)
    return val


screen = pygame.display.set_mode((1000, 500))
w = screen.get_width()
h = screen.get_height()
size = (w, h)
screenrect = screen.get_rect()

white = (255, 255, 255)
turquoise = (0, 255, 255)
pink = (255, 0, 255)

recordlength = 1

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
        for i in range(recordlength):
            for j in range(len(self.pos)):
                self.posrecord.append(self.pos[j] - size[j])
    
    def move(self, keys):
        # print(keys)
        keycheck = [(key in keys) for key in self.keys]
        rightforce = keycheck[3] - keycheck[1]
        downforce = keycheck[2] - keycheck[0]
        self.kick((rightforce, downforce))
        self.kick(gravity)
        self.vel += self.acc
        self.pos += self.vel
        if self.pos[0] < 0 or self.pos[0] >= w:
            self.vel[0] = 0
        if self.pos[1] < 0 or self.pos[1] >= h:
            self.vel[1] = 0
        self.pos = np.clip(self.pos, np.zeros(2), np.array([w, h]))
        self.acc = np.zeros(2, 'float32')
        for i in range(len(self.pos)):
            self.posrecord.append(self.pos[i] - size[i])
            self.posrecord.pop(0)
        # print(self.posrecord)
        # print(keycheck)
        return np.array([self.posrecord]), np.array([keycheck])


class AIBall(PlayerBall):
    def __init__(self, pos, mass=50, col=turquoise):
        self.syn0 = 2 * np.random.random((recordlength * 2, recordlength * 4)) - 1
        self.syn1 = 2 * np.random.random((recordlength * 4, 4)) - 1
        super(AIBall, self).__init__(pos, mass=mass, col=col)
    
    def move(self, inputdata, outputdata):
        layer0 = np.float32(inputdata.copy())
        layer1 = sigmoid(np.dot(layer0, self.syn0))
        layer2 = sigmoid(np.dot(layer1, self.syn1))
        layer2error = outputdata - layer2
        layer2delta = layer2error * sigmoid(layer2, True)
        layer1error = layer2delta.dot(self.syn1.T)
        layer1delta = layer1error * sigmoid(layer1, True)
        self.syn1 += layer1.T.dot(layer2delta)
        self.syn0 += layer0.T.dot(layer1delta)

        layer0 = np.float32(self.posrecord.copy())
        layer1 = sigmoid(np.dot(layer0, self.syn0))
        layer2 = sigmoid(np.dot(layer1, self.syn1))
        activations = layer2 > 0.9
        super(AIBall, self).move(self.keys[activations])


AIs = [AIBall((w/2, h/2)) for i in range(5)]
Player = PlayerBall((w/2, h/2))
keyset = set()

while True:
    screen.fill(0)
    record = Player.move(keyset)
    for AI in AIs:
        AI.move(*record)
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
        elif e.type == KEYUP:
            keyset.remove(e.key)
    #sleep(0.01)
