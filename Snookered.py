import numpy as np
import pygame
from pygame.locals import *
from time import sleep

WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
gravity = np.float32((0, 2))

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

balls = []


class Ball:
    def __init__(self, pos, radius, mass, restitution=1.0, col=WHITE):
        self.pos = np.float32(pos)
        self.vel = np.float32((0, 0))
        self.acc = np.float32((0, 0))
        self.r = radius
        self.restitution = restitution
        self.col = col
        if mass > 0:
            self.invmass = 1/mass
        else:
            self.invmass = 0
        balls.append(self)
    
    def collide(self, other):
        normal = other.pos - self.pos
        dist = np.linalg.norm(normal)
        if dist <= other.r + self.r:
            relvel = other.vel - self.vel
            normal /= dist
            normvel = np.dot(relvel, normal)
            if normvel <= 0:
                e = min(other.restitution, self.restitution)
                j = -((1 + e) * normvel) / (other.invmass + self.invmass)
                impulse = j * normal
                self.acc -= self.invmass * impulse
                other.acc += other.invmass * impulse
    
    def show(self):
        self.acc += gravity
        for B in balls:
            if B != self:
                self.collide(B)
        self.vel += self.acc
        self.pos += self.vel
        self.acc = np.float32((0, 0))
        if 0 > self.pos[0] or w < self.pos[0]:
            self.vel[0] *= -self.restitution
            self.pos[0] = w - (self.pos[0] % w)
        if 0 > self.pos[1] or h < self.pos[1]:
            self.vel[1] *= -self.restitution
            self.pos[1] = h - (self.pos[1] % h)
        pygame.draw.circle(screen, self.col, self.pos, self.r)


Ball((0, 0), 10, 1)
Ball((10, h), 10, 0.5, 0.1, col=MAGENTA)

while True:
    screen.fill(0)
    for ball in balls:
        ball.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    sleep(0.05)
