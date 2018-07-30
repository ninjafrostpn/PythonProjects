import pygame
from pygame.locals import *
import numpy as np
import time

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))


def drawarrow(surface, col, pos, ang, arrowwidth, arrowlength, width=0):
    pos = np.float32(pos)
    pygame.draw.polygon(surface, col, [pos + np.float32([np.cos(np.radians(ang)),
                                                         -np.sin(np.radians(ang))]) * arrowlength,
                                       pos + np.float32([np.cos(np.radians(ang - 90)),
                                                         -np.sin(np.radians(ang - 90))]) * arrowwidth / 2,
                                       pos + np.float32([np.cos(np.radians(ang + 90)),
                                                         -np.sin(np.radians(ang + 90))]) * arrowwidth / 2],
                        width)


class Leaper:
    def __init__(self, pos):
        self.pos = np.float32(pos)
        self.vel = np.float32([0, 0])
        self.ang = -np.degrees(np.arctan2(*self.vel[::-1]))
        self.jumpang = 0
        self.jumpspeed = 2
        self.jumping = False
    
    def show(self, jumping=False):
        pygame.draw.circle(screen, 255, np.int32(self.pos), 10)
        drawarrow(screen, (0, 255, 0), self.pos, self.ang, 10, 30, 2)
        self.ang = -np.degrees(np.arctan2(*self.vel[::-1]))
        if jumping:
            if not self.jumping:
                self.jumping = True
                self.jumpang = self.ang
            self.jumpang += ((K_LEFT in keys) - (K_RIGHT in keys))
            drawarrow(screen, (255, 0, 0), self.pos, self.jumpang, 10, 30, 2)
        else:
            if self.jumping:
                self.jumping = False
                self.vel += np.float32([np.cos(np.radians(self.jumpang)),
                                        -np.sin(np.radians(self.jumpang))]) * self.jumpspeed
            self.pos += self.vel
            while True:
                if self.pos[0] < 0:
                    self.pos[0] *= -1
                    self.vel[0] *= -1
                elif self.pos[1] < 0:
                    self.pos[1] *= -1
                    self.vel[1] *= -1
                elif self.pos[0] > w:
                    self.pos[0] = w - (self.pos[0] - w)
                    self.vel[0] *= -1
                elif self.pos[1] > h:
                    self.pos[1] = h - (self.pos[1] - h)
                    self.vel[1] *= -1
                else:
                    break
            self.ang = -np.degrees(np.arctan2(*self.vel[::-1]))
            self.vel *= 0.995


keys = set()

L = Leaper(screensize / 2)
Q = Leaper(screensize / 4)

start = time.time()

while True:
    screen.fill(0)
    leaptime = int((time.time() - start) * 10) % 12 < 5
    L.show(leaptime)
    Q.show(leaptime)
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
    time.sleep(0.001)
