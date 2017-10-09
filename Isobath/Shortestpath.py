import pygame, math
from pygame.locals import *
pygame.init()
from random import randrange as rand

dist = lambda x1, y1, x2, y2: math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))
white = (255, 255, 255)

screen = pygame.display.set_mode((750, 500))
w = screen.get_width()
h = screen.get_height()

points = [(rand(w), rand(h)) for i in range(20)]

connections = []
for i in range(len(points) - 1):
    p1 = points[i]
    for j in range(i + 1, len(points)):
        p2 = points[j]
        connections.append([i, j, dist(p1[0], p1[1], p2[0], p2[1])])
connections.sort(key=lambda c:c[2])
final = []
done = set()
for c in connections:
    if c[0] not in done or c[1] not in done:
        done.add(c[0])
        done.add(c[1])
        final.append(c)
    if len(done) == len(points):
        break

while True:
    for arc in final:
        pygame.draw.line(screen, white, points[arc[0]][:2], points[arc[1]][:2])
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
