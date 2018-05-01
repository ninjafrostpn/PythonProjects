import numpy as np
import pygame
from pygame.locals import *
from time import sleep

w, h = 500, 500
size = (w, h)
screen = pygame.display.set_mode(size)


trampolines = []
class TrampoLine:
    def __init__(self, end1, end2, k, sticky=True):
        self.ends = np.float32([end1, end2])
        self.k = k
        self.sticky = sticky
        self.balltracker = []
        for B in balls:
            self.balltracker.append(np.sign(np.cross(B.pos - self.ends[0], self.ends[1] - self.ends[0])))
        trampolines.append(self)
    
    def show(self):
        for i, B in enumerate(balls):
            side = np.sign(np.cross(B.pos - self.ends[0], self.ends[1] - self.ends[0]))
            if side * self.balltracker[i] == -1:
                vecs = np.float32([self.ends[i] - B.pos for i in range(2)])
                dists = np.linalg.norm(vecs, axis=1)
                normvecs = vecs/dists
                # shouldbe = np.linalg.norm(self.ends[0] - self.ends[1])/2
                forces = self.k * dists * normvecs
                for j, force in enumerate(forces):
                    B.force(force)
                    pygame.draw.line(screen, (0, 255, 255), self.ends[j], B.pos)
        pygame.draw.line(screen, (255, 0, 255), self.ends[0], self.ends[1], 3)


balls = []
class Ball:
    def __init__(self, pos, mass):
        self.pos = np.float32(pos)
        self.vel = np.float32([0, 0])
        self.acc = np.float32([0, 0])
        self.invmass = 1/mass
        for T in trampolines:
            T.balltracker.append(np.sign(np.cross(self.pos - T.ends[0], T.ends[1] - T.ends[0])))
        balls.append(self)
    
    def force(self, F, scaleformass=True):
        if scaleformass:
            self.acc += np.float32(F) * self.invmass
        else:
            self.acc += np.float32(F)
    
    def show(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc = np.float32([0, 0])
        pygame.draw.circle(screen, (255, 255, 0), self.pos, 10)
    
    def __del__(self):
        try:
            for T in trampolines:
                T.balltracker.remove(self)
        except:
            pass


corners = [(100, 400), (400, 400), (400, 100), (100, 100)]
for i in range(len(corners)):
    TrampoLine(corners[i], corners[(i + 1) % len(corners)], 0.1)
Q = Ball((200, 250), 1)

while True:
    screen.fill(0)
    for B in balls:
        B.force((0, 5), False)  # Gravity
        B.show()
    for T in trampolines:
        T.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
            if e.key == K_LEFT:
                Q.force((-5, -5))
            if e.key == K_RIGHT:
                Q.force((5, -5))
    sleep(0.1)
