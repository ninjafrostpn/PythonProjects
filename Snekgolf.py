import pygame
from pygame.locals import *

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

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


class InvalidOperation(Exception):
    pass


class InvalidIndex(Exception):
    pass


class snek:
    def __init__(self):
        self.coords = [Vector(w/2, h/2)]

    def

while True:
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()