import cv2
import numpy as np
from math import sqrt, sin, cos, radians
from time import sleep

w = 500
h = 500
screensize = (w, h)
screen = np.zeros([w, h, 3])

manimg = cv2.imread(r"D:\Users\Charles Turvey\Pictures\Art\Shadows\Man.png", -1)

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
        return M
    return raypoints[0]


def transformpoints(*points):
    n = int(len(np.float32(points).flatten()) / 3)
    point3D = np.float32(points).reshape(1, n, 3)
    point2D, _ = cv2.projectPoints(point3D, np.float32(rvec), np.float32(tvec),
                                   produced_camera_matrix, produced_dist_coefs)
    point2D = np.float32(point2D)
    return point2D


# Blits, but transparency is a binary option. If it's not 0, it's counted as 255
def blit(src, dest, pos=(0,0)):
    destw, desth = dest.shape[:2]
    srcw, srch = src.shape[:2]
    destx = (constrain(pos[0], 0, destw - 1), constrain(pos[0] + srcw, 0, destw - 1))
    desty = (constrain(pos[1], 0, desth - 1), constrain(pos[0] + srch, 0, desth - 1))
    srcx = (destx[0] - pos[0], destx[1] - pos[0])
    srcy = (desty[0] - pos[1], desty[1] - pos[1])
    decisions = (src[srcx[0]:srcx[1], srcy[0]:srcy[1], 3] > 0)
    for i in range(3):
        dest[destx[0]:destx[1], desty[0]:desty[1], i][decisions] = src[srcx[0]:srcx[1], srcy[0]:srcy[1], i][decisions]
    dest[:10, :10, :3] = np.array([255, 0, 0])


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
    def __init__(self, rectin, z, ang=0, col=(255, 255, 255)):
        self.rect = rectin
        self.z = z
        self.ang = radians(ang)
        self.col = col
        rightedgex = self.rect[0] + (self.rect[2] * cos(self.ang))
        rightedgez = z + (self.rect[2] * sin(self.ang))
        self.corners3D = np.float32([[*self.rect[:2], z],
                                     [rightedgex, self.rect[1], rightedgez],
                                     [rightedgex, self.rect[1] + self.rect[3], rightedgez],
                                     [self.rect[0], self.rect[1] + self.rect[3], z]])
        self.xvec = self.corners3D[1] - self.corners3D[0]
        self.yvec = self.corners3D[3] - self.corners3D[0]
        self.planevec = np.cross(self.xvec, self.yvec)
        self.corners2D = np.float32([[0, 0],
                                     [self.rect[2], 0],
                                     self.rect[2:],
                                     [0, self.rect[3]]]).reshape(4, 1, 2)
        self.surface = np.ones([self.rect[2], self.rect[3], 4], dtype="uint8") * 255
        backdrops.append(self)
    
    def project(self, lightpos, silhouette):
        projection3D = np.float32([quad_ray_intersection(self.corners3D,
                                                         [silhouette.corners3D[i], lightpos]) for i in range(4)])
        # Only cast a shadow if the object is closer than the light and they're both on the same side of the backdrop
        lightisbehindobject = np.all(np.linalg.norm(projection3D - lightpos, axis=1)
                                     > np.linalg.norm(projection3D - silhouette.corners3D, axis=1))
        bothsameside = np.all(np.sign(np.dot(lightpos - self.corners3D[0], self.planevec))
                              == np.sign(np.dot(silhouette.corners3D[:] - self.corners3D[0], self.planevec)))
        if lightisbehindobject and bothsameside:
            projection2D = np.zeros((4, 1, 2), dtype="float32")
            projection2D[:, 0, 0] = np.dot(projection3D - self.corners3D[0], self.xvec) / self.rect[2]
            projection2D[:, 0, 1] = np.dot(projection3D - self.corners3D[0], self.yvec) / self.rect[3]
            M = cv2.getPerspectiveTransform(silhouette.corners2D, projection2D)
            # Transparent bordermode is not listed in docs...
            # Neither is there a simple way to keep transparency in conversion from cvimages to surfaces...
            # So currently, transparency is handled by using a dark pink border in the cvimage and
            #   setting the colorkey to this colour in the surface
            tsurface = cv2.warpPerspective(silhouette.surface, M, self.rect[2:],
                                           borderMode=cv2.BORDER_TRANSPARENT)
            # Shadowifies the object by turning all non-dark-pink pixels dark grey
            tsurface[tsurface != [10, 0, 10, 0]] = 20
            blit(tsurface, self.surface)
        
    def show(self, offset=(0, 0, 0)):
        points2D = transformpoints(self.corners3D - np.array(offset))
        # Checks if all the points are off one side
        xon = not (np.all(0 > points2D[:, 0, 0]) or np.all(points2D[:, 0, 0] > w))
        yon = not (np.all(0 > points2D[:, 0, 1]) or np.all(points2D[:, 0, 1] > h))
        if xon and yon:
            M = cv2.getPerspectiveTransform(self.corners2D, points2D)
            # Transparent bordermode is not listed in docs...
            # Neither is there a simple way to keep transparency in conversion from cvimages to surfaces...
            # So currently, transparency is handled by using a dark pink border in the cvimage and
            #   setting the colorkey to this colour in the surface
            tsurface = cv2.warpPerspective(self.surface, M, screensize,
                                           borderMode=cv2.BORDER_TRANSPARENT)
            blit(tsurface, screen)
            self.surface = np.ones([*self.rect[2:], 4], dtype="uint8") * 255


class Light:
    def __init__(self, pos):
        self.pos = pos


class Silhouette:
    def __init__(self, surface, pos, ang=0):
        self.surface = surface
        self.rect = [*pos[:2], len(surface), len(surface[0])]
        self.pos = pos
        self.ang = radians(ang)
        self.z = pos[2]
        rightedgex = self.rect[0] + (self.rect[2] * cos(self.ang))
        rightedgez = self.z + (self.rect[2] * sin(self.ang))
        self.corners3D = np.float32([[*self.rect[:2], self.z],
                                     [rightedgex, self.rect[1], rightedgez],
                                     [rightedgex, self.rect[1] + self.rect[3], rightedgez],
                                     [self.rect[0], self.rect[1] + self.rect[3], self.z]])
        self.xvec = self.corners3D[1] - self.corners3D[0]
        self.yvec = self.corners3D[3] - self.corners3D[0]
        self.planevec = np.cross(self.xvec, self.yvec)
        self.corners2D = np.float32([[0, 0],
                                     [self.rect[2], 0],
                                     self.rect[2:],
                                     [0, self.rect[3]]]).reshape(4, 1, 2)
        backdrops.append(self)
    
    def project(self, a, b):
        ...
    
    def show(self, offset):
        points2D = transformpoints(self.corners3D - np.array(offset))
        # Checks if all the points are off one side
        xon = not (np.all(0 > points2D[:, 0, 0]) or np.all(points2D[:, 0, 0] > w))
        yon = not (np.all(0 > points2D[:, 0, 1]) or np.all(points2D[:, 0, 1] > h))
        if xon and yon:
            M = cv2.getPerspectiveTransform(self.corners2D, points2D)
            # Transparent bordermode is not listed in docs...
            # Neither is there a simple way to keep transparency in conversion from cvimages to surfaces...
            # So currently, transparency is handled by using a dark pink border in the cvimage and
            #   setting the colorkey to this colour in the surface
            tsurface = cv2.warpPerspective(self.surface, M, screensize,
                                           borderMode=cv2.BORDER_TRANSPARENT)
            blit(tsurface, screen)


Backdrop((int(w/2), int(h/3), w, int(h/1.5)), 150, -10)
Backdrop((-w*2, 0, w*4, h), 200, 0)
Silhouette(manimg, (0, h - len(manimg[0]), 0))
pos = np.array([0, 0, 0])
k = -1
while True:
    screen[:, :] = 0
    if k == 27:       # ESC KEY
        break
    if k == 2555904:  # RIGHT KEY
        pos[0] += 10
    if k == 2424832:  # LEFT KEY
        pos[0] -= 10
    if k == 2490368:  # UP KEY
        pos[2] += 10
    if k == 2621440:  # DOWN KEY
        pos[2] -= 10
    backdrops.sort(key=lambda B: B.z, reverse=True)
    lightpos = np.array([pos[0] + w/2, h/1.3, -50])
    for i, B in enumerate(backdrops):
        for B2 in backdrops[:i] + backdrops[i+1:]:
            B.project(lightpos, B2)
        B.show(pos)
    cv2.imshow("Window", screen)
    k = cv2.waitKeyEx(1)
