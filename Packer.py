import pygame
from pygame.locals import *
from random import randint as rand

pygame.init()
display = pygame.display.set_mode((988, 612))
w = display.get_width()
h = display.get_height()
screen = pygame.Surface((w, h), SRCALPHA)
screen.fill((0, 0, 0, 0))
# screen.set_colorkey((255, 255, 255))

gammapath = "D:\\Users\\Charles Turvey\\Pictures\\Art\\GammaRay\\Gamma.png"
gamma = pygame.image.load_extended(gammapath)
gamma = pygame.transform.smoothscale(gamma, (int(gamma.get_width()/2), int(gamma.get_height()/2)))
gamma.convert()

def check(surf, pos):
    # print(pos)
    sw = len(surf)
    sh = len(surf[0])
    for i in range(pos[0] - 2, pos[0] + 3):
        if i >= 0 and i < sw:
            for j in range(pos[1] - 2, pos[1] + 3):
                if j >= 0 and j < sh:
                    if surf[i][j] > 0:
                        return True
    return False

while True:
    display.fill((255, 255, 255))
    screenalphas = pygame.surfarray.array_alpha(screen)
    temp = pygame.transform.rotate(gamma, rand(0, 360))
    tempalphas = pygame.surfarray.array_alpha(temp)
    # target = [[False] * temp.get_height()] * temp.get_width()  # cool way of initialising a suitable array
    # peg = [[tempalphas[x][y] > 0 for y in range(temp.get_height())] for x in range(temp.get_width())]
    tw = temp.get_width()
    th = temp.get_height()
    pos = (rand(0, w - tw), rand(0, h - th))
    okay = True
    for x in range(0, tw):
        for y in range(0, th):
            if x < w and y < h:
                if check(screenalphas, (x + pos[0], y + pos[1])) and check(tempalphas, (x, y)):
                    okay = False
    if okay:
        screen.blit(temp, pos)
    else:
        display.blit(temp, pos)
    display.blit(screen, (0, 0))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.image.save(screen, "Packed.png")
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame.image.save(screen, "Packed.png")
                exit()
