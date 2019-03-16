import numpy as np
import pygame
from pygame.locals import *
from time import sleep

pygame.init()

screen = pygame.display.set_mode((1000, 500))
w = screen.get_width()
h = screen.get_height()
screensize = np.float32([w, h])

allbirbs = []


class Birb:
    def __init__(self, pos, col):
        self.acc = np.float32([0, 0])
        self.vel = np.float32([0, 0])
        self.pos = np.float32(pos)
        self.col = col
        allbirbs.append(self)
    
    def update(self, dynamicity=0.95):
        self.vel += self.acc
        self.pos += self.vel
        self.vel *= dynamicity
        self.pos = np.clip(self.pos, (0, 0), screensize)
        self.acc = np.float32([0, 0])
    
    def show(self):
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 3)
    

class Flock:
    def __init__(self, population=10, neighbourno=2, tightness=20, strength=0.1, dynamicity=0.95):
        self.dynamicity = dynamicity  # Ranges best from 0, position-based, to 1, completely free acceleration
        self.birbno = population
        self.birbs = [Birb((np.random.random() * w, np.random.random() * h),
                           (i * (255/self.birbno), (self.birbno - i) * (255/self.birbno), 0))
                      for i in range(self.birbno)]
        self.tightness = tightness
        self.strength = strength
        self.neighbourno = neighbourno
    
    def show(self):
        np.random.shuffle(self.birbs)
        birbvecs = np.zeros((self.birbno, self.birbno, 2), "float32")
        for i in range(self.birbno):
            for j in range(i, self.birbno):
                if i == j:
                    birbvecs[i, j] = screensize * 2
                else:
                    vec = self.birbs[j].pos - self.birbs[i].pos
                    birbvecs[i, j] = vec
                    birbvecs[j, i] = -vec
        birbdists = np.linalg.norm(birbvecs, axis=2)
        # Begin bodge to avoid sticking together
        zerodists = birbdists == 0
        birbdists[zerodists] = 1
        birbvecs[zerodists] = np.random.normal(0, 1, (np.count_nonzero(zerodists), 2))
        # Move birbs toward their nearest neighbours
        for i, birb in enumerate(self.birbs):
            closest = np.argpartition(birbdists[i], min(max(self.neighbourno, 0), self.birbno - 1))[:self.neighbourno]
            corrections = (birbvecs[i][closest].T * ((birbdists[i][closest] - self.tightness) / birbdists[i][closest])).T
            correction = np.sum(corrections, axis=0) * self.strength
            birb.acc += correction
            birb.update(self.dynamicity)
            birb.show()


F = Flock(200, 15, 60, strength=0.1)

selecting = False
selectrect = pygame.Rect(0, 0, 0, 0)
selectedbirbs = []

keys = set()

while True:
    mousepos = np.float32(pygame.mouse.get_pos())
    F.tightness += (K_w in keys) - (K_s in keys)
    F.neighbourno += (K_d in keys) - (K_a in keys)
    screen.fill(0)
    for birb in selectedbirbs:
        birb.acc += np.float32([(K_RIGHT in keys) - (K_LEFT in keys),
                                (K_DOWN in keys) - (K_UP in keys)])
    F.show()
    if selecting:
        selectrect.size = mousepos - np.float32(selectrect.topleft)
        pygame.draw.rect(screen, 255, selectrect, 1)
    for birb in selectedbirbs:
        pygame.draw.circle(screen, 255, np.int32(birb.pos), 3, 1)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
            elif e.key == K_SPACE:
                selectedbirbs = []
            keys.add(e.key)
        elif e.type == KEYUP:
            keys.discard(e.key)
        elif e.type == MOUSEBUTTONDOWN and not selecting:
            selectrect.topleft = np.float32(mousepos)
            selectrect.size = (0, 0)
            selectedbirbs = []
            selecting = True
        elif e.type == MOUSEBUTTONUP and selecting:
            selectrect.size = mousepos - np.float32(selectrect.topleft)
            selectrect.normalize()
            selectrect.inflate_ip(3, 3)
            for birb in allbirbs:
                if selectrect.collidepoint(*birb.pos):
                    selectedbirbs.append(birb)
            selecting = False
    # sleep(0.01)
