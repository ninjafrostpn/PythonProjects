import pygame, math, time
from random import randint as rand
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500))

n = 10
skip = 0
clockwise = True
mode = 0

class Mouse:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col
        self.nextx = -1
        self. nexty = -1

    def update(self, x, y):
        self.nextx = self.x + (x - self.x)/10
        self.nexty = self.y + (y - self.y)/10

    def show(self):
        pygame.draw.line(screen, self.col, (round(self.x), round(self.y)), (round(self.nextx), round(self.nexty)))
        self.x = self.nextx
        self.y = self.nexty

modeset = {K_0: 0, K_1: 1, K_2: 2}
inc = 360/n
cx = screen.get_width()/2
cy = screen.get_height()/2

startup = True
while True:
    if startup == True:
        screen.fill((255, 255, 255))
        mice = []
        for i in range(n):
            col = (i*(255/n), (n-i)*(255/n), 0)
            if mode == 0:
                r = min(cx, cy)
                mice.append(
                    Mouse(cx + (r * math.cos(math.radians(inc * i))), cy + (r * math.sin(math.radians(inc * i))), col))
            elif mode == 1:
                r = rand(0, min(cx, cy))
                mice.append(
                    Mouse(cx + (r * math.cos(math.radians(inc * i))), cy + (r * math.sin(math.radians(inc * i))), col))
            elif mode == 2:
                mice.append(Mouse(rand(0, cx * 2), rand(0, cy * 2), col))
        startup = False
        if clockwise:
            mice.reverse()
    for i in range(len(mice)):
        M2 = mice[(i + 1 + skip) % len(mice)]
        mice[i].update(M2.x, M2.y)
    for M in mice:
        M.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
            elif e.key in modeset.keys():
                mode = modeset[e.key]
                startup = True
            elif e.key == K_SPACE:
                clockwise = not clockwise
                startup = True
    time.sleep(0.03)