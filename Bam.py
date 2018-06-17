import numpy as np
import pygame
from pygame.locals import *
from time import sleep

pygame.init()

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((1000, 500), SRCALPHA)
w = screen.get_width()
h = screen.get_height()
screensize = np.float32(screen.get_size())
screenrect = screen.get_rect()

thingrects = []


def circleline(circcent, circrad, linept1, linept2):
    # adapted from my Crawler.py
    # http://mathworld.wolfram.com/Circle-LineIntersection.html
    x1, y1 = linept1 - circcent
    x2, y2 = linept2 - circcent
    p1, p2 = np.float32([[x1, y1], [x2, y2]])
    dx, dy = x2 - x1, y2 - y1
    dr = np.linalg.norm([dx, dy])
    D = (x1 * y2) - (x2 * y1)
    discriminant = ((circrad ** 2) * (dr ** 2)) - (D ** 2)
    if discriminant == 0:
        # print("Clink", circcent, circrad, linept1, linept2)
        retpt = D * np.float32([dy, -dx]) / (dr ** 2)
        if np.linalg.norm(retpt - p1) + np.linalg.norm(retpt - p2) <= dr + 0.1:
            return True
        # pygame.draw.circle(screen, (255, 0, 255), np.int32(retpt + circcent), 10)
    elif discriminant > 0:
        # print("Bam", circcent, circrad, linept1, linept2)
        rootdiscriminant = discriminant ** 0.5
        retpt1 = np.float32([(D * dy) + (np.copysign(dx, dy) * rootdiscriminant),
                             (-D * dx) + (abs(dy) * rootdiscriminant)]) / (dr ** 2)
        retpt2 = np.float32([(D * dy) - (np.copysign(dx, dy) * rootdiscriminant),
                             (-D * dx) - (abs(dy) * rootdiscriminant)]) / (dr ** 2)
        if np.linalg.norm(retpt1 - p1) + np.linalg.norm(retpt1 - p2) <= dr + 0.1:
            return True
        elif np.linalg.norm(retpt2 - p1) + np.linalg.norm(retpt2 - p2) <= dr + 0.1:
            return True
        # pygame.draw.circle(screen, (255, 0, 255), np.int32(retpt1 + circcent), 10)
        # pygame.draw.circle(screen, (255, 0, 255), np.int32(retpt2 + circcent), 10)
    return False


class Thing:
    def __init__(self, pos, vel, rect, col=WHITE):
        self.pos = np.float32(pos)
        self.vel = np.float32(vel)
        self.acc = np.zeros(2, dtype="float32")
        self.col = col
        self.prevpos = self.pos.copy()
        self.strikescreen = pygame.Surface(screensize, SRCALPHA)
    
    def collide(self, other):
        # pygame.draw.line(screen, (255, 0, 0), self.pos, self.prevpos, 5)
        # pygame.draw.circle(screen, (255, 0, 0), np.int32(other.pos), 10)
        if circleline(other.pos, 40, self.pos, self.pos - self.vel):
            self.strikescreen.fill((0, 0, 0, 0))
            pygame.draw.line(self.strikescreen, (255, 0, 0), self.pos, self.prevpos, 5)
            screen.blit(self.strikescreen, (0, 0))
            other.vel += self.vel / 5
            self.vel *= 0.9
            return True
        return False
    
    def kick(self, vec):
        self.acc += vec
        
    def show(self):
        self.vel += self.acc
        self.prevpos = self.pos.copy()
        self.pos += self.vel
        if self.pos[0] < 0 or self.pos[0] > w:
            self.vel[0] *= -0.9
        if self.pos[1] < 0 or self.pos[1] > h:
            self.vel[1] *= -0.9
        self.vel *= 0.99
        self.pos = np.clip(self.pos, np.zeros(2), screensize)
        self.acc = np.zeros(2, dtype="float32")
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 20)


T1 = Thing((20, 20), (2, -1), (0, 0, 20, 20), (0, 255, 0))
T2 = Thing((w - 20, 20), (-1, 1), (0, 0, 20, 20))

blackfade = pygame.Surface(screensize, SRCALPHA)
blackfade.fill((0, 0, 0, 50))

maxzapdelay = 60
hitcounter = 0
boostcounter = 0

keys = set()

while True:
    T1.kick(((K_RIGHT in keys) - (K_LEFT in keys), (K_DOWN in keys) - (K_UP in keys)))
    if boostcounter > 0:
        boostcounter -= 1
    elif K_SPACE in keys:
        T1.kick(T1.vel * 2)
        boostcounter = 200
    if hitcounter % 10 == 0:
        T1.show()
        T2.show()
    if hitcounter == 0:
        if T1.collide(T2):
            hitcounter = maxzapdelay
        screen.blit(blackfade, (0, 0))
    if hitcounter > 0:
        screen.blit(T1.strikescreen, (0, 0))
        hitcounter -= 1
    if hitcounter % (maxzapdelay - 1) == 0:
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
