import pygame, math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1200,500))

def constrain(val, lo, hi):
    # Because these things are useful :)
    if val <= lo:
        return lo
    elif val >= hi:
        return hi
    else:
        return val

def func(x,y):
    if x >= w or x < 0 or y >= h or y < 0:
        return 0
    else:
        screenarr = pygame.surfarray.pixels_blue(bckgrd)
        return (255 - screenarr[int(x)][int(y)])/200

grey = lambda val: (val, val, val)

w = screen.get_width()
h = screen.get_height()
bckgrd = pygame.Surface((w, h))
pygame.draw.ellipse(bckgrd, grey(200), (w*0.4, 0, w*0.2, h))

class wavefront:
    def __init__(self, x, y, ang, width=100):
        self.x = x
        self.y = y
        self.ang = ang
        self.width = width
        self.sprite = pygame.Surface((10, width/2))
        self.sprite.set_colorkey(grey(0))  # so that, after rotation and blitting to screen, padding is transparent
        self.sprite = self.sprite.convert()  # makes the sprite the same format as the screen, making blitting faster
        self.sprite.fill(grey(255))

    def move(self):
        # x and y components of the forwards and sideways directions
        forx = math.cos(self.ang - (math.pi / 2))
        fory = -math.sin(self.ang - (math.pi / 2))
        sidex = math.cos(self.ang)
        sidey = -math.sin(self.ang)
        L = func(self.x + sidex, self.y + sidey)
        R = func(self.x - sidex, self.y - sidey)
        if L == R:
            # prevents nasty zero-division errors when trying to drive in a straight line :)
            self.x = constrain(self.x + R*math.cos(self.ang), 0, w)
            self.y = constrain(self.y - R*math.sin(self.ang), 0, h)
        else:
            # interior radius of turn and angle passed through
            r = (L*self.width)/(R-L)
            theta = (R-L)/self.width
            # movements relative to itself
            relx = ((2*r) + self.width)*math.sin(theta)/2
            rely = ((2*r) + self.width)*(1 - math.cos(theta))/2
            # movements in reference frame of arena
            xmov = (relx * sidex) + (rely * forx)
            ymov = (relx * sidey) + (rely * fory)
            # actually moving the bot5
            self.x = self.x + xmov/10
            self.y = self.y - ymov/10
            self.ang -= theta

    def show(self):
        if self.x > w or self.x < 0 or self.y > h or self.y < 0:
            wavefronts.remove(self)
        else:
            self.move()
            cursprite = pygame.transform.rotate(self.sprite, -math.degrees(self.ang))
            screen.blit(cursprite, (self.x - (cursprite.get_width() / 2), self.y - (cursprite.get_height() / 2)))

wavefronts = []  # [wavefront(w/2, h/2, i) for i in range(10)]

cycles = 0
while True:
    if cycles == 0:
        pos = pygame.mouse.get_pos()
        wavefronts.append(wavefront(pos[0], pos[1], 0))
    cycles = (cycles + 1) % 100
    screen.blit(bckgrd, (0,0))
    for wave in wavefronts:
        wave.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
