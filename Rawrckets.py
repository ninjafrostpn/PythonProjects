import numpy as np
import pygame
from pygame.locals import *
from time import sleep

# Orb in the centre with four hands, one for each cardinal direction
# Arrow keys for movement
# WASD for grabbing items or using the ones held
# Q and E for rotating hands around one step in either direction (or maybe LSHUFT and SHIFT?)
# X to drop item in WASD hands active

pygame.init()

ORANGE = np.float32((255, 100, 0))

w, h = 1000, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

rockets = []


class Rocket:
    def __init__(self, launchpos, launchangle, launchspeed, radius=10):
        self.pos = np.float32(launchpos)
        self.vel = np.float32([np.cos(np.deg2rad(launchangle)), np.sin(np.deg2rad(launchangle))]) * launchspeed
        self.acc = np. float32([0, 0])
        self.radius = radius
        self.exploding = 0
        rockets.append(self)
    
    def update(self):
        if not np.all((0 < self.pos) & (self.pos < (w, h))) or self.exploding:
            self.exploding += 10
    
    def show(self):
        self.update()
        if not self.exploding:
            self.acc[1] += 1
            self.vel += self.acc
            self.pos += self.vel
            self.acc[:] = 0
            pygame.draw.circle(screen, (0, 0, 255), np.int32(self.pos), int(self.radius))
        else:
            if self.exploding < 255:
                pygame.draw.circle(screen, np.int32(ORANGE * (255 - self.exploding) / 255),
                                   np.int32(self.pos), int(self.radius * (self.exploding/255 + 1)))
            else:
                rockets.remove(self)
                del self


launchers = []


class Launcher:
    def __init__(self, pos, launchangle, rocketspeed, rocketradius, reloadperiod):
        self.pos = np.float32(pos)
        self.angle = launchangle
        self.rocketspeed = rocketspeed
        self.rocketradius = rocketradius
        self.reloadperiod = reloadperiod
        self.timer = 0
        launchers.append(self)
    
    def fire(self):
        if self.timer == 0:
            Rocket(self.pos, self.angle, self.rocketspeed, self.rocketradius)
            self.timer = self.reloadperiod
    
    def show(self):
        if self.timer > 0:
            self.timer -= 1
        pygame.draw.circle(screen, (255, 0, 0), np.int32(self.pos), int(self.rocketradius) + 2)
        pygame.draw.circle(screen, (255, 255, 255), np.int32(self.pos), int(self.rocketradius) + 2, 2)


keys = set()
launcherA = Launcher((0, 0), 180, 50, 20, 10)
launcherW = Launcher((0, 0), -135, 20, 50, 100)
robotpos = screensize / 2

while True:
    screen.fill((0, 0, 0))
    launcherA.pos = robotpos
    launcherW.pos = robotpos + (0, -30)
    if K_a in keys:
        launcherA.fire()
    if K_w in keys:
        launcherW.fire()
    for L in launchers:
        L.show()
    for R in rockets:
        R.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type ==KEYUP:
            keys.discard(e.key)
    sleep(0.01)
