import pygame
from pygame.locals import *
import math
import numpy as np
import time

pygame.init()
screen = pygame.display.set_mode((988, 612))
w = screen.get_width()
h = screen.get_height()

fury = pygame.mixer.Sound("D:\\Users\\Charles Turvey\\Music\\SFX\\Others from Mario\\malpit_fawful_FURY.wav")

chanmax = pygame.mixer.get_num_channels()
print(chanmax)
channels = [pygame.mixer.Channel(i) for i in range(chanmax)]

notefreq = lambda note: pow(2, note/12) * 440

def singen(freq, amp, dur=100, ear=3):
    sinusoid = []
    samples = math.floor(22050/freq)
    for i in range(dur):
        for j in range(samples):
            theta = math.radians(j * (360/samples))
            if ear >= 2:
                sinusoid.append(int(amp*math.sin(theta)))
            else:
                sinusoid.append(0)
            if ear % 2 != 0:
                sinusoid.append(int(amp*math.sin(theta)))
            else:
                sinusoid.append(0)
    sinusoid = np.array(sinusoid).reshape(dur * samples, 2)
    # print(sinusoid)
    return pygame.sndarray.make_sound(sinusoid)

chords = dict()
chords["maj"] = [0, 4, 7]
chords["min"] = [0, 3, 7]
chords["dim"] = [0, 3, 6]

def playchord(start, type):
    notes = []
    for i in chords[type]:
        notes.append(singen(notefreq(start + i), 100))
    for i in range(len(notes)):
        channels[i].play(notes[i], -1)

noteL = singen(392, 100, ear=2)
noteR = singen(587.33, 100, ear=1)

side = 0
high = 0

while True:
    playchord(int(pygame.mouse.get_pos()[0]/100), "dim")
    #channels[int(high/2 % 8)].play(singen(notefreq(high), 100), -1)
    #high += 2
    """
    if pygame.mouse.get_pos()[0] >= w/2 and side == 0:
        channels[0].play(noteR, -1)
        side = 1
    elif pygame.mouse.get_pos()[0] < w/2 and side == 1:
        channels[1].play(noteL, -1)
        side = 0
    """
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
    time.sleep(1)
