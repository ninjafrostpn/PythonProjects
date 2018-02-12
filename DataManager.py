from math import sqrt, sin, cos, pi  # only sqrt required
import pygame
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()


def dist(x1, y1, x2, y2):
    return sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


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
    
    def __str__(self):
        return "Vector({}, {})".format(self.x, self.y)
    
    def norm(self):
        if abs(self) == 0:
            return Vector(0, 0)
        else:
            return self / abs(self)
        

conglomerates = []
alltags = set()
allheadings = set()


class Conglomerate:
    def __init__(self, data={}, tags=[]):
        self.data = data
        self.headings = set(data.keys())
        allheadings.update(data.keys())
        self.tags = set(tags)
        alltags.update(tags)
        conglomerates.append(self)
        self.pos = Vector(0, 0)
        self.targ = Vector(0, 0)
        self.moving = 0
    
    def show(self, xheading, yheading, yestags=[], notags=[], speed=1):
        headingspresent = self.headings >= {xheading, yheading}  # tests if subset of headings
        yestagspresent = self.tags >= set(yestags)
        notagsabsent = not (self.tags >= set(notags) and len(notags) > 0)
        # print(headingspresent, yestagspresent, notagsabsent)
        if headingspresent and yestagspresent and notagsabsent:
            self.targ = Vector(self.data[xheading], h - self.data[yheading])
            if self.pos != self.targ and self.moving == 0:
                self.moving = 100
        else:
            self.moving = -100
        if self.moving > 0:
            self.pos += (self.targ - self.pos).norm()
        elif self.moving < 0:
            pass
        if abs(self.targ - self.pos) < speed:
            self.pos = Vector(self.targ.x, self.targ.y)
            # print(list(self.targ), list(self.pos))
            self.moving = 0
        pygame.draw.circle(screen, (255, 255, 255), list(self.pos), 2)
    
mode = 1

if mode == 0:
    curxheading = K_1
    curyheading = K_8
    n = range(0, 360, 1)
    alldata = {K_1: [i for i in n],
               K_2: [1.1 * i for i in n],
               K_3: [3 * i for i in n],
               K_4: [sqrt(i) for i in n],
               K_5: [250 + 50 * cos(i * (pi/180)) for i in n],
               K_6: [250 + 100 * cos(i * (pi/180)) for i in n],
               K_7: [250 + 100 * cos(2 * i * (pi/180)) for i in n],
               K_8: [250 + 50 * sin(i * (pi/180)) for i in n],
               K_9: [250 + 100 * sin(i * (pi/180)) for i in n],
               K_0: [250 + 100 * sin(2 * i * (pi/180)) for i in n]}
elif mode == 0:
    imag = pygame.image.load_extended("D:\\Users\\Charles Turvey\\Pictures\\New folder\\Untitled.png")
    imagpix = pygame.PixelArray(imag)
    picx = []
    picy = []
    for i in range(imag.get_width()):
        for j in range(imag.get_height()):
            if imagpix[i, j] == imag.map_rgb((0, 0, 0)):
                picx.append(i)
                picy.append(j)
    curxheading = K_x
    curyheading = K_y
    alldata = {K_x: picx,
               K_y: picy,
               K_0: [h for i in range(len(picx))]}
    n = picx

for i in range(len(n)):
    datain = {}
    for j in list(alldata.keys()):
        datain[j] = alldata[j][i]
    Conglomerate(datain)

axis = 0
while True:
    screen.fill(0)
    for c in conglomerates:
        c.show(curxheading, curyheading)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
            elif e.key in list(alldata.keys()):
                if axis == 0:
                    curxheading = e.key
                else:
                    curyheading = e.key
            elif e.key == K_SPACE:
                axis = 1
        elif e.type == KEYUP:
            if e.key == K_SPACE:
                axis = 0
