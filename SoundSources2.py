import pygame
from pygame.locals import *
import numpy as np
from math import sqrt, sin, cos, radians, pi

pygame.init()

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()
diag = sqrt(w**2 + h**2)

HALF_PI = pi/2

# samples = int(22050/1000)
# gamesoundarray = []
# for i in range(samples):
#     val = int(10000 * sin(radians(i * (360/samples))))
#     gamesoundarray.append([val, val])
# gamesound = pygame.sndarray.make_sound(np.array(gamesoundarray))

gamesound = pygame.mixer.Sound("Snek/Wewewewewe.wav")

channels = [pygame.mixer.Channel(i) for i in range(pygame.mixer.get_num_channels())]
transmitters = []
receivers = []

grey = lambda val, alph=255: (val, val, val, alph)


def muteear(music, ear):
    musicarray = pygame.sndarray.array(music)
    musicarray[:, ear] = 0
    # print(musicarray)
    music = pygame.sndarray.make_sound(musicarray)
    return music


class transmitter:
    def __init__(self, x, y):
        self.id = len(transmitters)
        self.x = x
        self.y = y
        self.amp = 0
        self.channels = [[] for i in receivers]
        self.play(gamesound)
        transmitters.append(self)
    
    def play(self, sound):
        for i, R in enumerate(receivers):
            chan = channels.pop(0)
            # print(chan)
            editedsound = muteear(sound, (R.ear + 1) % 2)
            chan.play(editedsound, -1)
            self.channels[i].append(chan)
    
    def show(self):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5)
        for i, R in enumerate(receivers):
            d = sqrt(((R.x - self.x) ** 2) + ((R.y - self.y) ** 2)) + 1
            for chan in self.channels[i]:
                chan.set_volume(diag/(d ** 2))


class receiver:
    def __init__(self, x, y, ear, r=2):
        self.id = len(receivers)
        self.x = x
        self.y = y
        self.ear = ear
        self.r = abs(r)
        receivers.append(self)
    
    def show(self):
        pygame.draw.circle(screen, (255, 0, 255), (int(self.x), int(self.y)), self.r)


receiver(w/2, h/2, 0)
receiver(w/2, h/2, 1)
# Must make transmitters second
transmitter(w * 0.75, h/4)

cycles = 0
headx = w/2
heady = h/2
headang = 0

speed = 0.05
turnspeed = 0.2
while True:
    screen.fill(100)
    for T in transmitters:
        T.show()
    pressed = pygame.key.get_pressed()
    if pressed[K_RIGHT]:
        headang += turnspeed
    if pressed[K_LEFT]:
        headang -= turnspeed
    currang = radians(headang)
    if pressed[K_UP]:
        headx += speed * cos(currang - HALF_PI)
        heady += speed * sin(currang - HALF_PI)
    if pressed[K_DOWN]:
        headx -= speed * cos(currang - HALF_PI)
        heady -= speed * sin(currang - HALF_PI)
    for i, R in enumerate(receivers):
        side = ((2 * i) - 1)
        R.x = headx + (10 * cos(currang) * side)
        R.y = heady + (10 * sin(currang) * side)
        R.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    cycles += 1
    #transmitters[0].x = w/2 * (1 + sin(radians(0.5 * cycles)))
