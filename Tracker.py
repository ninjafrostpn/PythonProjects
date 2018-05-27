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
        self.length = np.linalg.norm(self.parallelunit)
        self.parallelunit /= self.length
        self.perpunit = np.matrix([[0, -1],
                                   [1,  0]]).dot(self.parallelunit)
        self.col = col
        segments.append(self)
    
    def posspoints(self, pos, dist, segi=-1, pref=(0, 0), filterbest=True):
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
                poss = np.float32([self.parallelunit * alongdist1, self.parallelunit * alongdist2]) + self.pts[0]
                if not filterbest:
                    return poss, segi
            else:
                poss = np.float32([self.parallelunit * dist, self.parallelunit * -dist]) + self.pts[0]
                if not filterbest:
                    return poss, segi
        except ValueError:
            return None, segi
        if len(poss) != 0:
            best = np.argmin(np.linalg.norm(poss - np.float32(pref), axis=1))
            return poss[best], segi
        else:
            return None, segi
    
    def calcpos(self, alongpos, segi=-1):
        relpos = self.parallelunit * min(max(alongpos, 0), self.length)
        return alongpos, self.pts[0] + relpos, segi
        
    def show(self):
        pygame.draw.line(screen, self.col, *self.pts[:])


class Driver:
    def __init__(self, track, alongpos, speed=1, col=WHITE):
        self.track = track
        self.alongpos = alongpos
        self.alongpos, self.pos, self.segi = self.track.calcpos(self.alongpos)
        self.speed = speed
        self.col = col
        drivers.append(self)
        
    def move(self, howmuch):
        self.alongpos += howmuch * self.speed
        self.alongpos, self.pos, self.segi = self.track.calcpos(self.alongpos, self.segi)
    
    def show(self):
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 15, 1)


class Follower:
    def __init__(self, track, driver, chainlength, startpref=(0, 0), col=WHITE):
        self.track = track
        self.driver = driver
        self.chainlength = chainlength
        self.segi = -1
        self.pos, self.segi = self.track.posspoints(self.driver.pos, self.chainlength, self.segi, startpref)
        self.col = col
        followers.append(self)
    
    def show(self):
        pos, segi = self.track.posspoints(self.driver.pos, self.chainlength, self.segi, self.pos)
        if pos is not None:
            self.pos, self.segi = pos, segi
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 15, 1)
        pygame.draw.line(screen, self.col, self.pos, self.driver.pos)
        

class Track:
    def __init__(self, ptlist, closed=True, col=WHITE):
        self.ptlist = list(ptlist)
        self.segments = []
        self.closed = closed
        for i in range(len(self.ptlist) + self.closed - 1):
            self.segments.append(Segment(ptlist[i], ptlist[(i + 1) % len(ptlist)], col))
        self.col = col

    def posspoints(self, pos, dist, segi=-1, pref=(0,0), filterbest=True):
        if segi == -1:
            poss = []
            segis = []
            for S in self.segments:
                pt, newsegi = S.posspoints(pos, dist, pref=pref)
                if pt is not None and (0 <= np.dot(S.parallelunit, pt - S.pts[0]) <= S.length):
                    poss.append(pt)
                    segis.append(newsegi)
            poss = np.float32(poss)
            if not filterbest:
                return poss, segis
            if len(poss) != 0:
                best = np.argmin(np.linalg.norm(poss - np.float32(pref), axis=1))
                return poss[best], segis[best]
            else:
                return None, segi
        else:
            pass
    
    def calcpos(self, alongpos, segi=0):
        currseg = self.segments[segi]
        while alongpos < 0:
            if segi == 0:
                if self.closed:
                    segi = len(self.segments) - 1
                    currseg = self.segments[segi]
                    alongpos += currseg.length
                else:
                    alongpos = 0
            else:
                segi -= 1
                currseg = self.segments[segi]
                alongpos += currseg.length
        while alongpos > currseg.length:
            if segi == len(self.segments) - 1:
                if self.closed:
                    segi = 0
                    alongpos -= currseg.length
                    currseg = self.segments[segi]
                else:
                    alongpos = currseg.length
            else:
                segi += 1
                alongpos -= currseg.length
                currseg = self.segments[segi]
        return alongpos, currseg.pts[0] + (currseg.parallelunit * alongpos), segi
        
rad = int(w/8)

T1 = Track(125 * (3 * np.ones(2) - np.float32([(cos(radians(theta)), sin(radians(theta))) for theta in range(0, 360, 20)])))
T2 = Segment((0, 60), (w, h), col=(255, 0, 255))
T3 = Segment((60, 0), (w, h), col=(0, 255, 0))
T4 = Segment((w, 0), (0, h), col=(255, 0, 0))

D1 = Driver(T1, 0, col=(0, 255, 255))
F1 = Follower(T1, D1, 100, startpref=(w, h))
F2 = Follower(T2, D1, 200, startpref=(w/2, h/2))
F3 = Follower(T3, F1, 200, startpref=(w/2, h/2))
F4 = Follower(T2, F3, 100, startpref=(0, 0))
F5 = Follower(T1, F4, 280, startpref=(0, 0))

keys = set()

while True:
    screen.fill(0)
    mpos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, WHITE, mpos, rad, 1)
    for S in segments:
        S.show()
        # pts, _ = S.posspoints(mpos, rad)
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
    sleep(0.001)
