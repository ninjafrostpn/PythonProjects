from math import acos, atan2, cos, radians, sin, sqrt
import numpy as np
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

segments = []


class Segment:
    def __init__(self, pt1, pt2, col=WHITE):
        self.col = col
        self.pts = np.float32([pt1, pt2])
        self.parallelunit = self.pts[1] - self.pts[0]
        self.parallelunit /= np.linalg.norm(self.parallelunit)
        self.perpunit = np.matrix([[0, -1],
                                   [1,  0]]).dot(self.parallelunit)
        segments.append(self)
    
    def posspoints(self, pos, dist):
        try:
            pos = np.float32(pos)
            topos = pos - self.pts[0]
            todist = np.linalg.norm(topos)
            ang = acos(np.dot(self.parallelunit, topos) / todist)  # Because unit vector has length 1
            toposparallel = todist * cos(ang)
            toposperp = todist * sin(ang)
            spreaddist = sqrt((dist ** 2) - (toposperp ** 2))
            alongdist1 = toposparallel - spreaddist
            alongdist2 = toposparallel + spreaddist
            return np.float32([self.parallelunit * alongdist1, self.parallelunit * alongdist2]) + self.pts[0]
        except ValueError:
            return np.float32([])
        
    def show(self, ):
        pygame.draw.line(screen, self.col, *self.pts[:])

Segment((0, 0), (w, h), col=(255, 255, 0))
Segment((w, 0), (0, h), col=(255, 0, 255))
rad = int(w/4)

while True:
    screen.fill(0)
    mpos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, WHITE, mpos, rad, 1)
    for S in segments:
        S.show()
        for pt in S.posspoints(mpos, rad):
            pygame.draw.circle(screen, S.col, np.int32(pt), 10)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
