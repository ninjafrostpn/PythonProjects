import pygame
from pygame.locals import *
import numpy as np
from time import sleep, time

pygame.init()

manualmode = False
Kp = 0.5
Ki = 0
Kd = 0.05

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))
font = pygame.font.Font(None, 40)


class Thing:
    def __init__(self, masspos, mass, shuttlepos):
        self.pos = np.float32(masspos)
        self.vel = np.zeros(2, "float32")
        self.acc = np.zeros(2, "float32")
        self.force = np.zeros(2, "float32")
        self.mass = mass
        self.invmass = 1 / mass
        self.shuttlepos = np.float32(shuttlepos)
        self.origdist = np.linalg.norm(self.pos - self.shuttlepos)

    def update(self, t):
        distvec = self.pos - self.shuttlepos
        normvec = distvec / np.linalg.norm(distvec)
        self.force += [0, self.mass]
        self.force -= np.dot(self.force, normvec) * normvec
        self.acc = self.force * self.invmass
        self.force[:] = 0
        self.vel += self.acc * t
        self.vel -= np.dot(self.vel, normvec) * normvec
        self.pos += self.vel * t
        distvec = self.pos - self.shuttlepos
        dist = np.linalg.norm(distvec)
        self.pos = self.shuttlepos + (distvec * (self.origdist / dist))

    def show(self):
        correctedpos = self.pos - self.shuttlepos + screensize/2
        pygame.draw.line(screen, (255, 255, 0), correctedpos, screensize/2, 2)
        pygame.draw.circle(screen, (0, 0, 255), np.int32(correctedpos), 10, 0)
        pygame.draw.line(screen, (255, 0, 255), (0, h/2), (w, h/2), 2)
        for i in range(4):
            xpos = (i * w/4) - self.shuttlepos[0]
            correctedxpos = xpos % w
            pygame.draw.line(screen, (255, 255, 255), (correctedxpos, 0), (correctedxpos, h), 2)
            screen.blit(font.render(str((xpos * 4) // w), True, (255, 255, 255)), (correctedxpos + 5, 0))


keys = set()

Q = Thing(screensize/4, 10, screensize/2)
Q.force += 10

prevtime = time()
while True:
    if K_LEFT in keys:
        Q.force += [-1, 0]
    elif K_RIGHT in keys:
        Q.force += [1, 0]
    screen.fill(0)
    if manualmode:
        Q.shuttlepos[:] = pygame.mouse.get_pos()
    else:
        Q.shuttlepos[0] += ((Q.vel * Kp) +
                            (Q.acc * Kd) +
                            ((Q.pos - Q.shuttlepos) * Ki))[0]
    nexttime = time()
    # print(nexttime - prevtime)
    while prevtime < nexttime:
        Q.update(0.05)
        prevtime += 0.01
    prevtime = nexttime
    Q.show()
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
