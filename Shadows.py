import pygame
from pygame.locals import *
import cv2
import numpy as np
from math import sqrt, sin, cos, radians

pygame.init()
screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

gbaimg = pygame.image.load_extended(r"D:\Users\Charles Turvey\Pictures\DP Maps\GBA.png")

constrain = lambda val, lo, hi: min(max(lo, val), hi)


def dist(p1, p2):
    if len(p1) == len(p2):
        return sqrt(sum([(p1[i] - p2[i]) ** 2 for i in range(len(p1))]))
    else:
        return -1


# Computes whether a quad defined by four coplanar points and ray defined by two intersect
# https://stackoverflow.com/questions/21114796/3d-ray-quad-intersection-test-in-java
def quad_ray_intersection(planepoints, raypoints):
    planepoints = np.array(planepoints)
    planevec1 = planepoints[0] - planepoints[1]
    planevec2 = planepoints[2] - planepoints[1]
    planenormvector = np.cross(planevec1, planevec2)
    raypoints = np.array(raypoints)
    rayvector = raypoints[1] - raypoints[0]
    dp = np.dot(planenormvector, rayvector)
    if abs(dp) > 0.00001:
        t = np.dot(-planenormvector, raypoints[0] - planepoints[1]) / dp
        M = raypoints[0] + (rayvector * t)
        # u = np.dot(M - planepoints[1], planevec1)
        # v = np.dot(M - planepoints[1], planevec2)
        return M
    return raypoints[0]


def transformpoints(*points):
    points = np.float32(points).flatten()
    n = int(len(points) / 3)
    point3D = np.float32(points).reshape(1, n, 3)
    point2D, _ = cv2.projectPoints(point3D, np.float32(rvec), np.float32(tvec),
                                   produced_camera_matrix, produced_dist_coefs)
    point2D = np.float32(point2D)
    return point2D


def surfacetocvimage(surface):
    sa = pygame.surfarray.array3d(surface)
    sa = np.flipud(np.rot90(sa))
    cvimage = cv2.cvtColor(sa, cv2.COLOR_RGB2BGR)
    return cvimage


def cvimagetosurface(cvimage, colorkey=(10, 0, 10)):
    sa = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
    sa = np.rot90(np.fliplr(sa))
    surface = pygame.surfarray.make_surface(sa)
    surface.set_colorkey(colorkey)
    return surface


screensize = (w, h)

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
                                                                                      screensize, camera_matrix,
                                                                                      dist_coefs,
                                                                                      flags=cv2.CALIB_USE_INTRINSIC_GUESS)


backdrops = []

class Backdrop:
    def __init__(self, rectin, z, ang=0):
        self.rect = pygame.Rect(rectin)
        self.z = z
        self.ang = radians(ang)
        rightedgex = self.rect.left + (self.rect.width * cos(self.ang))
        rightedgez = z + (self.rect.width * sin(self.ang))
        self.points3D = np.float32([[*self.rect.topleft, z],
                                    [rightedgex, self.rect.top, rightedgez],
                                    [rightedgex, self.rect.bottom, rightedgez],
                                    [*self.rect.bottomleft, z]])
        self.corners = np.float32([[0, 0],
                                   [self.rect.width, 0],
                                   self.rect.size,
                                   [0, self.rect.height]]).reshape(4, 1, 2)
        self.surface = pygame.Surface(self.rect.size).convert_alpha()
        self.surface.fill((255, 255, 255))
        for i in range(0, self.rect.width, 20):
            pygame.draw.circle(self.surface, 255, (i, i), 10)
        self.surface.blit(gbaimg, (100, 100))
        backdrops.append(self)
    
    def project(self):
        ...
        
    def show(self, offset=(0, 0, 0)):
        points2D = transformpoints(self.points3D - np.array(offset))
        xon = np.any((0 < points2D[:, 0, 0]) & (points2D[:, 0, 0] < w))
        yon = np.any((0 < points2D[:, 0, 1]) & (points2D[:, 0, 1] < h))
        if xon and yon:
            M = cv2.getPerspectiveTransform(self.corners, points2D)
            cvsurface = surfacetocvimage(self.surface)
            # Transparent bordermode is not listed in docs...
            # Neither is there a simple way to keep transparency in conversion from cvimages to surfaces...
            # So currently, transparency is handled by using a dark pink border in the cvimage and
            #   setting the colorkey to this colour in the surface
            cvsurface = cv2.warpPerspective(cvsurface, M, screensize,
                                            borderMode=cv2.BORDER_CONSTANT, borderValue=(10, 0, 10))
            screen.blit(cvimagetosurface(cvsurface), (0, 0))


class light:
    def __init__(self, pos):
        pass


class silhouette:
    def __init__(self, points):
        self.points = points
        
for i in range(10):
    Backdrop((i * w, 0, w, h), 100, i)
pos = np.array([0, 0, 0])
while True:
    screen.fill(0)
    keys = pygame.key.get_pressed()
    pos += np.array([keys[K_RIGHT] - keys[K_LEFT],
                     0,
                     keys[K_UP] - keys[K_DOWN]]) * 10
    backdrops.sort(key=lambda B: B.z, reverse=True)
    for B in backdrops:
        B.show(pos)
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    pygame.display.flip()
