import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))


class Segment:
    def __init__(self, length, angvel, startang):
        self.length = length
        self.angvel = angvel
        self.angoffset = startang * 10
        self.ang = 0
        self.nextseg = None
    
    def attach(self, seg):
        self.nextseg = seg
    
    def show(self, t, basepos, offset, energyuse=0):
        self.ang = (45 * np.sin(np.deg2rad((t * self.angvel/20) + self.angoffset))) + offset
        endpos = basepos + (self.length * np.sin(np.deg2rad([self.ang + 90, self.ang])))
        pygame.draw.line(screen, 255, basepos, endpos)
        if self.nextseg is not None:
            self.nextseg.show(t, endpos, self.ang)


wavers = []


class Waver:
    def __init__(self, base):
        self.basepos = np.float32(base)
        self.baseoffset = np.random.random() * 360
        self.segments = []
        self.energy = 100
        wavers.append(self)
        
    def addsegment(self, seglength, segangvel, segstartang):
        newseg = Segment(seglength, segangvel, segstartang)
        if self.segments:
            self.segments[-1].attach(newseg)
        self.segments.append(newseg)
    
    def show(self, t):
        self.segments[0].show(t, self.basepos, self.baseoffset)


def wavergen(base, code):
    W = Waver(base)
    # code is a string of code letters
    # - J for new segment
    # - Q for increased velocity of segment movement
    # - q for the opposite (can go into negative for reversed direction)
    # - L for increased length of segment
    # - l for the opposite (can go into negative for inverted segments)
    seglength = 1
    segvelocity = 1
    segstartang = 0
    for c in code:
        if c == "J":
            W.addsegment(seglength, segvelocity, segstartang)


keys = set()

cycles = 0
while True:
    screen.fill(0)
    for Worm in wavers:
        Worm.show(cycles)
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
    sleep(0.001)
    cycles += 1
