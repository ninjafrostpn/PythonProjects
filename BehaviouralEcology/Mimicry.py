import pygame
from pygame.locals import *
import numpy as np
from math import pi, sin, cos
from time import sleep

pygame.init()

w, h = 1000, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()

COL_WHITE = (255, 255, 255)
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_CYAN = (0, 255, 255)
COL_MAGENTA = (255, 0, 255)
COL_ORANGE = (255, 200, 0)


def drawspinner(pos, rad, ang):
    pygame.draw.circle(screen, COL_ORANGE, np.int32(pos), rad)
    hexcoords = np.float32([(sin((i - ang) * pi/180),
                             cos((i - ang) * pi/180)) for i in range(0, 361, ang)]) * rad * -2
    for i in hexcoords:
        pygame.draw.line(screen, COL_MAGENTA, pos - i, pos + i, 5)


class AllPrey:
    def __init__(self):
        self.pos = None
        self.vel = None
        self.edible = None
        self.col = None

    def update(self):
        for P in predators:
            diffvec = self.pos - P.pos
            diff = np.linalg.norm(diffvec, axis=1)
            detectmask = (0 < diff) & (diff < 40)
            if np.any(detectmask):
                self.vel[detectmask] += (diffvec[detectmask].T / (diff[detectmask] * 5)).T
        self.vel += np.random.randint(-1, 2, self.vel.shape) / 10
        self.pos += self.vel
        outsidemask = (self.pos < 0) | (self.pos > screensize)
        self.vel[outsidemask] *= -1
        self.pos = np.minimum(np.maximum(self.pos, 0), screensize)
        self.vel *= 0.9

    def show(self):
        for i in range(len(self.pos)):
            pygame.draw.circle(screen, self.col[i], np.int32(self.pos[i]), 5)
            if not self.edible[i]:
                pygame.draw.circle(screen, 0, np.int32(self.pos[i]), 2)

    def addprey(self, pos, vel, edible, col):
        if self.pos is None:
            self.pos = np.float32([pos])
            self.vel = np.float32([vel])
            self.edible = np.bool([edible])
            self.col = np.float32([col])
        else:
            self.pos = np.append(self.pos, [pos], axis=0)
            self.vel = np.append(self.vel, [vel], axis=0)
            self.edible = np.append(self.edible, edible)
            self.col = np.append(self.col, [col], axis=0)


class Predator:
    def __init__(self, pos, vel):
        self.pos = np.float32(pos)
        self.vel = np.float32(vel)
        self.randacc = np.float32([0, 0])
        self.memories = dict()
        self.timer = -10

    def update(self, preylist):
        diffvec = np.float32(self.pos - preylist.pos)
        diff = np.linalg.norm(diffvec, axis=1)
        detectmask = (0 < diff) | (diff < 50)
        bias = np.ones(preylist.pos[detectmask].shape[0], "float32") * 2
        for knowncol in list(self.memories.keys()):
            bias += (np.max(np.abs(knowncol - preylist.col[detectmask]), axis=1) < 50) * self.memories[knowncol]
        self.vel -= np.sum(((diffvec.T / (diff ** 2)) * (np.minimum(np.maximum(bias, -0), 2) / 2)).T, axis=0)
        reachmask = diff < 15
        eatchance = 0.5 - (np.minimum(np.maximum(bias[reachmask], -4.5), 4.5) / 10)
        eatmask = np.random.random_sample(len(eatchance)) > eatchance
        if np.any(eatmask):
            #print(np.argwhere(reachmask)[np.argwhere(eatmask).flatten(), 0])
            i = np.argwhere(reachmask)[np.random.choice(np.argwhere(eatmask).flatten()), 0]
            thiscol = tuple(np.int32(preylist.col[i]))
            try:
                self.memories[thiscol] += [-1, 1][int(preylist.edible[i])]
            except KeyError:
                self.memories[thiscol] = [-1, 1][int(preylist.edible[i])]
            preylist.pos = np.delete(preylist.pos, i, axis=0)
            preylist.vel = np.delete(preylist.vel, i, axis=0)
            preylist.edible = np.delete(preylist.edible, i)
            preylist.col = np.delete(preylist.col, i, axis=0)

        self.randacc += np.random.randint(-1, 2, 2)
        self.randacc = np.minimum(np.maximum(self.randacc, -1), 1)
        self.vel += self.randacc / 10
        self.pos += self.vel
        if self.pos[0] < 0 or self.pos[0] >= w:
            self.pos[0] = np.minimum(np.maximum(self.pos[0], 0), w)
            self.vel[0] *= -0.8
        if self.pos[1] < 0 or self.pos[1] >= h:
            self.pos[1] = np.minimum(np.maximum(self.pos[1], 0), h)
            self.vel[1] *= -0.8
        self.vel *= 0.995
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                predators.remove(self)
        else:
            self.timer += 1
            if self.timer == 0:
                self.timer = 8000

    def show(self):
        if self.timer > 0:
            pygame.draw.circle(screen, COL_RED, np.int32(self.pos), min(10, self.timer))
        elif self.timer < 0:
            pygame.draw.circle(screen, COL_RED, np.int32(self.pos), max(11 + self.timer, 1))


def breed(no, col=None, edible=None):
    # Randomise order whilst preserving individuals
    indices = np.int32([i for i in range(allprey.edible.shape[0])])
    np.random.shuffle(indices)
    allprey.pos = allprey.pos[indices]
    allprey.vel = allprey.vel[indices]
    allprey.edible = allprey.edible[indices]
    allprey.col = allprey.col[indices]
    # Select prey subpopulation according to colour or edibility
    if col is not None:
        colmask = (allprey.col == col)[:, 0].flatten()
    else:
        colmask = np.ones(allprey.edible.shape, "bool")
    if edible is not None:
        ediblemask = (allprey.edible == edible)
    else:
        ediblemask = np.ones(allprey.edible.shape, "bool")
    breedmask = colmask | ediblemask
    # Initialise arrays of new prey data
    addpos = np.float32([[0, 0]])
    addvel = np.float32([[0, 0]])
    addedible = np.bool([False])
    addcol = np.int32([[0, 0, 0]])
    # Generate new prey to be spawned from old ones, no indicates the average number of babies per existing prey
    while no >= 1:
        addpos = np.append(addpos, allprey.pos[breedmask], axis=0)
        addvel = np.append(addvel, 2 * np.random.random_sample(allprey.vel[breedmask].shape), axis=0)
        addedible = np.append(addedible, allprey.edible[breedmask])
        addcol = np.append(addcol, allprey.col[breedmask], axis=0)
        no -= 1
    if no > 0:
        no = int(np.ceil(1 / no))
        addpos = np.append(addpos, allprey.pos[breedmask][::no], axis=0)
        addvel = np.append(addvel, 2 * np.random.random_sample(allprey.vel[breedmask][::no].shape), axis=0)
        addedible = np.append(addedible, allprey.edible[breedmask][::no])
        addcol = np.append(addcol, allprey.col[breedmask][::no], axis=0)
    # Put new prey in with old ones
    allprey.pos = np.append(allprey.pos[1:], addpos, axis=0)
    allprey.vel = np.append(allprey.vel[1:], addvel, axis=0)
    allprey.edible = np.append(allprey.edible[1:], addedible)
    allprey.col = np.append(allprey.col[1:], addcol, axis=0)


allprey = AllPrey()
for i in range(20):
    allprey.addprey(np.random.random_sample(2) * screensize, (0, 0), True, COL_RED)
    allprey.addprey(np.random.random_sample(2) * screensize, (0, 0), False, COL_GREEN)
    allprey.addprey(np.random.random_sample(2) * screensize, (0, 0), True, COL_GREEN)
predators = [Predator(np.random.randint(0, w, 2), (0, 0))]

cycles = 0
while True:
    screen.fill(0)
    for Q in predators:
        Q.update(allprey)
        Q.show()
    allprey.update()
    allprey.show()
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
    cycles += 1
    if cycles % 2000 == 0:
        predators.append(Predator(np.random.randint(0, w, 2), (0, 1)))
        breed(0.75, edible=False)
        breed(0.5, edible=True)
