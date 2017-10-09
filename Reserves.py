import pygame, math, random
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

textfont = pygame.font.Font("D:\\Users\\Charles Turvey\\Documents\\Python\\Projects\\Snek\\OpenSans-Regular.ttf", 30)

dist = lambda x1, y1, x2, y2: math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def arrow(surface, col, startpos, endpos):
    pygame.draw.line(surface, col, startpos, endpos)
    arrowlength = dist(startpos[0], startpos[1], endpos[0], endpos[1])
    halfxdist = (endpos[0] - startpos[0])/2
    halfydist = (endpos[1] - startpos[1])/2
    xnorm = (endpos[0] - startpos[0])/arrowlength
    ynorm = (endpos[1] - startpos[1])/arrowlength
    pointpos = (startpos[0] + halfxdist, startpos[1] + halfydist)
    leftfootpos = (startpos[0] + halfxdist + (xnorm * 10) - (ynorm * 5), startpos[1] + halfydist + (ynorm * 10) + (xnorm * 5))
    rightfootpos = (startpos[0] + halfxdist + (xnorm * 10) + (ynorm * 5), startpos[1] + halfydist + (ynorm * 10) - (xnorm * 5))
    pygame.draw.polygon(surface, col, (pointpos, leftfootpos, rightfootpos))

reserves = []

class reserve:
    def __init__(self, x, y, amount, col=(0,255,0), cap=-1, rad=50):
        self.amount = amount
        self.cap = cap
        self.col = col
        self.x = x
        self.y = y
        self.rad = rad
        reserves.append(self)

    def show(self):
        pygame.draw.circle(screen, self.col, (self.x, self.y), self.rad)
        num = textfont.render(str(self.amount), 0, (0,0,0))
        screen.blit(num, (self.x - (num.get_width()/2), self.y - (num.get_height()/2)))

processes = []

class process:
    def __init__(self, inputs, outputs, cooldown, col=(255,0,0)):
        self.inputs = inputs
        self.outputs = outputs
        self.cooldownmax = cooldown
        self.cooldown = cooldown
        self.col = col
        processes.append(self)

    def show(self):
        if self.cooldown == 0:
            if (False not in [(R.cap == -1 or R.amount < R.cap) for R in self.outputs]) and (False not in [(R.amount > 0) for R in self.inputs]):
                for R in self.inputs:
                    R.amount -= 1
                for R in self.outputs:
                    R.amount += 1
                self.cooldown = self.cooldownmax
        else:
            self.cooldown -= 1
        factor = 1 - (self.cooldown/float(self.cooldownmax))
        currcol = (self.col[0] * factor, self.col[1] * factor, self.col[2] * factor)
        midpos = ((sum([R.x for R in self.inputs]) + sum([R.x for R in self.outputs]))/(len(self.inputs) + len(self.outputs)),
                  (sum([R.y for R in self.inputs]) + sum([R.y for R in self.outputs]))/(len(self.inputs) + len(self.outputs)))
        for R in self.inputs:
            arrow(screen, currcol, (R.x, R.y), midpos)
        for R in self.outputs:
            arrow(screen, currcol, midpos, (R.x, R.y))


for i in range(0, 360, 60):
    reserve(int((w/2) + (math.cos(math.radians(i)) * 200)), int((h/2) + (math.sin(math.radians(i)) * 200)), [1, 0][constrain(i, 0, 1)], cap=10)
for i in range(len(reserves)):
    P = process([reserves[i]], [reserves[(i+1) % len(reserves)]], 3000)
    P.cooldown = i * 300

while True:
    random.shuffle(processes)
    screen.fill((0, 0, 0))
    for p in processes:
        p.show()
    for r in reserves:
        r.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()