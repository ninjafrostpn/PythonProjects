import pygame
from pygame.locals import *
import numpy as np
from time import sleep
import glob

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

WAHPURPLE = (84, 6, 116)
wahs = [pygame.mixer.Sound(file) for file in glob.glob(r"D:\Users\Charles Turvey\Music\SFX\Waluigi\Wahs\Wah*.wav")]


wah = lambda: pygame.mixer.find_channel(True).play(wahs[np.random.randint(0, len(wahs))])


poltocart = lambda ang, length: np.float32([np.cos(np.radians(ang)), -np.sin(np.radians(ang))]) * length


class Bone:
    def __init__(self, pos, length, ang, width):
        self.startpos = np.float32(pos)
        self.offset = np.float32([0, 0])
        self.ang = ang
        self.length = length
        self.width = width
        self.endpos = poltocart(ang, length) + self.startpos
        self.attachbone = None
        self.x = poltocart(ang + 90, 1)
        self.y = poltocart(ang, 1)
    
    def attach(self, bone, offset=0):
        self.attachbone = bone
        self.attachoffset = offset
    
    def follow(self, pos):
        self.ang = -np.degrees(np.arctan2(*(pos - self.startpos)[::-1]))
    
    def show(self):
        if self.attachbone is not None:
            self.startpos = self.attachbone.endpos + self.attachoffset
        self.endpos[:] = poltocart(self.ang, self.length) + self.startpos + self.offset
        halfarmwidth = poltocart(self.ang + 90, self.width / 2)
        pygame.draw.polygon(screen, WAHPURPLE, [self.startpos + self.offset + halfarmwidth,
                                                self.startpos + self.offset - halfarmwidth,
                                                self.endpos - halfarmwidth,
                                                self.endpos + halfarmwidth])
        pygame.draw.circle(screen, WAHPURPLE, np.int32(self.startpos + self.offset), int(self.width / 2))
        

class Waluigi:
    def __init__(self, pos):
        pos = np.float32(pos)
        self.body = Bone(pos, 70, 90, 30)
        self.body.follow(mousepos)
        self.armL = Bone(pos + [10, -65], 60, 0, 10)
        self.armL.attach(self.body)
        self.armR = Bone(pos + [-10, -65], 60, 180, 10)
    
    def show(self):
        self.body.show()
        self.armL.show()
        self.armR.show()


keys = set()
mousepos = np.float32([0, 0])
W = Waluigi(screensize / 2)

while True:
    screen.fill(0)
    mousepos[:] = pygame.mouse.get_pos()
    W.body.follow(mousepos)
    W.show()
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
        elif e.type == MOUSEBUTTONDOWN:
            wah()
    sleep(0.01)
