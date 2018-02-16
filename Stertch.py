import pygame, math
from pygame.locals import *
pygame.init()

mode = 0

if mode == 0:
    screen = pygame.display.set_mode((500, 500))
elif mode == 1:
    screen = pygame.display.set_mode((60, 500))
w = screen.get_width()
h = screen.get_height()

white = (255, 255, 255)
black = (0, 0, 0)

dist = lambda x1, y1, x2, y2: math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))


class InvalidOperation(Exception):
    pass


class InvalidIndex(Exception):
    pass


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return dist(0, 0, self.x, self.y)

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

    def norm(self):
        if abs(self) == 0:
            return Vector(0, 0)
        else:
            return self / abs(self)

g = Vector(0, 9.8)

class Mass:
    def __init__(self, x, y, mass, radius=10, restitution=0.9, friction=0.1, col=white):
        self.mass = mass
        self.inv_mass = 1/mass
        self.r = radius
        self.col = col
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.res = restitution
        self.fric = friction

    def show(self, fixed=False):
        self.acc = self.acc + g
        if not fixed:
            self.vel = self.vel + (self.acc / 10000)
            self.pos = self.pos + self.vel
        else:
            self.pos = Vector(mpos[0], mpos[1])
            self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        if self.pos.y > h:
            self.vel.y *= -self.res
            self.vel.x *= (1 - self.fric)
            self.pos.y = h - (self.pos.y - h)
        if self.pos.x < 0:
            self.vel.x *= -self.res
            self.vel.y *= (1 - self.fric)
            self.pos.x *= -1
        if self.pos.x > w:
            self.vel.x *= -self.res
            self.vel.y *= (1 - self.fric)
            self.pos.x = w - (self.pos.x - w)
        # print(self.pos[1], self.vel[1], self.acc[1])
        pygame.draw.circle(screen, self.col, tuple(self.pos), self.r)

    def kick(self, force):
        self.acc = self.acc + (force * self.inv_mass)


class DummyMass:
    def __init__(self, x, y, mass=0):
        self.pos = Vector(x, y)

    def show(self, fixed=False):
        pass

    def kick(self, force):
        pass


class Spring:
    def __init__(self, end1, end2, spring_constant, length=-1, col=white):
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
        # print(fact)
        self.end1.kick((self.end1.pos - self.end2.pos).norm() * fact)
        self.end2.kick((self.end2.pos - self.end1.pos).norm() * fact)
        pygame.draw.line(screen, self.col, tuple(self.end1.pos), tuple(self.end2.pos))

if mode == 0:
    leftside = [Mass(w/2 - 50, h - (20 * i), 1) for i in range(10)]
    leftside.insert(0, DummyMass(w/2 - 50, h))
    rightside = [Mass(w/2 + 50, h - (20 * i), 1) for i in range(10)]
    rightside.insert(0, DummyMass(w/2 + 50, h))
    springs = []
    strongth = 1000
    for i in range(11):
        if i != 0:
            springs.append(Spring(leftside[i], rightside[i], strongth))
        if i != 10:
            springs.append(Spring(leftside[i], rightside[i + 1], strongth))
            springs.append(Spring(leftside[i], leftside[i + 1], strongth))
            springs.append(Spring(leftside[i + 1], rightside[i], strongth))
            springs.append(Spring(rightside[i], rightside[i + 1], strongth))
    M = Mass(w/2, h - 200, 1)
    springs.append(Spring(M, leftside[-1], 1))
    springs.append(Spring(M, rightside[-1], 1))
    rinc = 0
    linc = 0
elif mode == 1:
    strongth = 1000
    nodes = []
    for i in range(4):
        nodes.append(Mass(0, h + 150 - (i * 50), 1, restitution=0.1, friction=0.9))
        nodes.append(Mass(50, h + 150 - (i * 50), 1, restitution=0.1, friction=0.9))
    acrosprings = [Spring(nodes[i], nodes[i+1], strongth) for i in range(0, 8, 2)]
    downsprings = [Spring(nodes[i], nodes[i+2], strongth) for i in range(6)]
    diagsprings = [Spring(nodes[i], nodes[i+3], strongth) for i in range(0, 6, 2)] \
                  + [Spring(nodes[i], nodes[i+1], strongth) for i in range(1, 6, 2)]
    cycles = 0

fixit = False
mpos = pygame.mouse.get_pos()

while True:
    prevpos = mpos
    mpos = pygame.mouse.get_pos()
    mvel = (mpos[0] - prevpos[0], mpos[1] - prevpos[1])
    screen.fill(black)
    if mode == 0:
        for s in springs:
            if s.end1 in leftside and s.end2 in leftside:
                s.l += linc
            elif s.end1 in rightside and s.end2 in rightside:
                s.l += rinc
            elif s.end1 in leftside and s.end2 in rightside:
                if leftside.index(s.end1) == rightside.index(s.end2):
                    s.l += (pygame.mouse.get_pos()[1] < h/2)/10
            s.show()
        for i in range(11):
            leftside[i].show()
            rightside[i].show()
        M.show(fixit)
    elif mode == 1:
        for i in range(len(acrosprings)):
            acrosprings[i].l = 50 + math.copysign(10, math.sin(math.radians(cycles + (i * 180))))
            acrosprings[i].show()
        for i in range(0, len(downsprings), 2):
            downsprings[i].l = 50 + math.copysign(10, math.sin(math.radians(cycles + 90 + (i * 180))))
            downsprings[i+1].l = 50 + math.copysign(10, math.sin(math.radians(cycles + 90 +  (i * 180))))
            downsprings[i].show()
            downsprings[i+1].show()
        for i in range(len(diagsprings)):
            diagsprings[i].show()
        for n in nodes:
            n.show()
        cycles += 1
    pygame.display.flip()
    if mode == 0:
        linc = 0
        rinc = 0
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
            if mode== 0:
                if e.key == K_q:
                    linc = 1
                elif e.key == K_a:
                    linc = -1
                if e.key == K_e:
                    rinc = 1
                elif e.key == K_d:
                    rinc = -1
        elif e.type == MOUSEBUTTONDOWN:
            fixit = True
        elif e.type == MOUSEBUTTONUP:
            fixit = False
