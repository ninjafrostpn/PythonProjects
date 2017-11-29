import pygame, math, time, random
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

dist = lambda x1, y1, x2, y2: math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))

def bestang(targang, currang):
    diff = targang - currang
    diffs = [diff, diff + (math.pi * 2), diff - (math.pi * 2)]
    best = diffs[0]
    for i in range(1, len(diffs)):
        if abs(diffs[i]) < abs(best):
            best = diffs[i]
    return best

def intriangle(point, corner1, corner2, corner3):
    # If the point is outside the triangle, the sum of the shortest differences from one corner to the next in
    # the same direction have one negative, winding up with them cancelling to get 0
    # inside, they add to get 360
    point = Vector(point[0], point[1])
    corner1 = Vector(corner1[0], corner1[1])
    corner2 = Vector(corner2[0], corner2[1])
    corner3 = Vector(corner3[0], corner3[1])
    vec1 = corner1 - point
    vec2 = corner2 - point
    vec3 = corner3 - point
    ang1 = math.atan2(vec1.y, vec1.x)
    ang2 = math.atan2(vec2.y, vec2.x)
    ang3 = math.atan2(vec3.y, vec3.x)
    total = bestang(ang1, ang2) + bestang(ang2, ang3) + bestang(ang3, ang1)
    return math.degrees(total) == 360

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

    def __len__(self):
        return 2

    def norm(self):
        if abs(self) == 0:
            return Vector(0, 0)
        else:
            return self / abs(self)

pins = []

class pin:
    def __init__(self, pos, col=(255,255,255)):
        self.pos = Vector(pos[0], pos[1])
        self.col = col
        pins.append(self)

    def show(self):
        pygame.draw.circle(screen, self.col, self.pos, 1)

ropes = []

class Rope:
    def __init__(self, start, maxlength=1000, col=(0,255,0)):
        self.corners = [Vector(start[0], start[1])]
        self.lengths = []
        self.maxlength = maxlength
        self.entryangs = []
        self.entrydirs = []
        self.col = col
        self.prevtarget = self.corners[0]
        ropes.append(self)

    def show(self, target):
        target = Vector(target[0], target[1])
        if abs(target - self.corners[-1]) + sum(self.lengths) > self.maxlength:
            target = ((target - self.corners[-1]).norm() * (self.maxlength - sum(self.lengths))) + self.corners[-1]
        collisions = []
        colldirs = []
        for p in pins:
            if not p.pos == self.corners[-1]:
                if intriangle(p.pos, self.corners[-1], self.prevtarget, target):
                    colldirs.append(-1)
                    collisions.append(p)
                elif intriangle(p.pos, self.corners[-1], target, self.prevtarget):
                    colldirs.append(1)
                    collisions.append(p)
        if len(collisions) > 0:
            closest = w*2
            index = -1
            for i in range(len(collisions)):
                c = collisions[i]
                cdist = abs(c.pos - self.corners[-1])
                if closest >= cdist:
                    index = i
                    closest = cdist
            if index != -1:
                self.addcorner(collisions[index].pos, colldirs[index])
        for i in range(len(self.corners)):
            start = self.corners[i]
            if i == len(self.corners) - 1:
                end = target
            else:
                end = self.corners[i + 1]
            pygame.draw.line(screen, self.col, (start.x, start.y), (end.x, end.y))
        self.prevtarget = target

    def addcorner(self, pos, entrydir):
        self.corners.append(Vector(pos[0], pos[1]))
        self.lengths.append(abs(self.corners[-1] - self.corners[-2]))
        vec = self.corners[-1] - self.corners[-2]
        self.entryangs.append(math.atan2(vec.y, vec.x))
        self.entrydirs.append(entrydir)

ROP1 = Rope((random.randint(0, w), random.randint(0, h)))
for i in range(100):
    pin((random.randint(0, w), random.randint(0, h)))

while True:
    screen.fill((0, 0, 0))
    mpos = pygame.mouse.get_pos()
    for p in pins:
        p.show()
    for r in ropes:
        r.show(mpos)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
            elif e.key == K_UP:
                ROP1.maxlength += 10
            elif e.key == K_DOWN and ROP1.maxlength >= 10:
                ROP1.maxlength -= 10
                