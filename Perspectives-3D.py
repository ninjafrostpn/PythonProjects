import pygame
from pygame.locals import *
import cv2
import numpy as np
from math import sqrt

constrain = lambda val, lo, hi: min(max(lo, val), hi)


def dist(p1, p2):
    if len(p1) == len(p2):
        return sqrt(sum([(p1[i] - p2[i]) ** 2 for i in range(len(p1))]))
    else:
        return -1


def transformpoints(*points):
    n = int(len(points)/3)
    point3D = np.float32(points).reshape(1, n, 3)
    point2D, _ = cv2.projectPoints(point3D, np.float32(rvec), np.float32(tvec),
                                   produced_camera_matrix, produced_dist_coefs)
    return list(point2D[:, 0])
    

pygame.init()
screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

size = (w, h)

posx = 0
posy = 0
vely = 0
posz = 0

fx = 100
fy = 100

while True:
    keys = pygame.key.get_pressed()
    screen.fill(0)
    mpos = pygame.mouse.get_pos()

    # https://stackoverflow.com/a/46048098
    # x is to the right, y is down, z is into the screen
    obj_points = [0, 0, 10,
                  w, 0, 10,
                  w, h, 10,
                  0, h, 10]
    img_points = [100, 100,
                  400, 100,
                  400, 400,
                  100, 400]

    obj_points = np.float32(obj_points).reshape(1, int(len(obj_points) / 3), 3)
    img_points = np.float32(img_points).reshape(1, int(len(img_points) / 2), 2)
    
    camera_matrix = np.zeros((3, 3))
    camera_matrix[0, 0] = 100  # F_x
    camera_matrix[1, 1] = 100  # F_y
    camera_matrix[2, 2] = 1.0
    camera_matrix[0, 2] = w/2 # C_x
    camera_matrix[1, 2] = h * 5/8 # C_y

    dist_coefs = np.zeros(4, dtype="float32")
    
    retval, produced_camera_matrix, produced_dist_coefs, rvec, tvec = cv2.calibrateCamera(obj_points, img_points,
                                                                        size, camera_matrix, dist_coefs,
                                                                        flags=cv2.CALIB_USE_INTRINSIC_GUESS)
    
    for i in range(5):
        z = i * w
        squarepoints = transformpoints(10, 10, z,
                                       10, h - 10, z,
                                       w - 10, h - 10, z,
                                       w - 10, 10, z)
        pygame.draw.lines(screen, (255, 0, 255), True, squarepoints, 1)
    posx = constrain(posx + (keys[K_RIGHT] - keys[K_LEFT]), 0, w)
    if posy < h:
        vely += 0.1
    else:
        posy = h
        vely = 0
    if keys[K_SPACE] and posy == h:
        vely = -5
    posy += vely
    posz = max(posz + (keys[K_UP] - keys[K_DOWN]), 0)
    tpoints = transformpoints(posx, posy, posz, posx, posy - 25, posz)
    pygame.draw.circle(screen, 255, tpoints[0], int(dist(tpoints[0], tpoints[1])))
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    pygame.display.flip()
