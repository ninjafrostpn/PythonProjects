from math import acos, atan2, cos, radians, sin, sqrt
import numpy as np
import pygame
from pygame.locals import *
from time import sleep

WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

segments = []
drivers = []
followers = []


class Segment:
    def __init__(self, pt1, pt2, col=WHITE):
        self.pts = np.float32([pt1, pt2])
        self.parallelunit = self.pts[1] - self.pts[0]
        self.parallelunit /= np.linalg.norm(self.parallelunit)
        self.perpunit = np.matrix([[0, -1],
                                   [1,  0]]).dot(self.parallelunit)
        self.col = col
        segments.append(self)
    
    def posspoints(self, pos, dist):
        try:
            pos = np.float32(pos)
            topos = pos - self.pts[0]
            todist = np.linalg.norm(topos)
            if todist > 0:
                ang = acos(np.dot(self.parallelunit, topos) / todist)  # Because unit vector has length 1
                toposparallel = todist * cos(ang)
                toposperp = todist * sin(ang)
                spreaddist = sqrt((dist ** 2) - (toposperp ** 2))
                alongdist1 = toposparallel - spreaddist
                alongdist2 = toposparallel + spreaddist
                return np.float32([self.parallelunit * alongdist1, self.parallelunit * alongdist2]) + self.pts[0]
            else:
                return np.float32([self.parallelunit * dist, self.parallelunit * -dist]) + self.pts[0]
        except ValueError:
            return np.float32([])
    
    def calcpos(self, alongpos):
        return self.pts[0] + (self.parallelunit * alongpos)
        
    def show(self):
        pygame.draw.line(screen, self.col, *self.pts[:])


class Driver:
    def __init__(self, track, alongpos, speed=1, col=WHITE):
        self.track = track
        self.alongpos = alongpos
        self.pos = self.track.calcpos(self.alongpos)
        self.speed = speed
        self.col = col
        drivers.append(self)
        
    def move(self, howmuch):
        self.alongpos += howmuch * self.speed
        self.pos = self.track.calcpos(self.alongpos)
    
    def show(self):
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 15, 1)
        

class Follower:
    def __init__(self, track, driver, chainlength, startpref=(0, 0), col=WHITE):
        self.track = track
        self.driver = driver
        self.chainlength = chainlength
        self.place(startpref)
        self.col = col
        followers.append(self)
    
    def place(self, pref=None):
        if pref is None:
            pref = self.pos
        else:
            pref = np.float32(pref)
        poss = self.track.posspoints(self.driver.pos, self.chainlength)
        if len(poss) != 0:
            best = np.argmin(np.linalg.norm(poss - pref, axis=1))
            self.pos = poss[best]
    
    def show(self):
        self.place()
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 15, 1)
        pygame.draw.line(screen, self.col, self.pos, self.driver.pos)
        
        
rad = int(w/4)

T1 = Segment((0, 0), (w, h), col=(255, 255, 0))
T2 = Segment((0, 60), (w, h + 10), col=(255, 0, 255))
T3 = Segment((0, 120), (w, h + 60), col=(0, 255, 0))
D1 = Driver(T1, 0, speed=5, col=(0, 255, 255))
F1 = Follower(T3, D1, rad, startpref=T1.parallelunit * -rad)
F2 = Follower(T1, F1, rad, startpref=T3.parallelunit * 2 * -rad)
F3 = Follower(T3, F2, rad, startpref=T3.parallelunit * 3 * -rad)

keys = set()

while True:
    screen.fill(0)
    mpos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, WHITE, mpos, rad, 1)
    for S in segments:
        S.show()
        for pt in S.posspoints(mpos, rad):
            pygame.draw.circle(screen, S.col, np.int32(pt), 10)
    for D in drivers:
        D.move((K_RIGHT in keys) - (K_LEFT in keys))
        D.show()
    for F in followers:
        F.show()
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
    sleep(0.01)
