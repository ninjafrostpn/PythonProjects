import pygame
from pygame.locals import *
import numpy as np
import time
import glob
import random

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

WHITE = (255, 255, 255)
WAHPURPLE = (84, 6, 116)
WAHYELLOW = (255, 242, 0)

font = pygame.font.Font(None, 20)

wahsounds = [pygame.mixer.Sound(file) for file in glob.glob(r"D:\Users\Charles Turvey\Music\SFX\Waluigi\Wahs\Wah*.wav")]
wahtexts = [font.render(wahtext, True, WHITE, (0, 0, 0)) for wahtext in ["Wwwah!",
                                                              "Wwahhh!",
                                                              "Wwwwah-haaa!",
                                                              "Wah-ha-haa!",
                                                              "Wah-haa!",
                                                              "Waaah!"]]
wahs = []


class Wah:
    def __init__(self, pos):
        self.wahid = random.randrange(0, len(wahsounds))
        pygame.mixer.find_channel(True).play(wahsounds[self.wahid])
        self.pos = np.float32(pos.copy()) - np.float32(wahtexts[self.wahid].get_size())/2 + (0, 20)
        self.pos[0] = min(max(self.pos[0], 0), w - wahtexts[self.wahid].get_width())
        self.wahstart = time.time()
        wahs.append(self)
        if countwhacks:
            whackcounter.append(1)

    def show(self):
        if time.time() - self.wahstart < 1.5:
            screen.blit(pygame.transform.rotate(wahtexts[self.wahid], (0.5 - random.random()) * 10), self.pos)
        else:
            wahs.remove(self)
            del self


# Following this tutorial, because learning:
# https://gamedevelopment.tutsplus.com/tutorials/
#         how-to-create-a-custom-2d-physics-engine-the-basics-and-impulse-resolution--gamedev-6331


def resolveCollision(a, b, norm):
    relvel = b.vel - a.vel
    normspd = relvel.dot(norm)
    if normspd < 0:
        restit = min(a.restit, b.restit)
        imp = norm * -(1 + restit) * normspd
        totmass = a.mass + b.mass
        a.vel -= (b.mass / totmass) * imp
        b.vel += (a.mass / totmass) * imp


class AABB:
    # Axis aligned bounding box
    def __init__(self, minpt, maxpt, mass, restit):
        self.rect = pygame.Rect(*minpt, maxpt[0] - minpt[0], maxpt[1] - minpt[1])
        self.vel = np.float32([0, 0])
        self.mass = mass
        if mass == 0:
            self.invmass = 0
        else:
            self.invmass = 1 / mass
        self.restit = restit

    def show(self):
        pygame.draw.rect(screen, WAHPURPLE, self.rect, 2)

    def vsAABB(self, other):
        # Separating axis theorem
        if self.rect.right < other.rect.left or self.rect.left < other.rect.right:
            return False
        if self.rect.bottom < other.rect.top or self.rect.top < other.rect.bottom:
            return False
        return True


class Circle:
    def __init__(self, pos, rad, mass, restit):
        self.pos = np.float32(pos)
        self.rad = float(rad)
        self.vel = np.float32([0, 0])
        self.mass = mass
        if mass == 0:
            self.invmass = 0
        else:
            self.invmass = 1 / mass
        self.restit = restit
        stuff.append(self)

    def show(self):
        pygame.draw.circle(screen, WAHPURPLE, self.pos, int(self.rad))
        pygame.draw.rect(screen, WAHYELLOW, pygame.Rect(*(self.pos - self.rad/2), self.rad, self.rad/3))
        pygame.draw.rect(screen, WAHYELLOW, pygame.Rect(*(self.pos - self.rad/2), self.rad/3, self.rad * 1.2))

    def update(self, i, t):
        for O in stuff[i + 1:]:
            circdist = np.linalg.norm(self.pos - O.pos)
            totrad = self.rad + O.rad
            if circdist < totrad:
                Wah((self.pos + O.pos) / 2)
                resolveCollision(self, O, (O.pos - self.pos) / circdist)
        if ((self.pos[0] < self.rad) and leftwall) or ((self.pos[0] > w - self.rad) and rightwall):
            Wah(self.pos)
            self.vel[0] *= -1
        if ((self.pos[1] < self.rad) and topwall) or ((self.pos[1] > h - self.rad) and bottomwall):
            Wah(self.pos)
            self.vel[1] *= -1
        self.pos += self.vel * t


keys = set()
stuff = []

hpi = np.pi / 2

whackcounter = []
countwhacks = False
leftwall = rightwall = topwall = bottomwall = True

fps = 60
timestep = 1 / fps
accumulator = 0

secondballmult = 1

framestart = time.time()
while True:
    # Work out how long it's been since the last frame was displayed
    # Calculate how many physics steps should have been carried out in that time
    # Calculate their effects
    # THEN display
    nowtime = time.time()
    accumulator += nowtime - framestart
    framestart = nowtime
    while accumulator > timestep:
        random.shuffle(stuff)
        for i, O in enumerate(stuff):
            O.update(i, timestep)
        accumulator -= timestep
    screen.fill(0)
    for O in stuff:
        O.show()
    for W in wahs:
        W.show()
    if countwhacks:
        screen.blit(font.render(str(sum(whackcounter)) + " wahcks, mass of right ball 100^"
                                + str(secondballmult) + " (" + str(100 ** secondballmult) + ") times mass of left",
                                True, WHITE), (10, 10))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
            if e.key == K_SPACE:
                leftwall = rightwall = topwall = bottomwall = True
                fps = 60
                timestep = 1 / fps
                stuff.clear()
                countwhacks = False
                for i in range(20):
                    theta = np.pi * (i / 10)
                    Circle((np.sin([theta, theta + hpi]) * 100) + screensize / 2, 10, 1, 1)
                    stuff[i].vel = np.sin([theta, theta + hpi]) * 100
            if e.key == K_0:
                fps = 60
                timestep = 1 / fps
                stuff.clear()
                whackcounter.clear()
                countwhacks = True
                rightwall = False
                leftwall = True
                Circle((200, 400), 10, 1, 1)
                Circle((230, 400), 10, 1, 1)
                secondballmult = 0
                stuff[1].vel[0] = -20
            if e.key == K_1:
                fps = 200
                timestep = 1 / fps
                stuff.clear()
                whackcounter.clear()
                countwhacks = True
                rightwall = False
                leftwall = True
                Circle((200, 400), 10, 1, 1)
                Circle((230, 400), 10, 100, 1)
                secondballmult = 1
                stuff[1].vel[0] = -20
            if e.key == K_2:
                fps = 500
                timestep = 1 / fps
                stuff.clear()
                whackcounter.clear()
                countwhacks = True
                rightwall = False
                leftwall = True
                Circle((200, 400), 10, 1, 1)
                Circle((230, 400), 10, 10000, 1)
                secondballmult = 2
                stuff[1].vel[0] = -20
            if e.key == K_3:
                fps = 1000
                timestep = 1 / fps
                stuff.clear()
                whackcounter.clear()
                countwhacks = True
                rightwall = False
                leftwall = True
                Circle((200, 400), 10, 1, 1)
                Circle((230, 400), 10, 1000000, 1)
                secondballmult = 3
                stuff[1].vel[0] = -20
            if e.key == K_4:
                fps = 10000
                timestep = 1 / fps
                stuff.clear()
                whackcounter.clear()
                countwhacks = True
                rightwall = False
                leftwall = True
                Circle((200, 400), 10, 1, 1)
                Circle((230, 400), 10, 100000000, 1)
                secondballmult = 4
                stuff[1].vel[0] = -20
        elif e.type == KEYUP:
            keys.discard(e.key)
