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
        u = np.dot(M - planepoints[1], planevec1)
        v = np.dot(M - planepoints[1], planevec2)
        if (0 <= u <= dist(*planepoints[:2]) ** 2) and (0 <= v <= dist(*planepoints[1:3]) ** 2):
            return M
    return raypoints[0]


plates = []

class Plate:
    def show(self, offset):
        # TODO: clip the rects as they approach the edge of vision
        if -100 < self.refz - P.z < 2000:
            self.points2D = transformpoints(np.array(self.points3D) + offset)
            pygame.draw.polygon(screen, self.col, self.points2D)
            
    def __lt__(self, other):
        if self.z > other.z:
            return False
        if self.z == other.z and dist([P.x, P.y], [self.x, self.y]) > dist([P.x, P.y], [other.x, other.y]):
            return False
        return True


# The rect defines top-left in x-y and width to the right, height downward
class Zplate(Plate):
    def __init__(self, rectin, z, col=(255, 0, 255)):
        rectin = Rect(rectin)
        self.points3D = [[*rectin.topleft, z],
                         [*rectin.topright, z],
                         [*rectin.bottomright, z],
                         [*rectin.bottomleft, z]]
        self.points2D = transformpoints(*self.points3D)
        self.z = z
        self.x, self.y = rectin.topleft
        self.refz = z
        self.col = col
        plates.append(self)
    
    def infront(self):
        if P.z > self.z:
            return True
        return False


# The rect defines top-left in z-y and width to the back, height downward
class Xplate(Plate):
    def __init__(self, rectin, x, col=(255, 0, 255)):
        rectin = Rect(rectin)
        self.points3D = [[x, rectin.top, rectin.left],
                         [x, rectin.top, rectin.right],
                         [x, rectin.bottom, rectin.right],
                         [x, rectin.bottom, rectin.left]]
        self.points2D = transformpoints(*self.points3D)
        self.x = x
        self.z, self.y = rectin.center
        self.refz = rectin.left
        self.col = col
        plates.append(self)
    
    def infront(self):
        if abs(P.x - (w/2)) > abs(self.x - (w/2)) and P.z > self.refz:
            return True
        return False


# The rect defines near-left in x-z and width to the right, height into the screen
class Yplate(Plate):
    def __init__(self, rectin, y, col=(255, 0, 255)):
        rectin = Rect(rectin)
        self.points3D = [[rectin.left, y, rectin.top],
                         [rectin.right, y, rectin.top],
                         [rectin.right, y, rectin.bottom],
                         [rectin.left, y, rectin.bottom]]
        self.points2D = transformpoints(*self.points3D)
        self.y = y
        self.x, self.z = rectin.center
        self.refz = rectin.top
        self.col = col
        plates.append(self)
    
    def infront(self):
        if abs(P.y - (h/2)) > abs(self.y - (h/2)) and P.z > self.refz:
            return True
        return False


class Player(Plate):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        plates.append(self)
    
    def show(self, offset):
        pygame.draw.circle(screen, 255, tpoints[0], int(dist(tpoints[0], tpoints[1])))


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

P = Player(0, 0, 0)
vely = 0

for i in range(1, 500):
    z = i * w/10
    # Zplate((0, 0, w, h), z, ((z * 7) % 256,
    #                          (z * 11) % 256,
    #                          (z * 13) % 256))
    Xplate((z, 0, w/10, h), w + i*2, ((z * 17) % 256,
                             (z * 19) % 256,
                             (z * 23) % 256))
    Xplate((z, 0, w/10, h), i*2, ((z * 17) % 256,
                             (z * 19) % 256,
                             (z * 23) % 256))
    Yplate((i*2, z, w, h/10), h, ((z * 29) % 256,
                             (z * 31) % 256,
                             (z * 37) % 256))
    Yplate((i*2, z, w, h/10), 0, ((z * 29) % 256,
                             (z * 31) % 256,
                             (z * 37) % 256))

while True:
    keys = pygame.key.get_pressed()
    screen.fill(0)
    mpos = pygame.mouse.get_pos()
    
    P.x = P.x + (keys[K_RIGHT] - keys[K_LEFT]) * 10
    
    if P.y < h - 25:
        vely += 0.1
    else:
        P.y = h - 25
        vely = 0
    if keys[K_SPACE] and P.y == h - 25:
        vely = -15
    P.y += vely
    
    P.z = max(P.z + (keys[K_UP] - keys[K_DOWN]) * 10, 0)
    
    tpoints = transformpoints(w/2, h - 25, 0, w/2, h, 0)
    
    # Draw things
    plates.sort(reverse=True)
    drawnplayer = False
    for i, b in enumerate(plates):
        b.show(np.array([((w / 2) - P.x, w - 25 - P.y, -P.z)]))
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    pygame.display.flip()
    # sleep(0.001)
