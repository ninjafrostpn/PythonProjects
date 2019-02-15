import pygame
from pygame.locals import *
import numpy as np
import time
import random

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

WHITE = (255, 255, 255)
WAHPURPLE = (84, 6, 116)
WAHYELLOW = (255, 242, 0)

font = pygame.font.Font(None, 20)

gravity = np.float32([0, 1000])

# Following this tutorial, because learning:
# https://gamedevelopment.tutsplus.com/tutorials/
#         how-to-create-a-custom-2d-physics-engine-the-basics-and-impulse-resolution--gamedev-6331


def resolvecollision(pair):
    # Takes a pair of objects that might be colliding and, if they are,
    #     enacts forces on them such that they are not
    A, B = pair
    # print(A, B)
    norm = A.getcollisionnorm(B)
    if norm is not None:
        norm = np.float32(norm)
        relvel = B.vel - A.vel
        normspd = relvel.dot(norm)
        # print(norm, relvel, normspd)
        if normspd < 0:
            restitution = min(A.material.restitution,
                              B.material.restitution)
            imp = norm * -(1 + restitution) * normspd
            totmass = A.mass + B.mass
            if B.mass == 0:
                A.vel -= imp
            elif A.mass == 0:
                B.vel += imp
            else:
                A.vel -= (B.mass / totmass) * imp
                B.vel += (A.mass / totmass) * imp


class Shape:
    # Stores the shape of a Thing, used for displaying it and colliding with it
    def __init__(self, area=0):
        self.area = area

    def __str__(self):
        return str(type(self))

    def show(self, pos, colour):
        # Takes position and colour, displays shape at that position on the screen using that colour
        pygame.draw.circle(screen, colour, pos, 50, 1)

    def broadcollidecoords(self, pos):
        # Provides bounding-box coords for checking if the object might be colliding
        return None

    def getcollisionnorm(self, pos, other, otherpos):
        # Checks if the shape is colliding
        #     Returns a collision normal if so
        #     Returns None if not
        return None


class Circle(Shape):
    def __init__(self, rad):
        self.rad = abs(rad)
        super().__init__(np.pi * rad * rad)

    def show(self, pos, colour):
        pygame.draw.circle(screen, colour, pos, self.rad)

    def broadcollidecoords(self, pos):
        r = (pos - self.rad, pos + self.rad)
        # print(r, self.rad)
        return r

    def getcollisionnorm(self, pos, other, otherpos):
        if type(other) == Circle:
            circdist = np.linalg.norm(pos - otherpos)
            totrad = self.rad + other.rad
            if circdist < totrad:
                return (otherpos - pos) / circdist
        elif type(other) == Wall:
            if other.horizontal:
                if abs(pos[1] - otherpos[1]) < self.rad:
                    if pos[1] < otherpos[1]:
                        return 0, -1
                    else:
                        return 0, 1
            else:
                if abs(pos[0] - otherpos[0]) < self.rad:
                    if pos[0] < otherpos[0]:
                        return -1, 0
                    else:
                        return 1, 0
        return None


class Wall(Shape):
    def __init__(self, horizontal=True):
        self.horizontal = horizontal
        super().__init__()

    def show(self, pos, colour):
        pass

    def broadcollidecoords(self, pos):
        if self.horizontal:
            return (0, pos[1]), (w, pos[1])
        else:
            return (pos[0], 0), (pos[0], h)

    def getcollisionnorm(self, pos, other, otherpos):
        if type(other) == Circle:
            if self.horizontal:
                if abs(pos[1] - otherpos[1]) < other.rad:
                    if pos[1] < otherpos[1]:
                        return 0, 1
                    else:
                        return 0, -1
            else:
                if abs(pos[0] - otherpos[0]) < other.rad:
                    if pos[0] < otherpos[0]:
                        return 1, 0
                    else:
                        return -1, 0
        return None


class Material:
    # Stores the parameters giving the characteristics of a Thing
    def __init__(self, density, restitution):
        self.density = density
        self.restitution = restitution

    def __str__(self):
        return "[Density: %s - Restit: %s]" % (self.density, self.restitution)


class Thing:
    # The objects which are displayed on the screen and moved around according to the physics
    def __init__(self, shape, material, pos, vel=(0, 0), col=(255, 255, 255)):
        self.material = material
        self.shape = shape
        self.density = self.material.density
        self.area = self.shape.area
        self.mass = self.area * self.density
        # print(self.mass)
        if self.mass == 0:
            self.invmass = 0
        else:
            self.invmass = 1 / self.mass
        self.restitution = self.material.restitution
        self.pos = np.float32(pos)
        self.vel = np.float32(vel)
        self.force = np.float32([0, 0])

        self.angpos = 0
        self.angvel = 0
        self.torque = 0
        self.col = col
        stuff.append(self)

    def __str__(self):
        return "Shape: %s - Material: %s - Colour: %s" % (self.shape, self.material, self.col)

    def show(self):
        self.shape.show(self.pos, self.col)

    def update(self, tstep):
        self.force += gravity * self.mass
        self.vel += self.force * self.invmass * tstep
        self.pos += self.vel * tstep

        self.angvel += self.torque * self.invmass * tstep
        self.angpos += self.angvel * tstep

        if wraparoundLR:
            self.pos[0] = self.pos[0] % w
        if wraparoundUD:
            self.pos[1] = self.pos[1] % h
        self.force[:] = 0
        self.torque = 0

    def applyforce(self):
        pass

    def setmaterial(self, material):
        if material != self.material:
            self.material = material
            self.density = self.material.density
            self.mass = self.area * self.density
            if self.mass == 0:
                self.invmass = 0
            else:
                self.invmass = 1 / self.mass
            self.restitution = self.material.restitution

    def setshape(self, shape):
        if shape != self.shape:
            self.shape = shape
            self.area = self.shape.area
            self.mass = self.area * self.density
            if self.mass == 0:
                self.invmass = 0
            else:
                self.invmass = 1 / self.mass

    def checkbroadcollision(self, other):
        selfcoords = self.shape.broadcollidecoords(self.pos)
        othercoords = other.shape.broadcollidecoords(other.pos)
        # Separating axis theorem
        if selfcoords[1][0] < othercoords[0][0] or selfcoords[0][0] > othercoords[1][0]:
            return False
        if selfcoords[1][1] < othercoords[0][1] or selfcoords[0][1] > othercoords[1][1]:
            return False
        return True

    def getcollisionnorm(self, other):
        return self.shape.getcollisionnorm(self.pos, other.shape, other.pos)


keys = set()
stuff = []

hpi = np.pi / 2

immovable = Material(0, 1)
ballstoff = Material(1, 1)

wraparoundLR = False
wraparoundUD = False

if not wraparoundLR:
    vertwall = Wall(False)
    lftwall = Thing(vertwall, immovable, (0, 0))
    rgtwall = Thing(vertwall, immovable, (w, 0))

if not wraparoundUD:
    horiwall = Wall(True)
    topwall = Thing(horiwall, immovable, (0, 0))
    btmwall = Thing(horiwall, immovable, (0, h))

for i in range(1, 5):
    for j in range(1, 5):
        ball = Thing(Circle(5 + i), ballstoff, (w * (i / 10), h * (j / 10)), (100 * j, -100 * i), WAHYELLOW)

fps = 300
timestep = 1 / fps
accumulator = 0

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
        #random.shuffle(stuff)
        for O in stuff:
            O.update(timestep)
        potentialcollisions = []
        for i in range(len(stuff)):
            for j in range(i + 1, len(stuff)):
                if stuff[i].checkbroadcollision(stuff[j]):
                    potentialcollisions.append((stuff[i], stuff[j]))
        for C in potentialcollisions:
            resolvecollision(C)
        accumulator -= timestep
    screen.fill(0)
    for O in stuff:
        O.show()
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
