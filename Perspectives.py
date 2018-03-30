import pygame
from pygame.locals import *
import cv2
import numpy as np
from random import randrange as rand
from math import sqrt

constrain = lambda val, lo, hi: min(max(lo, val), hi)
dist = lambda p1, p2: sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

def transformpoints(M, *points):
    cv2.perspectiveTransform(np.array([np.array(points, dtype="float32")]), M)


def pygame_to_cvimage(surface):
    sa = pygame.surfarray.array3d(surface)
    sa = np.flipud(np.rot90(sa))
    cvimage = cv2.cvtColor(sa, cv2.COLOR_RGB2BGR)
    return cvimage


def cvimagetosurface(cvimage):
    sa = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
    sa = np.rot90(np.fliplr(sa))
    surface = pygame.surfarray.make_surface(sa)
    return surface

pygame.init()

scorefont = pygame.font.Font(r"D:\Users\Charles Turvey\Documents\Python\Projects\OpenSans-Regular.ttf", 25)

gbaimg = pygame.transform.scale2x(pygame.image.load_extended(r"D:\Users\Charles Turvey\Pictures\DP Maps\GBA.png"))
screen = pygame.display.set_mode((gbaimg.get_width() + 480, max(gbaimg.get_height(), 320)))
w = screen.get_width()
h = screen.get_height()
gbaimg = gbaimg.convert_alpha()

gamescreen = screen.subsurface((0, max((h - 320)/2, 0), 480, 320))
gbascreen = screen.subsurface((480, max((h - gbaimg.get_height())/2, 0), gbaimg.get_width(), gbaimg.get_height()))

# Coordinates of screen corners, going clockwise
gamebox = np.array([[0, 0], [480, 0], [480, 320], [0, 320]], dtype="float32")
gbabox = np.array([[190, 21], [269, 67], [218, 114], [142, 63]], dtype="float32") * 2

# Obtain transformation matrix
M = cv2.getPerspectiveTransform(gamebox, gbabox)

points = 0
ballvel = [0, 0]
ballpos = [200, 100]
targpos = [rand(480), rand(320)]

while True:
    keys = pygame.key.get_pressed()
    ballvel = [0.99 * (ballvel[0] + (keys[K_d] - keys[K_a]) / 10),
               0.99 * (ballvel[1] + (keys[K_s] - keys[K_w]) / 10)]
    ballpos = [constrain(ballpos[0] + ballvel[0], 0, 480),
               constrain(ballpos[1] + ballvel[1], 0, 320)]
    if dist(ballpos, targpos) < 20:
        points += 1
        targpos = [rand(480), rand(320)]
        # print("{} Points".format(points))
    
    screen.fill(0)
    pygame.draw.circle(gamescreen, 255, (int(ballpos[0]), int(ballpos[1])), 10)
    pygame.draw.circle(gamescreen, (255, 0, 0), targpos, 10)
    gamescreen.blit(scorefont.render("Points: {}".format(points), True, (0, 255, 0)), (10, 260))
    pygame.draw.rect(gamescreen, (255, 255, 255), gamescreen.get_rect(), 2)
    
    gbadisplay = pygame_to_cvimage(gamescreen)
    # cv2.imshow("eep", gbadisplay)
    gbadisplay = cv2.warpPerspective(gbadisplay, M, gbascreen.get_size())
    gbascreen.blit(cvimagetosurface(gbadisplay), (0, 0))
    gbascreen.blit(gbaimg, (0, 0))
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    pygame.display.flip()
