import pygame
from pygame.locals import *
from random import shuffle, choice, randint
from math import copysign, sin, cos, radians

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

particles = []
emptybins = [0 for i in range(10000)]
bins = emptybins.copy()


class Particle:
    def __init__(self, pos=0):
        self.pos = pos
        bins[int(self.pos % len(bins))] += 1
        particles.append(self)
    
    def show(self):
        self.pos %= len(bins)
        mheight = bins[int(self.pos)]
        ldiff = bins[int((self.pos - 1) % len(bins))] - mheight
        rdiff = bins[int((self.pos + 1) % len(bins))] - mheight
        bins[int(self.pos % len(bins))] -= 1
        if ldiff < 0 and rdiff < 0:
            self.pos += choice([-randint(0, int(abs(ldiff))),
                                 randint(0, int(abs(rdiff)))])
        else:
            self.pos += copysign(randint(0, int(abs(rdiff - ldiff))), rdiff - ldiff)
        bins[int(self.pos % len(bins))] += 1


for i in range(10000):
    Particle()

factor = 5
while True:
    #print(bins)
    screen.fill(0)
    for i in range(len(bins)):
        vali = bins[i] * factor
        i *= 360 / len(bins)
        j = int((i + 1) % len(bins))
        valj = bins[j] * factor
        j *= 360 / len(bins)
        pygame.draw.line(screen, (255, 255, 255),
                                 ((vali * cos(radians(i))) + (w/2), (vali * sin(radians(i))) + (h/2)),
                                 ((valj * cos(radians(j))) + (w/2), (valj * sin(radians(j))) + (h/2)))
    shuffle(particles)
    for p in particles:
        p.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
                