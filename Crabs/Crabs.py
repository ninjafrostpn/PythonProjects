from math import sin, cos, radians, asin, copysign
import numpy as np
import pygame
from pygame.locals import *
from random import random
from time import sleep

w, h = 1200, 500
screen = pygame.display.set_mode((w, h))

CRABAPPLE = (135, 56, 47)
WHITE = (255, 255, 255)
DARK_MAGENTA = (100, 0, 100)

xflip = np.float32([-1, 1])

sind = lambda theta: sin(radians(theta))
cosd = lambda theta: cos(radians(theta))

hand = pygame.image.load_extended(r"Crabs/Hand.png").convert_alpha()

crabs = []


class Crab:
    def __init__(self, pos,
                 width=100, leglength=40,
                 aspect=0.5, legaspect=1,
                 maxspeed=20,
                 controls=(K_UP, K_LEFT, K_DOWN, K_RIGHT), col=CRABAPPLE):
        self.pos = np.float32(pos)
        self.vel = np.float32([0, 0])
        self.maxspeed = maxspeed
        self.col = np.int32(col)
        self.width = width
        self.aspect = aspect
        self.height = width * aspect
        self.diag = np.float32([self.width, self.height]) / 2
        self.rgt = np.float32([self.width / 2, 0])
        self.btm = np.float32([0, self.width * aspect / 2])
        self.rect = pygame.Rect(0, 0, *(self.diag * 2))
        self.eyerect = pygame.Rect(0, 0, *(self.diag[::-1] / 2))
        self.leglength1 = leglength
        self.legaspect = legaspect
        self.leglength2 = leglength * legaspect
        uplegtheta = asin(self.leglength2 / self.leglength1)
        downlegtheta = asin((self.leglength2 - (self.btm[1] * 2)) / self.leglength1)
        self.midlegtheta = (uplegtheta + downlegtheta) / 2
        self.movelegtheta = uplegtheta - self.midlegtheta
        self.legjoin = 0.9 * self.rgt
        self.stride = self.leglength2 * cosd(22.5) / 90
        self.lefteye = -self.diag[::-1] / 1.2
        self.righteye = (self.lefteye * xflip) - np.float32([self.eyerect.w, 0])
        self.lefthand = pygame.transform.scale(hand, (int(hand.get_width() * self.height * 1.1 / hand.get_width()),
                                                      int(hand.get_height() * self.height * 1.1 / hand.get_width())))
        self.righthand = pygame.transform.flip(self.lefthand, True, False)
        self.handdiag = np.float32(self.lefthand.get_rect().size)
        self.arm = np.float32([self.leglength1 * 2.1, 0])
        self.armcol = np.int32(WHITE) - self.col
        self.cycles = 0
        self.swimming = False
        self.controls = controls
        self.orighitbox = pygame.Rect(*(-self.arm - self.btm - self.handdiag/2),
                                      *(self.arm * 2 + self.btm + self.handdiag))
        self.hitbox = self.orighitbox.move(*self.pos)
        crabs.append(self)
    
    def move(self, keys):
        uppressed, leftpressed, downpressed, rightpressed = [(self.controls[i] in keys) for i in range(4)]
        if leftpressed:
            self.vel[0] -= 1
        if rightpressed:
            self.vel[0] += 1
        if not (leftpressed ^ rightpressed) and self.vel[0] != 0:
            self.vel[0] -= copysign(min(self.vel[0]/20, 1), self.vel[0])
        if uppressed:
            if not self.swimming:
                self.vel[1] = -5
        if downpressed:
            self.vel[0] = 0
        self.vel[0] = min(max(self.vel[0], -self.maxspeed), self.maxspeed)
    
    def show(self):
        if self.pos[1] < h - self.btm[1]:
            self.vel[1] += 0.1
            self.swimming = True
        else:
            if self.vel[1] >= 0:
                self.vel[1] = 0
                self.pos[1] = h - self.btm[1]
                self.swimming = False
        rightlegjoin = self.pos + self.legjoin
        leftlegjoin = self.pos - self.legjoin
        for i in range(4):
            col = np.maximum(np.minimum(self.col + (10 * i), 255), 0)
            theta = self.cycles + (140 * i)
            theta1 = self.midlegtheta + (self.movelegtheta * sind(theta))
            if not self.swimming:
                theta1 = max(theta1, self.midlegtheta - self.movelegtheta / 2)
            theta1 += random() * (self.vel[0]/180)
            theta2 = -30 * (3 + cosd(theta))
            legpos1 = self.leglength1 * np.float32([cos(theta1), -sin(theta1)])
            legpos2 = self.leglength2 * np.float32([cosd(theta2), -sind(theta2)])
            pygame.draw.lines(screen, col, False,
                              [rightlegjoin,
                               rightlegjoin + legpos1,
                               rightlegjoin + legpos1 + legpos2],
                              5)
            theta1 = self.midlegtheta + (self.movelegtheta * sind(-theta))
            if not self.swimming:
                theta1 = max(theta1, self.midlegtheta - self.movelegtheta / 2)
            theta1 += random() * (self.vel[0]/180)
            theta2 = -30 * (3 + cosd(-theta))
            legpos1 = self.leglength1 * np.float32([cos(theta1), -sin(theta1)])
            legpos2 = self.leglength2 * np.float32([cosd(theta2), -sind(theta2)])
            pygame.draw.lines(screen, col, False,
                              [leftlegjoin,
                               leftlegjoin + (legpos1 * xflip),
                               leftlegjoin + ((legpos1 + legpos2) * xflip)],
                              5)
        pygame.draw.ellipse(screen, self.col,
                            self.rect.move(*(self.pos - self.diag)))
        pygame.draw.ellipse(screen, WHITE,
                            self.eyerect.move(*(self.pos + self.lefteye)))
        pygame.draw.ellipse(screen, 0,
                            self.eyerect.move(*(self.pos + self.lefteye + np.sign(self.vel)))
                                        .inflate(-2, min(max(self.vel[0] - 8, 8 - self.eyerect.h), -8)))
        pygame.draw.ellipse(screen, WHITE,
                            self.eyerect.move(*(self.pos + self.righteye - np.sign(self.vel))))
        pygame.draw.ellipse(screen, 0,
                            self.eyerect.move(*(self.pos + self.righteye))
                                        .inflate(-2, min(max(-self.vel[0] - 8, 8 - self.eyerect.h), -8)))
        lefthandpos = self.pos - self.arm - self.btm
        righthandpos = self.pos + self.arm - self.btm
        pygame.draw.line(screen, self.armcol, leftlegjoin, lefthandpos, 5)
        currlefthand = pygame.transform.rotate(self.lefthand,
                                               (self.vel[0] < 0) * 10 * sind(self.cycles) + self.vel[1] * 2)
        screen.blit(currlefthand, lefthandpos - np.float32(currlefthand.get_rect().size)/2)
        pygame.draw.line(screen, self.armcol, rightlegjoin, righthandpos, 5)
        currrighthand = pygame.transform.rotate(self.righthand,
                                                (self.vel[0] > 0) * 10 * sind(self.cycles) - self.vel[1] * 2)
        screen.blit(currrighthand, righthandpos - np.float32(currrighthand.get_rect().size)/2)
        self.vel[0] = min(max(self.vel[0], -self.maxspeed), self.maxspeed)  # speed moderated before shoving
        for C in crabs:
            if C != self:
                if self.hitbox.colliderect(C.hitbox):
                    # random() for breaking up equal chances
                    C.vel[0] += (C.pos[0] - self.pos[0] + random()) * np.linalg.norm(self.vel - C.vel)
        self.cycles += self.vel[0]
        if self.swimming:
            self.pos[0] += self.vel[0] * self.stride / 1.5
        else:
            self.pos[0] += self.vel[0] * self.stride
        self.pos[1] += self.vel[1]
        self.hitbox = self.orighitbox.move(*self.pos)
        # pygame.draw.rect(screen, WHITE, self.hitbox, 1)


crab1 = Crab((w/4, h/2))
crab2 = Crab((w * 0.75, h/2), controls=(K_w, K_a, K_s, K_d), col=DARK_MAGENTA)

keyspressed = set()
while True:
    screen.fill(0)
    for C in crabs:
        C.move(keyspressed)
        C.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keyspressed.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type == KEYUP:
            keyspressed.remove(e.key)
    sleep(0.01)