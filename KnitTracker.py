import pygame
from pygame.locals import *
import numpy as np
import time
import random

pygame.init()

w, h = 1200, 400
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("You got this :)")
screensize = np.int32((w, h))

bigfont = pygame.font.Font(None, 250)
smlfont = pygame.font.Font(None, 50)

keys = set()

stitchnames = {"k": "KNIT",
               "p": "PURL",
               "b": "KNIT BELOW"}
stitchcolours = {"k": (100, 200, 100),
                 "p": (100, 100, 200),
                 "b": (0, 200, 255)}

stitches = 120
ontheround = False
pattern = "kb"

stitch = 0
round = 0
while True:
    screen.fill(0)
    stitchcode = pattern[stitch % len(pattern)]
    command = bigfont.render(stitchnames[stitchcode],
                             True, stitchcolours[stitchcode])
    screen.blit(command, (10, 10))
    readout = smlfont.render("Stitch {}/{} ({} completed) of round {}".format((stitch % stitches) + 1, stitches,
                                                                              stitch, round),
                             True, (255, 255, 255))
    screen.blit(readout, (10, 360))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
            if e.key == K_SPACE:
                stitch += 1
                if stitch % stitches == 0:
                    round += 1
            if e.key == K_BACKSPACE:
                stitch -= 1
                if stitch == 0:
                    round -= 1
        elif e.type == KEYUP:
            keys.discard(e.key)
    time.sleep(0.1)
