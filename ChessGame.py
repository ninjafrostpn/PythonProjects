import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

piecenames = ["", "B", "N", "R", "Q", "K"]


class Piece:
    def __init__(self, type="", colour="w"):
        pass
    
    def moves(self):
    

boardarray = np.zeros((8, 8), "int32")

keys = set()

while True:
    screen.fill(0)
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
    sleep(0.001)
