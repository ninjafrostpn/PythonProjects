import pygame
from pygame.locals import *
import numpy as np
from math import sqrt, sin, radians
from time import sleep

pygame.init()

chanmax = pygame.mixer.get_num_channels()
print("Available channels: " + str(chanmax))
channels = [pygame.mixer.Channel(i) for i in range(chanmax)]
samples = 22050/440
soundarray = []
for i in range(int(samples)):
    soundarray.append([0, int(1000 * sin(radians(i * (360/samples))))])
#channels[0].play(pygame.sndarray.make_sound(np.array(soundarray)), -1)

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

threshold = 1
distscale = 10

transmitters = []
sounds = []
receivers = []

grey = lambda val, alph=255: (val, val, val, alph)


def muteear(music, ear, reverse=False):
    musicarray = pygame.sndarray.array(music)
    musicarray[:, ear] = 0
    if reverse:
        musicarray = np.flipud(musicarray).copy('C')
    music = pygame.sndarray.make_sound(musicarray)
    return music


# Note that these are not sounds, merely pressure readings; these are parts of pressure waveforms
class sound:
    def __init__(self, id, x, y, val):
        self.id = id
        self.x = x
        self.y = y
        self.r = 0
        self.val = val
        sounds.append(self)
    
    def __del__(self):
        # print("GONE")
        pass
    
    def show(self):
        pygame.draw.circle(screen, grey(min(255, abs(self.val)/10)), (int(self.x), int(self.y)),
                           self.r, min(self.r, 1))
        self.r += 1
        currval = self.val / ((self.r / distscale) ** 2)
        if abs(currval) >= threshold:
            for R in receivers:
                d = sqrt(((R.x - self.x) ** 2 ) + ((R.y - self.y) ** 2))
                if d - R.r <= self.r <= d + R.r:
                    R.amp += currval
        else:
            sounds.remove(self)


class transmitter:
    def __init__(self, x, y):
        self.id = len(transmitters)
        self.x = x
        self.y = y
        self.amp = 0
        transmitters.append(self)
    
    def show(self):
        self.amp = 1000 * sin(radians(cycles * 300))
        sound(self.id, self.x, self.y, self.amp)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5)
        if self.amp > 0:
            pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)),
                               int(self.amp/10), min(int(self.amp/10), 1))
        elif self.amp < 0:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)),
                               int(abs(self.amp/10)), min(int(abs(self.amp/10)), 1))


class receiver:
    def __init__(self, x, y, channel, r=2):
        self.x = x
        self.y = y
        self.channel = channel
        self.r = abs(r)
        self.amp = 0
        receivers.append(self)
    
    def show(self):
        if self.channel:
            channels[0].play(pygame.sndarray.make_sound(np.array([[int(10 * self.amp), 0], ])), -1)
            #for i in range(10):
            #    soundarray.append([int(100 * self.amp), 0])
        pygame.draw.circle(screen, (255, 0, 255), (int(self.x), int(self.y)), self.r)
        if self.amp > 0:
            pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)),
                               int(self.amp), min(int(self.amp), 1))
        elif self.amp < 0:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)),
                               int(abs(self.amp)), min(int(abs(self.amp)), 1))
        self.amp = 0


#transmitter(w * 0.25, h/4)
transmitter(w * 0.75, h/4)
receiver(w * 0.25, h/2, 0)
receiver(w * 0.75, h/2, 1)

#gamemusic = pygame.mixer.Sound("Snek/Wewewewewe.wav")
#channels[0].play(muteear(gamemusic, 0, True), -1)
#channels[1].play(muteear(gamemusic, 1), -1)

cycles = 0
while True:
    screen.fill(100)
    for S in sounds:
        S.show()
    for T in transmitters:
        T.x, T.y = pygame.mouse.get_pos()
        T.show()
    for R in receivers:
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
    sleep(0.01)

channels[0].play(pygame.sndarray.make_sound(np.array(soundarray)), -1)
sleep(10)
