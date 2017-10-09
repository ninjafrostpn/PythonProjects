import pygame, math, time
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

dist = lambda x1, y1, x2, y2: math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))

def minmag(*terms):
    best = terms[0]
    for i in range(1, len(terms)):
        if abs(terms[i]) < abs(best):
            best = terms[i]
    return best

def checkcross(L1x1, L1y1, L1x2, L1y2, L2x1, L2y1, L2x2, L2y2):
    return True

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

walls = []

class wall:
    def __init__(self):
        pass

lights = []

class light:
    def __init__(self, x, y, intensity, col=(255, 255, 255)):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.col = col
        self.on = True
        lights.append(self)

    def rayCheck(self, pos):
        checkcross(0, 0, 0, 0, 0, 0, 0, 0)
        return True

    def show(self):
        pygame.draw.ellipse(screen, self.col, (self.x - 5, self.y - 5, 10, 10))

plants = []

class plant:
    def __init__(self, x, y, ang=90, movespeed=10.0, turnspeed=10.0):
        self.bits = [Vector(x, y)]
        self.movespeed = movespeed
        self.turnspeed = turnspeed
        self.ang = ang % 360
        plants.append(self)

    def show(self):
        targangs = []
        for light in lights:
            if light.on:
                if light.rayCheck(self.bits[-1]):
                    vec = Vector(light.x, light.y) - self.bits[-1]
                    for i in range(light.intensity):
                        targangs.append(math.degrees(math.atan2(vec.y, vec.x)) % 360)
        if len(targangs) > 0:
            targang = -sum(targangs)/len(targangs)
            diff = targang - self.ang
            self.ang += math.copysign(self.turnspeed, minmag(diff, diff + 360, diff - 360))
            #print(self.ang, targang, diff)
        self.bits.append(self.bits[-1] + Vector(math.cos(math.radians(self.ang)), -math.sin(math.radians(self.ang))) * self.movespeed)
        #start = self.bits[-2]
        #end = self.bits[-1]
        #pygame.draw.line(screen, (0, 255, 0), (start.x, start.y), (end.x, end.y))
        for i in range(len(self.bits) - 1):
            start = self.bits[i]
            end = self.bits[i+1]
            pygame.draw.line(screen, (0,255,0), (start.x, start.y), (end.x, end.y))

for i in range(1, 11):
    plant((w/12) * i, h, 100, 0.3, 1)
L = light(w/2, h/2, 8)

cycles = 0
while True:
    screen.fill((0, 0, 0))
    L.x = (w/2) + ((w/1.5) * math.cos(math.radians(cycles)))
    L.y = h - ((h/1.5) * math.sin(math.radians(cycles)))
    if L.x < 0 or L.x > w or L.y > h:
        L.on = False
    else:
        L.on = True
    for l in lights:
        l.show()
    for p in plants:
        p.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
    cycles += 1
    time.sleep(0.1)
