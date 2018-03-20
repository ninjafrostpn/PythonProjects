import math
import random
import time
import pygame
from pygame.locals import *

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

dist = lambda p1, p2: math.sqrt(((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))


class InvalidOperation(Exception):
    pass


class InvalidIndex(Exception):
    pass


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return dist((0, 0), (self.x, self.y))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (type(3), type(0.3))):
            return Vector(self.x * other, self.y * other)
        elif isinstance(other, type(Vector(0, 0))):
            return (self.x * other.x) + (self.y * other.y)
        else:
            raise InvalidOperation

    def __truediv__(self, other):
        if isinstance(other, (type(3), type(0.3))):
            return Vector(self.x / other, self.y / other)
        else:
            raise InvalidOperation

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise InvalidIndex

    def __iter__(self):
        yield int(self.x)
        yield int(self.y)
    
    def __str__(self):
        return "V({}, {})".format(*self)

    def norm(self):
        if abs(self) == 0:
            return Vector(0, 0)
        else:
            return self / abs(self)
    
    def copy(self):
        return Vector(self.x, self.y)


g = Vector(0, 150)


class Spring:
    def __init__(self, end1, end2, spring_constant, length=-1, col=(255, 0, 0)):
        self.end1 = end1
        self.end2 = end2
        self.k = spring_constant
        if length < 0:
            self.l = abs(self.end1.pos - self.end2.pos)
        else:
            self.l = length
        self.col = col

    def show(self):
        fact = (abs(self.end1.pos - self.end2.pos) - self.l) * -self.k
        self.end1.kick((self.end1.pos - self.end2.pos).norm() * fact)
        self.end2.kick((self.end2.pos - self.end1.pos).norm() * fact)
        pygame.draw.line(screen, self.col, tuple(self.end1.pos), tuple(self.end2.pos))


def touchline(pt, line):
    # http://mathworld.wolfram.com/Circle-LineIntersection.html
    r = 5
    x1, y1 = line.p1 - pt
    x2, y2 = line.p2 - pt
    dx = x2 - x1
    dy = y2 - y1
    dr = math.sqrt((dx ** 2) + (dy ** 2))
    D = (x1 * y2) - (x2 * y1)
    disc = ((r ** 2) * (dr ** 2)) - (D ** 2)
    if disc == 0:
        retpt = Vector((D * dy) / (dr ** 2),
                       (-D * dx) / (dr ** 2))
        print("yolp", retpt)
        retpt += pt
    elif disc > 0:
        retpt1 = Vector(((D * dy) + (math.copysign(dx, dy) * math.sqrt(disc))) / (dr ** 2),
                        ((-D * dx) + (abs(dy) * math.sqrt(disc))) / (dr ** 2))
        retpt2 = Vector(((D * dy) - (math.copysign(dx, dy) * math.sqrt(disc))) / (dr ** 2),
                        ((-D * dx) - (abs(dy) * math.sqrt(disc))) / (dr ** 2))
        print("yelp", retpt1, retpt2)
        retpt = ((retpt1 + retpt2) / 2) + pt
    else:
        return False
    if dist(retpt, line.p1) + dist(retpt, line.p2) <= line.l + 0.1:
        return retpt


lines = []


class Line:
    def __init__(self, p1, p2, col=(255, 255, 255)):
        self.p1 = Vector(p1[0], p1[1])
        self.p2 = Vector(p2[0], p2[1])
        self.dx = p2[0] - p1[0]
        self.dy = p2[1] - p1[1]
        self.l = dist(self.p1, self.p2)
        if self.dx != 0:
            self.m = self.dy / self.dx
            self.c = p1[1] - (self.m * p1[0])
        self.col = col
        lines.append(self)
    
    def show(self):
        pygame.draw.line(screen, self.col, tuple(self.p1), tuple(self.p2))
        

class Foot:
    def __init__(self, body, x, y, mass, col=(255, 0, 255)):
        self.body = body
        self.leg = Spring(self, self.body, 10, 0)
        self.mass = mass
        self.inv_mass = 1 / mass
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.targs = []
        self.orig = Vector(x, y)
        self.col = col
        self.stood = False
        self.cyc = 0
    
    def hurl(self, ang, reach):
        self.vel = Vector(0, 0)
        self.orig = self.pos.copy()
        self.targs.append(self.body.pos.copy())
        self.targs.append(self.body.pos + (Vector(math.cos(ang), math.sin(ang)) * reach))

    def kick(self, force):
        if not self.stood:
            self.acc = self.acc + (force * self.inv_mass)
    
    def show(self):
        if self.body.released:
            self.stood = False
            self.targs.clear()
            self.cyc = 0
        if not self.stood and self.cyc % 10 == 0:
            self.acc = self.acc + g
            self.vel = self.vel + (self.acc / 10000)
            if dist(self.pos, self.body.pos) < 25:
                self.vel *= 0.96
            self.pos = self.pos + self.vel
            self.acc = Vector(0, 0)
        if len(self.targs) > 0:
            v = (self.targs[0] - self.pos)/70
            self.cyc += 1
            self.pos = self.pos + (v * 7 * self.cyc)
            self.stood = False
            if self.cyc == 10:
                self.cyc = 0
                self.targs.pop(0)
        elif not self.stood and not self.body.released:
            for L in lines:
                touch = touchline(self.pos, L)
                if touch:
                    print(touch)
                    self.pos = touch.copy()
                    self.stood = True
                    self.orig = self.pos.copy()
                    self.targs.clear()
                    self.vel = Vector(0, 0)
                    break
        self.leg.show()
        if self.stood and self.body.released:
            print("oops")
        pygame.draw.circle(screen, self.col, (int(self.pos.x), int(self.pos.y)), 5)


class Bug:
    def __init__(self, x, y, mass, col=(255, 0, 255), footno=6):
        self.mass = mass
        self.inv_mass = 1 / mass
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.feet = [Foot(self, x, y, 0.1, col) for F in range(footno)]
        self.footindex = 0
        self.reaching = False
        self.released = False
        self.col = col
    
    def reachout(self, ang):
        if not self.reaching:
            self.feet[self.footindex].hurl(ang + math.radians(random.randrange(-3, 3)), 75)
            self.reaching = True
    
    def kick(self, force):
        self.acc += (force * self.inv_mass)
    
    def show(self):
        if self.reaching and (len(self.feet[self.footindex].targs) == 0):
            self.reaching = False
            self.footindex = (self.footindex + 1) % len(self.feet)
        self.acc += g
        self.vel += (self.acc / 10000)
        self.vel *= 0.96
        self.pos += self.vel
        self.acc = Vector(0, 0)
        for F in self.feet:
            F.show()
        pygame.draw.circle(screen, self.col, tuple(self.pos), 10)
        pygame.draw.circle(screen, self.col, (int(self.pos[0]), int(self.pos[1])), 25, 2)
        

B = Bug(w/2, h/2, 1)
Line((0, 0), (w, h))
Line((300, 0), (100, h))
Line((w/2, 200), (w, 200))

while True:
    screen.fill(0)
    for L in lines:
        L.show()
    if pygame.mouse.get_pressed()[0]:
        m = pygame.mouse.get_pos()
        B.reachout(math.atan2(m[1] - B.pos[1], m[0] - B.pos[0]))
    k = pygame.key.get_pressed()
    if k[K_SPACE]:
        B.released = True
    else:
        B.released = False
        right = k[K_RIGHT] - k[K_LEFT]
        down = k[K_DOWN] - k[K_UP]
        if right != 0 or down != 0:
            B.reachout(math.atan2(down, right))
    B.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    time.sleep(0.01)
