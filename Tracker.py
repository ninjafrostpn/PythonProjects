from math import acos, atan2, cos, radians, sin, sqrt
import numpy as np
import pygame
from pygame.locals import *
from time import sleep

WHITE = np.int32([255, 255, 255])
GREY = np.int32([1, 1, 1])
RED = np.int32([255, 0, 0])
GREEN = np.int32([0, 255, 0])
BLUE = np.int32([0, 0, 255])
CYAN = BLUE + GREEN
perpmat =np.matrix([[0, -1],
                    [1,  0]])

pygame.init()

w, h = 1000, 500
screensize = np.int32([w, h])
screen = pygame.display.set_mode((w, h))

tracks = []
drivers = []
followers = []


class Segment:
    def __init__(self, pt1, pt2, col=WHITE):
        self.pts = np.float32([pt1, pt2])
        self.parallelunit = self.pts[1] - self.pts[0]
        self.length = np.linalg.norm(self.parallelunit)
        self.parallelunit /= self.length
        self.perpunit = perpmat.dot(self.parallelunit)
        self.col = col
        tracks.append(self)
    
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


class Track:
    def __init__(self, ptlist, ends=(None, None), col=WHITE):
        self.ptlist = list(ptlist)
        self.segments = []
        self.closed = ends == (None, None)
        if not self.closed:
            self.ends = ends
        else:
            self.ends = None
        for i in range(len(self.ptlist) + self.closed - 1):
            S = Segment(self.ptlist[i], self.ptlist[(i + 1) % len(self.ptlist)], col)
            self.segments.append(S)
            tracks.remove(S)
        self.col = col
        tracks.append(self)
    
    def __add__(self, other):
        if isinstance(other, Track):
            return Track(self.ptlist + other.ptlist, self.closed, self.col)
        elif isinstance(other, Segment):
            return Track(self.ptlist + other.pts, self.closed, self.col)
        else:
            newptlist = self.ptlist
            for pt in other:
                newptlist.append(pt)
            return Track(newptlist, self.closed, self.col)
    
    def __sub__(self, other):
        newptlist = self.ptlist
        if isinstance(other, Track):
            removals = other.ptlist
        elif isinstance(other, Segment):
            removals = other.pts
        else:
            removals = list(other)
        for pt in removals:
            try:
                newptlist.remove(pt)
            except ValueError:
                pass
        return Track(newptlist, self.closed, self.col)

    def posspoints(self, pos, dist, segi=-1, pref=(0,0), filterbest=True):
        poss = []
        segis = []
        for newsegi, S in enumerate(self.segments):
            pt, _ = S.posspoints(pos, dist, pref=pref)
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
    
    def calcpos(self, alongpos, segi=0):
        currseg = self.segments[segi]
        while alongpos < 0:
            if segi == 0:
                if self.closed:
                    segi = len(self.segments) - 1
                    currseg = self.segments[segi]
                    alongpos += currseg.length
                else:
                    if self.ends[0] is None:
                        alongpos = 0
                    else:
                        return self.ends[0].nexttrack(self)
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
                    if self.ends[0] is None:
                        alongpos = currseg.length
                    else:
                        return self.ends[0].nexttrack(self)
            else:
                segi += 1
                alongpos -= currseg.length
                currseg = self.segments[segi]
        return alongpos, currseg.pts[0] + (currseg.parallelunit * alongpos), segi, self

    def show(self):
        for S in self.segments:
            S.show()


class Trackchange:
    def __init__(self):
        # Is attached to several tracks on one side and the other
        # Could be attached to far or near end of said tracks
        # Must send position of moving items to next track on opposite side according to its own state
        # May involve reversing speed of train according to directionality of incoming and outgoing tracks
        # No idea about Followers...
        ...
    
    def next(self):
        ...
    
    def show(self):
        ...


class Driver:
    def __init__(self, track, alongpos, speed=1, col=WHITE):
        self.track = track
        self.alongpos = alongpos
        self.alongpos, self.pos, self.segi, self.track = self.track.calcpos(self.alongpos)
        self.speed = speed
        self.col = col
        drivers.append(self)
        
    def move(self, howmuch):
        self.alongpos += howmuch * self.speed
        self.alongpos, self.pos, self.segi, self.track = self.track.calcpos(self.alongpos, self.segi)
    
    def jumptracks(self, newtrack, maxjump=2):
        for i in range(int(maxjump + 1)):
            pos, segi = newtrack.posspoints(self.pos, i)
            if pos is not None:
                self.track = newtrack
                self.pos = pos
                self.segi = segi
                self.alongpos = np.dot(newtrack.segments[segi].parallelunit,
                                       self.pos - newtrack.segments[segi].pts[0])
                break
    
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
        
    def move(self):
        pos, segi = self.track.posspoints(self.driver.pos, self.chainlength, self.segi, self.pos)
        if pos is not None:
            self.pos, self.segi = pos, segi
    
    def show(self):
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 15, 1)
        pygame.draw.line(screen, self.col, self.pos, self.driver.pos)


class Train:
    def __init__(self, front, rear, maincol=WHITE, bogeycol=WHITE):
        self.ends = [front, rear]
        self.maincol = maincol
        self.bogeycol = bogeycol
    
    def show(self):
        for end in self.ends:
            seg = end.track.segments[end.segi]
            parallelunit, perpunit = seg.parallelunit, seg.perpunit
            outline = [(end.pos + parallelunit * 20 + perpunit * 10),
                       (end.pos + parallelunit * 20 - perpunit * 10),
                       (end.pos - parallelunit * 20 - perpunit * 10),
                       (end.pos - parallelunit * 20 + perpunit * 10)]
            pygame.draw.polygon(screen, self.bogeycol, [(i[0, 0], i[0, 1]) for i in outline])
        parallelunit = self.ends[0].pos - self.ends[1].pos
        parallelunit /= np.linalg.norm(parallelunit)
        perpunit = perpmat.dot(parallelunit)
        outline = [(self.ends[0].pos + (parallelunit + perpunit) * 10),
                   (self.ends[0].pos + (parallelunit - perpunit) * 10),
                   (self.ends[1].pos + (-parallelunit - perpunit) * 10),
                   (self.ends[1].pos + (-parallelunit + perpunit) * 10)]
        pygame.draw.polygon(screen, self.maincol, [(i[0, 0], i[0, 1]) for i in outline])
    
    
rad = int(w/8)

t1 = []
t2 = []
for i in range(-90, 91, 10):
    t1.append([(w - 200) + cos(radians(i)) * 170,
               h/2 + sin(radians(i)) * (h/2 - 30)])
    t2.append([(w - 270) + cos(radians(i)) * 170,
               (h/2 - 30) + sin(radians(i)) * (h/2 - 60)])
for i in range(90, 271, 10):
    t1.append([200 + cos(radians(i)) * 170,
               h/2 + sin(radians(i)) * (h/2 - 30)])
    t2.append([270 + cos(radians(i)) * 170,
               (h/2 - 30) + sin(radians(i)) * (h/2 - 60)])
    
T1 = Track(t1)
T2 = Track(t2)

D1 = Driver(T2, -200, speed=2, col=CYAN)
F1 = Follower(T1, D1, 100, startpref=(w, 0))
F2 = Follower(T1, F1, 50, startpref=(w, 0))
F3 = Follower(T1, F2, 100, startpref=(w, 0))
Tren = Train(D1, F1, GREEN, BLUE)
Carriage = Train(F2, F3, RED, BLUE)

keys = set()

while True:
    screen.fill(0)
    # mpos = pygame.mouse.get_pos()
    for S in tracks:
        S.show()
    for D in drivers:
        D.move((K_RIGHT in keys) - (K_LEFT in keys))
    for F in followers:
        F.move()
    Tren.show()
    Carriage.show()
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
