from math import atan2, sin, cos, pi
import numpy as np
import pygame
from pygame.locals import *


def disintegrate(source, rect, dirang, fragsize, throwdist, resample=True):
    print("I don't feel so good...")
    if not resample:
        orig = pygame.surfarray.array3d(source)
    curr = pygame.surfarray.pixels3d(source)
    angx = np.float32([cos(dirang - scatterang / 2), sin(dirang - scatterang / 2)])
    angy = np.float32([cos(dirang + scatterang / 2), sin(dirang + scatterang / 2)])
    for i in range(int(np.prod(rect.size) / (2 * (fragsize ** 2)))):
        pos = np.int32([np.random.randint(rect.left, rect.right - fragsize),
                        np.random.randint(rect.top, rect.bottom - fragsize)])
        newpos = pos + np.int32((angx * np.random.random() + angy * np.random.random()) * throwdist)
        if resample:
            frag = curr[pos[0]:pos[0] + fragsize, pos[1]:pos[1] + fragsize].copy()
            newfrag = curr[newpos[0]:newpos[0] + fragsize, newpos[1]:newpos[1] + fragsize].copy()
        else:
            frag = orig[pos[0]:pos[0] + fragsize, pos[1]:pos[1] + fragsize].copy()
            newfrag = orig[newpos[0]:newpos[0] + fragsize, newpos[1]:newpos[1] + fragsize].copy()
        curr[pos[0]:pos[0] + fragsize, pos[1]:pos[1] + fragsize] = newfrag
        curr[newpos[0]:newpos[0] + fragsize, newpos[1]:newpos[1] + fragsize] = frag


MAGENTA = (255, 0, 255)

img = pygame.image.load(r"D:\Users\Charles Turvey\Pictures\Art\Wah\Waluigi-Sized-1.jpg")
scalefactor = 1
w = int(img.get_width() / scalefactor)
h = int(img.get_height() / scalefactor)
img = pygame.transform.scale(img, (w, h))
screen = pygame.display.set_mode((w, h))
img = img.convert()

selecting = False
areastart = 0
areaend = 0
selectrect = 0

angselecting = False
ang = 0

scatterang = pi/2

while True:
    screen.fill(0)
    screen.blit(img, (0, 0))
    if selecting:
        pygame.draw.rect(screen, MAGENTA, (*areastart, *(np.float32(pygame.mouse.get_pos()) - areastart)), 1)
    elif angselecting:
        pygame.draw.rect(screen, MAGENTA, selectrect, 1)
        pygame.draw.line(screen, MAGENTA, selectrect.center, pygame.mouse.get_pos())
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
        elif e.type == MOUSEBUTTONDOWN:
            if not selecting and not angselecting:
                selecting = True
                areastart = np.float32(pygame.mouse.get_pos())
                areaend = np.float32(pygame.mouse.get_pos())
        elif e.type == MOUSEBUTTONUP:
            if selecting:
                areaend = np.float32(pygame.mouse.get_pos())
                selectrect = pygame.Rect(*areastart, *(areaend - areastart))
                selectrect.normalize()
                selecting = False
                angselecting = True
            elif angselecting:
                pointer = np.float32(pygame.mouse.get_pos()) - np.float32(selectrect.center)
                ang = atan2(*pointer[::-1])
                angselecting = False
                disintegrate(img, selectrect, ang, 3, np.linalg.norm(pointer))
