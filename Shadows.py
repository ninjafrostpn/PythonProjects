import pygame
from pygame.locals import *
import cv2.cv2 as cv2

pygame.init()
screen = pygame.display.set_mode((1000, 500))
w = screen.get_width()
h = screen.get_height()


class backdrop:
    def __init__(self):
        pass


class light:
    def __init__(self, pos):
        pass


class silhouette:
    def __init__(self, points):
        self.points = points
        

while True:
    screen.fill(0)
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    pygame.display.flip()
