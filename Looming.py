import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500))
infx = screen.get_width()/2
infy = screen.get_height() * (2/3)
infz = 500

dragon = pygame.image.load_extended("D:\\Users\\Charles Turvey\\Documents\\Python\\DRAGON.png")
#dragon = pygame.transform.scale(dragon, (40 * int(dragon.get_width() / dragon.get_height()), 40))
dragon.set_colorkey((255, 255, 255))
dragon.convert()

def ztrans(coords):
    zc = 1 - (coords[2]/infz)
    return (((coords[0] - infx) * zc) + infx, ((coords[1] - infy) * zc) + infy)

def zscale(no, z):
    zc = 1 - (z/infz)
    return no * zc

class cutout:
    def __init__(self, image, coords=(0, 0, 0)):
        self.image = image
        self.coords = list(coords)

    def show(self):
        w = int(zscale(self.image.get_width(), self.coords[2]))
        h = int(zscale(self.image.get_height(), self.coords[2]))
        cent = ztrans(self.coords)
        curimage = pygame.transform.scale(self.image, (w, h))
        screen.blit(curimage, (cent[0] - curimage.get_width()/2, cent[1] - curimage.get_height()/2))

dragon = cutout(dragon, (500, 250, 0))

while True:
    screen.fill(100)
    dragon.coords[2] = pygame.mouse.get_pos()[0]
    dragon.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()

