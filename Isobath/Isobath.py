import pygame, math
from pygame.locals import *
pygame.init()
from random import randrange as rand

dist = lambda x1, y1, x2, y2: math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))

screen = pygame.display.set_mode((800, 500))
w = screen.get_width()
h = screen.get_height()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0,0)

class datum:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def show(self):
        pygame.draw.ellipse(screen, red, (self.x - 5, self.y - 5, 1, 1))

gridwidth = 5
data = []
for i in range(gridwidth * 2, w - gridwidth, gridwidth):
    for j in range(gridwidth * 2, h - gridwidth, gridwidth):
        s = dist(i, j, w/2, h/2)
        data.append(datum(i, j, math.exp((s + i/2)/200)))
data.sort(key=lambda d: d.z)
maxz = max([data[i].z for i in range(len(data))])
# print(data)

intervalwidth = 1
pointintervals = []
i = 0
j = 0
while i < maxz:
    interval = []
    while i <= data[j].z < i + intervalwidth:
        # print(j)
        interval.append(data[j])
        j += 1
        if j == len(data):
            break
    pointintervals.append(interval)
    i += intervalwidth
# print([[pointintervals[i][j].z for j in range(len(pointintervals[i]))] for i in range(len(pointintervals))])

i = -1
while len(pointintervals[i]) == 0:
    i -= 1
centx = sum([d.x for d in pointintervals[i]]) / len(pointintervals[i])
centy = sum([d.y for d in pointintervals[i]]) / len(pointintervals[i])

isobathintervals = []
for i in range(len(pointintervals) - 1):
    interval = []
    thisz = (i+1) * intervalwidth
    if len(pointintervals[i]) != 0:
        centx = sum([d.x for d in pointintervals[i]]) / len(pointintervals[i])
        centy = sum([d.y for d in pointintervals[i]]) / len(pointintervals[i])
    for p1 in pointintervals[i]:
        for p2 in pointintervals[i+1]:
            if -5 < (math.degrees(math.atan2(p1.y - centy, p1.x - centx) - math.atan2(p2.y - centy, p2.x - centx))) % 360 < 5:
                factor = (thisz - p1.z)/(p2.z - p1.z)
                xpos = p1.x + ((p2.x - p1.x) * factor)
                ypos = p1.y + ((p2.y - p1.y) * factor)
                interval.append(datum(xpos, ypos, thisz))
    isobathintervals.append(interval)

for i in range(len(isobathintervals)):
    isobathintervals[i].sort(key=lambda p: math.atan2(p.y - centy, p.x - centx))

screen.fill(black)
i = 0
while len(isobathintervals[i]) == 0:
    i -= 1
centx = sum([d.x for d in isobathintervals[i]]) / len(isobathintervals[i])
centy = sum([d.y for d in isobathintervals[i]]) / len(isobathintervals[i])
for i in range(len(isobathintervals)):
    if len(isobathintervals[i]) != 0:
        centx = sum([d.x for d in isobathintervals[i]]) / len(isobathintervals[i])
        centy = sum([d.y for d in isobathintervals[i]]) / len(isobathintervals[i])
    for j in range(len(isobathintervals[i])):
        p1 = isobathintervals[i][j]
        p2 = isobathintervals[i][(j+1) % len(isobathintervals[i])]
        if dist(centx, centy, p1.x, p1.y) + dist(centx, centy, p2.x, p2.y) > 2 * dist(p1.x, p1.y, p2.x, p2.y):
        #if -10 < (math.degrees(math.atan2(p1.y - centy, p1.x - centx) - math.atan2(p2.y - centy, p2.x - centx))) % 360 < 10:
            pygame.draw.line(screen, white, (p1.x, p1.y), (p2.x, p2.y))
for d in data:
    d.show()
pygame.display.flip()

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
