import pygame
from pygame.locals import *
import cv2
import numpy as np
from math import sqrt
from time import sleep

constrain = lambda val, lo, hi: min(max(lo, val), hi)


def dist(p1, p2):
    if len(p1) == len(p2):
        return sqrt(sum([(p1[i] - p2[i]) ** 2 for i in range(len(p1))]))
    else:
        return -1


def transformpoints(*points):
    points = np.float32(points).flatten()
    n = int(len(points) / 3)
    point3D = np.float32(points).reshape(1, n, 3)
    point2D, _ = cv2.projectPoints(point3D, np.float32(rvec), np.float32(tvec),
                                   produced_camera_matrix, produced_dist_coefs)
    return list(point2D[:, 0])


backplates = []

class Backplate:
    def __init__(self, rectin, z, col=(255, 0, 255)):
        rectin = Rect(rectin)
        self.points3D = [[*rectin.topleft, z],
                         [*rectin.topright, z],
                         [*rectin.bottomright, z],
                         [*rectin.bottomleft, z]]
        self.points2D = transformpoints(*self.points3D)
        self.z = z
        self.col = col
        backplates.append(self)
    
    def show(self):
        if self.z - posz > -100:
            self.points2D = transformpoints(*[(p[0] - posx + w/2, p[1], self.z - posz) for p in self.points3D])
            pygame.draw.polygon(screen, self.col, self.points2D)


pygame.init()
screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

size = (w, h)

# https://stackoverflow.com/a/46048098
# x is to the right, y is down, z is into the screen
obj_points = [0, 0, 10,
              w, 0, 10,
              w, h, 10,
              0, h, 10]
img_points = [100, 100,
              w - 100, 100,
              w - 100, h - 100,
              100, h - 100]

obj_points = np.float32(obj_points).reshape(1, int(len(obj_points) / 3), 3)
img_points = np.float32(img_points).reshape(1, int(len(img_points) / 2), 2)

camera_matrix = np.zeros((3, 3))
camera_matrix[0, 0] = 100  # F_x
camera_matrix[1, 1] = 100  # F_y
camera_matrix[2, 2] = 1.0
camera_matrix[0, 2] = w / 2  # C_x
camera_matrix[1, 2] = h * 5 / 8  # C_y

dist_coefs = np.zeros(4, dtype="float32")

retval, produced_camera_matrix, produced_dist_coefs, rvec, tvec = cv2.calibrateCamera(obj_points, img_points,
                                                                                      size, camera_matrix,
                                                                                      dist_coefs,
                                                                                      flags=cv2.CALIB_USE_INTRINSIC_GUESS)

posx = 0
posy = 0
vely = 0
posz = 0

for i in range(1, 50):
    z = i * w
    Backplate((10, 10, w - 20, h - 20), z, ((z * 7) % 256,
                                            (z * 11) % 256,
                                            (z * 13) % 256))

while True:
    keys = pygame.key.get_pressed()
    screen.fill(0)
    mpos = pygame.mouse.get_pos()
    
    posx = posx + (keys[K_RIGHT] - keys[K_LEFT])
    
    if posy < h - 25:
        vely += 0.1
    else:
        posy = h - 25
        vely = 0
    if keys[K_SPACE] and posy == h - 25:
        vely = -5
    posy += vely
    
    posz = max(posz + (keys[K_UP] - keys[K_DOWN]), 0)
    
    tpoints = transformpoints(posx, posy, 0, posx, posy - 25, 0)
    
    # Draw things
    backplates.sort(key=lambda b: b.z, reverse=True)
    drawnplayer = False
    for i, b in enumerate(backplates):
        if b.z < posz and not drawnplayer:
            pygame.draw.circle(screen, 255, (int(w / 2), int(tpoints[0][1])), int(dist(tpoints[0], tpoints[1])))
            drawnplayer = True
        b.show()
    if not drawnplayer:
        pygame.draw.circle(screen, 255, (int(w/2), int(tpoints[0][1])), int(dist(tpoints[0], tpoints[1])))
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    pygame.display.flip()
    sleep(0.001)
