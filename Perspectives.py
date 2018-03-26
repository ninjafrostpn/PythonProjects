import pygame
from pygame.locals import *
import cv2.cv2 as cv2

pygame.init()
screen = pygame.display.set_mode((1000, 500))
w = screen.get_width()
h = screen.get_height()

while True:
    screen.fill(0)
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    pygame.display.flip()
