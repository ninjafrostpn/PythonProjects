# TODO: LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG.

from math import sin, cos, radians, asin, copysign
import numpy as np
import pygame
from pygame.locals import *
import random as r
from time import sleep

pygame.init()

w, h = 1200, 500
screen = pygame.display.set_mode((w, h))

groundy = 20

CRABAPPLE = (135, 56, 47)
DARK_MAGENTA = (100, 0, 100)
BEAK = (255, 255, 0)
BLUESKY = (10, 200, 200)
SAND = np.float32([225, 169, 95])
WHITE = (255, 255, 255)
GREY = np.float32((1, 1, 1))
RED = (255, 0, 0)

xflip = np.float32([-1, 1])

sind = lambda theta: sin(radians(theta))
cosd = lambda theta: cos(radians(theta))

hand = pygame.image.load_extended(r"Crabs/Hand.png").convert_alpha()

SFXphrases = ["crab-powie", "clack", "crunch-stacean", "smack", "bam", "whack", "crunch", "biff", "bop"]
SFXfont = pygame.font.Font(None, 40)

SFXs = []


class SFX:
    def __init__(self, pos):
        self.pos = pos
        self.phrase = SFXfont.render(r.choice(SFXphrases).upper() + ("!" * r.randrange(1, 4)), True, (255, 255, 255))
        self.size = 1
        SFXs.append(self)
    
    def show(self):
        text = pygame.transform.scale(self.phrase, np.float32(self.phrase.get_rect().size) * self.size/200)
        screen.blit(text, self.pos - np.float32(text.get_rect().size)/2 - np.float32([0, text.get_height()]))
        self.size += 9
        if self.size >= 255:
            SFXs.remove(self)

"""
class Shadow:
    def __init__(self, rect, diagonal=False):
        self.rect = pygame.Rect(rect)
        self.mask = np.ones((self.rect.right - self.rect.left, self.rect.bottom - self.rect.top, 3),
                            dtype='float32') * 0.7
        if diagonal:
            self.mask[np.triu_indices(self.mask.shape[0], m=self.mask.shape[1])] = 1
            self.mask = np.flip(self.mask, axis=1)
            self.mask = np.maximum(self.mask, np.flip(self.mask, axis=0))
    
    def move(self, pos, relative=False):
        if relative:
            self.rect = self.rect.move(pos)
        else:
            self.rect.topleft = pos
    
    def enshadow(self, surface):
        surf = pygame.surfarray.pixels3d(surface)
        currrect = self.rect.clip(surface.get_rect())
        maskrect = pygame.Rect(currrect)
        maskrect.topleft = (0, 0)
        darkversion = surf[currrect.left:currrect.right, currrect.top:currrect.bottom] \
                      * self.mask[maskrect.left:maskrect.right, maskrect.top:maskrect.bottom]
        surf[currrect.left:currrect.right, currrect.top:currrect.bottom] = np.uint8(darkversion)
"""


collisions = set()
crabs = []


class Crab:
    def __init__(self, name, pos,
                 width=80, leglength=32,
                 aspect=0.5, legaspect=1,
                 maxspeed=20,
                 controls=(K_UP, K_LEFT, K_DOWN, K_RIGHT), col=CRABAPPLE):
        self.name = name
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
        self.cycles = 0
        self.swimming = False
        self.controls = controls
        self.orighitbox = pygame.Rect(*(-self.arm - self.btm - self.handdiag/2),
                                      *(self.arm * 2 + self.handdiag))
        self.hitbox = self.orighitbox.move(*self.pos)
        self.stance = 0
        self.changestance = -1
        self.dead = False
        crabs.append(self)
    
    def updateinputs(self, keys=set()):
        uppressed, leftpressed, downpressed, rightpressed = [(self.controls[i] in keys) for i in range(4)]
        if leftpressed and not self.dead:
            self.vel[0] -= 1
        if rightpressed and not self.dead:
            self.vel[0] += 1
        if (not (leftpressed ^ rightpressed) or self.dead) and self.vel[0] != 0:
            self.vel[0] -= copysign(min(self.vel[0]/20, 1), self.vel[0])
        if uppressed and not self.dead and not self.swimming:
            self.vel[1] = -7
        if downpressed and not self.dead:
            if abs(self.changestance) == 1:
                self.changestance *= -2
        elif abs(self.changestance) > 1:
            self.changestance -= copysign(1, self.changestance)
        self.vel[0] = min(max(self.vel[0], -self.maxspeed), self.maxspeed)
        
    def isin(self, zone):
        # Zone must be a convex shape defined clockwise
        return np.all(np.cross(zone[1:] - zone[:-1], self.pos - zone[:-1], axis=1) > 0)
        
    def show(self, keys, zone):
        self.stance = min(max(self.stance + copysign(10, self.changestance), 0), 90)
        if self.pos[1] < h - self.btm[1] - groundy:
            self.vel[1] += 0.2
            self.swimming = True
        else:
            if self.vel[1] >= 0:
                self.vel[1] = 0
                self.pos[1] = h - self.btm[1] - groundy
                self.swimming = False
        rightlegjoin = self.pos + self.legjoin
        leftlegjoin = self.pos - self.legjoin
        for i in range(4):
            col = np.maximum(np.minimum(self.col + (10 * i), 255), 0)
            theta = self.cycles + (140 * i)
            theta1 = self.midlegtheta + (self.movelegtheta * sind(theta))
            if not self.swimming:
                theta1 = max(theta1, self.midlegtheta - self.movelegtheta / 2)
            theta1 += r.random() * (self.vel[0]/180)
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
            theta1 += r.random() * (self.vel[0]/180)
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
        pygame.draw.ellipse(screen, WHITE,
                            self.eyerect.move(*(self.pos + self.righteye - np.sign(self.vel))))
        if not self.dead:
            pygame.draw.ellipse(screen, 0,
                                self.eyerect.move(*(self.pos + self.lefteye + np.sign(self.vel)))
                                            .inflate(-2, min(max(self.vel[0] - 8, 4 - self.eyerect.h), -8)))
            pygame.draw.ellipse(screen, 0,
                                self.eyerect.move(*(self.pos + self.righteye))
                                            .inflate(-2, min(max(-self.vel[0] - 8, 4 - self.eyerect.h), -8)))
        else:
            pygame.draw.circle(screen, 0, self.eyerect.move(*(self.pos + self.lefteye)).center, 1)
            pygame.draw.circle(screen, 0, self.eyerect.move(*(self.pos + self.righteye)).center, 1)
        lefthandpos = self.pos - self.arm - self.btm
        righthandpos = self.pos + self.arm - self.btm
        ang1 = 10 * sind(self.cycles)
        ang2 = self.vel[1] * 2 + 40 * sind(self.stance)
        pygame.draw.line(screen, np.int32(WHITE) - self.col, leftlegjoin, lefthandpos, 5)
        currlefthand = pygame.transform.rotate(self.lefthand, (self.vel[0] < 0) * ang1 + ang2).convert_alpha()
        screen.blit(currlefthand, lefthandpos - np.float32(currlefthand.get_rect().size)/2)
        pygame.draw.line(screen, np.int32(WHITE) - self.col, rightlegjoin, righthandpos, 5)
        currrighthand = pygame.transform.rotate(self.righthand, (self.vel[0] > 0) * ang1 - ang2).convert_alpha()
        screen.blit(currrighthand, righthandpos - np.float32(currrighthand.get_rect().size)/2)
        for C in crabs:
            if C != self:
                if self.hitbox.colliderect(C.hitbox):
                    posdiff = C.pos - self.pos + np.float32([0, 50])
                    self.vel -= posdiff * np.float32([(sind(C.stance) - sind(self.stance) + 1)/50,
                                                      (cosd(C.stance) - cosd(self.stance) + 1)/25])
                    C.vel += posdiff * np.float32([(sind(self.stance) - sind(C.stance) + 1)/50,
                                                   (cosd(self.stance) - cosd(C.stance) + 1)/25])
                    if not (self, C) in collisions:
                        collisions.update([(self, C), (C, self)])
                        SFX((self.pos + C.pos) / 2)
                else:
                    collisions.discard((self, C))
                    collisions.discard((C, self))
        self.updateinputs(keys)
        # speed moderated before shoving
        self.vel[0] = min(max(self.vel[0], -self.maxspeed * 2), self.maxspeed * 2)
        self.vel[1] = min(max(self.vel[1], -self.maxspeed/2), self.maxspeed/2)
        self.cycles += self.vel[0]
        if not self.dead:
            if self.swimming:
                self.pos[0] += self.vel[0] * self.stride / 1.5
            else:
                self.pos[0] += self.vel[0] * self.stride
            self.pos[1] += self.vel[1]
        self.pos[0] = min(max(self.pos[0], 0), w)
        self.hitbox = self.orighitbox.move(*self.pos)
        # pygame.draw.rect(screen, WHITE, self.hitbox, 1)
        return not self.isin(zone)


birds = []


class Bird:
    def __init__(self, pos, length=50):
        self.pos = np.float32(pos)
        self.length = length
        self.height = length/4
        self.eyepos = np.float32([0, -self.height/6])
        self.diag = np.float32([self.length, self.height]) / 2
        self.wingpoly = np.float32([(0.35, 0),
                                    (-0.35, 0),
                                    (-0.2, 0.5),
                                    (-0.3, 1),
                                    (0.2, 0.7)])
        self.sidebeakpoly = np.float32([self.eyepos - self.eyepos[::-1],
                                        -self.eyepos * 3 - self.eyepos[::-1] * 10,
                                        -self.eyepos - self.eyepos[::-1]])
        self.frontbeakpoly = np.float32([self.eyepos + self.eyepos[::-1],
                                         -self.eyepos * 3,
                                         self.eyepos - self.eyepos[::-1]])
        self.openbeakpoly = np.float32([(-self.length, -h),
                                        (self.length, -h),
                                        (self.length/3, 0),
                                        (0, -h * 0.7),
                                        (-self.length/3, 0)])
        self.closedbeakpoly = np.float32([(-self.length, -h),
                                          (self.length, -h),
                                          (0, 0)])
        #self.shadow = Shadow((self.pos[0] - self.length, 0, self.length * 2, h))
        self.background = True
        self.cycles = 0
        self.speed = 5
        self.nom = 0
        birds.append(self)
    
    def show(self):
        if self.background:
            headcentre = np.float32([self.pos[0] + copysign(self.length / 2, self.speed), self.pos[1]])
            pygame.draw.ellipse(screen, GREY * 200, (*(self.pos - self.diag), *(self.diag * 2)))
            pygame.draw.polygon(screen, GREY * 100,
                                self.wingpoly * np.float32([copysign(self.length, self.speed),
                                                            self.height * sind(self.cycles)]) + self.pos)
            pygame.draw.circle(screen, GREY * 200, headcentre, int(self.length / 6))
            if activation == 0:
                pygame.draw.polygon(screen, BEAK,
                                    headcentre + self.sidebeakpoly * np.float32([copysign(1, self.speed), 1]))
                pygame.draw.circle(screen, 0, headcentre + self.eyepos, int(self.length / 15))
            else:
                pygame.draw.polygon(screen, BEAK,
                                    headcentre + self.frontbeakpoly)
                pygame.draw.circle(screen, 0, headcentre + self.eyepos - self.eyepos[::-1] * 2, int(self.length / 15))
                pygame.draw.circle(screen, 0, headcentre + self.eyepos + self.eyepos[::-1] * 2, int(self.length / 15))
            self.pos[0] += self.speed
        else:
            self.pos[1] = min(max(self.pos[1] + self.nom, -100), h - groundy)
            if self.pos[1] >= 0:
                if self.nom > 0:
                    pygame.draw.polygon(screen, BEAK,
                                        self.pos + self.openbeakpoly * np.float32([copysign(1, self.speed), 1]))
                else:
                    pygame.draw.polygon(screen, BEAK,
                                        self.pos + self.closedbeakpoly * np.float32([copysign(1, self.speed), 1]))
            elif self.nom < 0:
                self.nom = 0
                self.pos[1] = -100
            pygame.draw.circle(screen, RED, (int(self.pos[0]), 40), 10)
            #self.shadow.move((self.pos[0] - self.length, 0))
            #self.shadow.enshadow(screen)
            if self.nom == 0:
                self.pos[0] += self.speed * 1.5
                for crab in crabs:
                    if not crab.isin(zone):
                        if -self.length/2 < crab.pos[0] - self.pos[0] < self.length/2 or \
                                (self.pos[0] < 0 and crab.pos[0] < 0) or \
                                (self.pos[0] > w and crab.pos[0] > w):
                            self.nom = 10
            elif self.nom > 0:
                hitcrab = False
                for crab in crabs:
                    if crab.hitbox.collidepoint(self.pos):
                        crab.dead = True
                        crab.pos = self.pos
                        hitcrab = True
                if self.pos[1] >= h - groundy or hitcrab:
                    self.nom *= -1
        if self.pos[0] > w + self.length * 2 or self.pos[0] < -self.length * 2:
            if activation/w >= 0.5:
                if self.background:
                    self.background = False
                    self.pos[1] = -100
            else:
                self.background = True
                self.pos[1] = r.randrange(groundy * 2, h - groundy * 2)
            self.speed *= -1
        self.cycles += 10
        

zone = np.int32([(w *  5/16, h),
                 (w *  5/16, h - (w * 3/16)),
                 (w * 11/16, h - (w * 3/16)),
                 (w * 11/16, h)])

crab1 = Crab("Geoffrey", (w/4, h * 0.75), controls=(K_w, K_a, K_s, K_d), col=DARK_MAGENTA)
crab2 = Crab("WinklePicker", (w * 0.75, h * 0.75))

# bunkershadow = Shadow((zone[0][0], zone[1][1], zone[3][0] - zone[0][0], h - zone[1][1]))

keyspressed = set()
activation = 0
gameover = False
timer = 0
while not gameover:
    if timer % 3000 == 0:
        Bird((-50, h/2))
    # It's actually faster to draw this every time than to blit a background in
    # Draw background
    screen.fill(BLUESKY)
    
    # Draw birds in background
    for B in birds:
        if B.background:
            B.show()
    
    # Draw background part of bunker
    pygame.draw.polygon(screen, SAND/1.5, zone)
    for i in range(1, zone.shape[0] - 1):
        pygame.draw.line(screen, GREY * 100, zone[i], (zone[i][0], h), 10)
    
    # Draw crabs in bunker and calculate danger
    r.shuffle(crabs)
    for C in crabs:
        activation += C.show(keyspressed, zone) * len(birds)
        if C.dead and C.pos[1] < 0:
            gameover = True
    activation -= 0.5
    activation = min(max(activation, 0), w)
    
    # Draw foreground portion of bunker, including sand
    # bunkershadow.enshadow(screen)
    pygame.draw.lines(screen, GREY * 100, False, zone, 10)
    for i in range(1, zone.shape[0] - 1):
        pygame.draw.circle(screen, GREY * 150, zone[i], 10)
    pygame.draw.rect(screen, SAND, (0, h - groundy, w, h - groundy))

    # Draw birds in foreground
    for B in birds:
        if not B.background:
            B.show()
    
    # Draw danger bar
    pygame.draw.rect(screen, GREY * 200, (0, 0, w, 20))
    pygame.draw.rect(screen, (255 * activation / w, 255 * (1 - activation / w), 0), (0, 0, activation, 20))
    pygame.draw.line(screen, 0, (activation, 0), (activation, 20), 2)
    pygame.draw.line(screen, 0, (0, 20), (w, 20), 2)
    for S in SFXs:
        S.show()
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keyspressed.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type == KEYUP:
            keyspressed.remove(e.key)
    sleep(0.002)
    timer += 1

for C in crabs:
    if not C.dead:
        print(C.name, "WINS")
    else:
        print(C.name, "LOSES")
