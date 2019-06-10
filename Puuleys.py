import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()

w, h = 1000, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

gravity = np.float32([0, 1])
airresist = 0.995
allk = 0.1
ropes = []
masses = []
pulleys = []
thrusters = []


class Rope:
    def __init__(self, end1, end2, length=None):
        self.end1 = end1
        self.end2 = end2
        self.k = allk  # Universal atm
        if length is None:
            self.length = np.linalg.norm(self.end1.pos - self.end2.pos)
        else:
            self.length = float(length)
        ropes.append(self)

    def update(self):
        d = self.end2.pos - self.end1.pos
        dmag = np.linalg.norm(d)
        x = dmag - self.length
        # Springy when pulled, slack when released
        if x > 0:
            F = d * self.k * x / dmag
            self.end1.applyforce(F)
            self.end2.applyforce(-F)

    def show(self):
        pygame.draw.line(screen, (255, 0, 255), self.end1.pos, self.end2.pos)


class Mass:
    def __init__(self, mass, pos, col=(255, 255, 0)):
        self.col = col
        self.mass = float(mass)
        if self.mass != 0:
            self.invmass = 1 / self.mass
        else:
            self.invmass = 0
        self.pos = np.float32(pos)
        self.vel = np.float32([0, 0])
        self.acc = np.float32([0, 0])
        self.force = np.float32([0, 0])
        masses.append(self)

    def applyforce(self, F):
        self.force += F
        toplftmask = self.pos <= 0
        btmrgtmask = self.pos >= screensize
        self.force[toplftmask] = np.maximum(self.force[toplftmask], 0)
        self.force[btmrgtmask] = np.minimum(self.force[btmrgtmask], 0)
        # pygame.draw.line(screen, (255, 255, 255), self.pos, self.pos + F * 50)

    def update(self):
        if self.mass != 0:
            self.acc += self.force * self.invmass
            self.vel += self.acc
            self.pos += self.vel
            toplftmask = self.pos < 0
            btmrgtmask = self.pos > screensize
            self.pos[toplftmask][:] = 0
            self.pos[btmrgtmask] = screensize[btmrgtmask]
            self.vel[toplftmask] = np.maximum(self.vel[toplftmask], 0)
            self.vel[btmrgtmask] = np.minimum(self.vel[btmrgtmask], 0)
            self.vel *= airresist
        self.force[:] = 0
        self.acc[:] = 0

    def show(self):
        pygame.draw.circle(screen, self.col, np.int32(self.pos), 10)


class Pulley(Mass):
    def __init__(self, mass, pos, end1, end2, length=None, ropecol=(0, 0, 255), pulleycol=(0, 255, 0)):
        self.ropecol = ropecol
        super(Pulley, self).__init__(mass, pos, pulleycol)
        self.end1 = end1
        self.end2 = end2
        self.k = allk  # Universal atm
        if length is None:
            self.length = np.linalg.norm(self.end1.pos - self.pos) + np.linalg.norm(self.end2.pos - self.pos)
        else:
            self.length = float(length)
        pulleys.append(self)

    def update(self):
        d1 = self.end1.pos - self.pos
        d2 = self.end2.pos - self.pos
        dmag1 = np.linalg.norm(d1)
        dmag2 = np.linalg.norm(d2)
        x = dmag1 + dmag2 - self.length
        # Tension applied when pulled, slack when released
        if x >= 0:
            Fmag1 = np.dot(self.end1.force, d1 / dmag1)
            Fmag2 = np.dot(self.end2.force, d2 / dmag2)
            Tmag = ((self.end1.mass * Fmag2) + (self.end2.mass * Fmag1)) / (self.end1.mass + self.end2.mass)
            # print(Fmag1 - Tmag, Fmag2 - Tmag)
            self.end1.applyforce(-d1 * Tmag / dmag1)
            self.end2.applyforce(-d2 * Tmag / dmag2)
            self.applyforce((d1 * Tmag / dmag1) + (d2 * Tmag / dmag2))
            F1 = d1 * self.k * x / dmag1
            F2 = d2 * self.k * x / dmag2
            self.end1.applyforce(-F1)
            self.end2.applyforce(-F2)
            self.applyforce(F1 + F2)
        if self.mass != 0:
            self.acc += self.force * self.invmass
            self.vel += self.acc
            self.pos += self.vel
            self.vel *= airresist
        self.force[:] = 0
        self.acc[:] = 0

    def show(self):
        pygame.draw.line(screen, self.ropecol, np.int32(self.pos), np.int32(self.end1.pos))
        pygame.draw.line(screen, self.ropecol, np.int32(self.pos), np.int32(self.end2.pos))
        super(Pulley, self).show()


class Thruster:
    def __init__(self, thing, thrust, controls=(K_UP, K_DOWN, K_LEFT, K_RIGHT)):
        self.thing = thing
        self.thrust = float(thrust)
        self.controls = controls
        thrusters.append(self)

    def update(self):
        self.thing.applyforce(np.float32([(self.controls[3] in keys) - (self.controls[2] in keys),
                                          (self.controls[1] in keys) - (self.controls[0] in keys)]) * self.thrust)


class Player:
    def __init__(self):
        self.mass = Mass(1, [w/2, h/2], col=(100, 100, 100))
        self.rope = None

    def update(self):
        if self.rope is None:
            if K_z in keys:
                closest = sorted(masses, key=lambda i: (np.linalg.norm(i.pos - self.mass.pos) ** 2))[1]
                if np.linalg.norm(closest.pos - self.mass.pos) < 30:
                    self.rope = Rope(closest, self.mass, 20)
        if (self.rope is not None) and (K_z not in keys or self.mass.pos[1] < self.rope.end1.pos[1]):
            ropes.remove(self.rope)
            del self.rope
            self.rope = None
        jump = np.float32([0, 0])
        if K_UP in keys and self.mass.force[1] <= 0:
            jump -= 20 * gravity
        if K_LEFT in keys and self.mass.force[0] <= 0:
            jump[0] -= 1
        if K_RIGHT in keys and self.mass.force[0] >= 0:
            jump[0] += 1
        self.mass.applyforce(jump * self.mass.mass)
        if self.rope is not None:
            self.rope.end1.applyforce(-jump * self.mass.mass)


keys = set()

scenario = 2

if scenario == 0:
    A = Mass(0, [w/2, 0])
    B = Mass(1, [w/4, h/4])
    C = Mass(2, [w/2, h/2])
    D = Mass(0, [0, 0])
    E = Mass(0, [w, 0])
    F = Mass(1.5, [w/3, h/2])
    AB = Rope(A, B)
    BC = Rope(B, C)
    CD = Rope(C, D)
    CE = Rope(C, E)
    BF = Rope(B, F)
elif scenario == 1:
    A = Mass(0, [w/4, 0])
    B = Mass(0, [w/2, 0])
    C = Mass(0.3, [w * 5/8, h/4])
    D = Mass(2, [w * 3/4, h/2])
    E = Pulley(0, [w * 3/4, 0], C, D, ropecol=(255, 0, 0), pulleycol=(100, 0, 0))
    F = Pulley(0.3, [w/2, h/2], B, C, ropecol=(0, 255, 0), pulleycol=(0, 100, 0))
    G = Pulley(0.3, [w/4, h * 5/8], A, F, ropecol=(0, 0, 255), pulleycol=(0, 0, 100))
    H = Thruster(D, 1, (K_w, K_s, K_a, K_d))
    I = Mass(4, [w/4, h * 6/8])
    J = Rope(G, I)
elif scenario == 2:
    Nw = 5
    Nh = 4
    for i in range(1, Nw + 1):
        A = Mass(0, [(i + 1) * w / (Nw + 2), 0])
        for j in range(0, Nh + 1):
            B = Mass(2, [(i + 1) * w/(Nw + 2), (j + 1) * h/(Nh + 5)])
            Rope(A, B)
            A = B
elif scenario == 3:
    N = 10
    A = Mass(N + 2, [w/2, h/2])
    Thruster(A, N + 2, (K_w, K_s, K_a, K_d))
    for i in np.arange(1, N + 1):
        B = Mass(1, [(i + 1) * w/(N + 2), h/2])
        C = Pulley(2, [(i + 0.5) * w/(N + 2), h/4], A, B)
        D = Mass(0, [(i + 0.5) * w/(N + 2), 0])
        Rope(C, D)
        E = Mass(2, [(i + 1) * w/(N + 2), h/1.5])
        Rope(B, E)
P = Player()


while True:
    screen.fill(0)
    for R in ropes:
        R.update()
    for T in thrusters:
        T.update()
    for M in masses:
        M.applyforce(gravity * M.mass)
    P.update()
    for M in masses:
        M.update()
        M.show()
    for R in ropes:
        R.show()
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
