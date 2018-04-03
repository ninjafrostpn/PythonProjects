import pygame
from pygame.locals import *
import cv2
import numpy as np
from math import sqrt, sin, cos, radians

pygame.init()
screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

manimg = pygame.image.load_extended(r"D:\Users\Charles Turvey\Pictures\Art\Shadows\Man.png")

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
    def __init__(self, rectin, z, ang=0, col=(255, 255, 255)):
        self.rect = pygame.Rect(rectin)
        self.z = z
        self.ang = radians(ang)
        self.col = col
        rightedgex = self.rect.left + (self.rect.width * cos(self.ang))
        rightedgez = z + (self.rect.width * sin(self.ang))
        self.corners3D = np.float32([[*self.rect.topleft, z],
                                     [rightedgex, self.rect.top, rightedgez],
                                     [rightedgex, self.rect.bottom, rightedgez],
                                     [*self.rect.bottomleft, z]])
        self.xvec = self.corners3D[1] - self.corners3D[0]
        self.yvec = self.corners3D[3] - self.corners3D[0]
        self.planevec = np.cross(self.xvec, self.yvec)
        self.corners2D = np.float32([[0, 0],
                                     [self.rect.width, 0],
                                     self.rect.size,
                                     [0, self.rect.height]]).reshape(4, 1, 2)
        self.surface = pygame.Surface(self.rect.size).convert_alpha()
        self.surface.fill(self.col)
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
            projection2D[:, 0, 0] = np.dot(projection3D - self.corners3D[0], self.xvec) / self.rect.width
            projection2D[:, 0, 1] = np.dot(projection3D - self.corners3D[0], self.yvec) / self.rect.height
            M = cv2.getPerspectiveTransform(silhouette.corners2D, projection2D)
            cvsurface = surfacetocvimage(silhouette.surface)
            # Transparent bordermode is not listed in docs...
            # Neither is there a simple way to keep transparency in conversion from cvimages to surfaces...
            # So currently, transparency is handled by using a dark pink border in the cvimage and
            #   setting the colorkey to this colour in the surface
            cvsurface = cv2.warpPerspective(cvsurface, M, self.rect.size,
                                            borderMode=cv2.BORDER_CONSTANT, borderValue=(10, 0, 10))
            # Shadowifies the object by turning all non-dark-pink pixels dark grey
            cvsurface[cvsurface != [10, 0, 10]] = 20
            self.surface.blit(cvimagetosurface(cvsurface).convert_alpha(), (0, 0))
        
    def show(self, offset=(0, 0, 0)):
        points2D = transformpoints(self.corners3D - np.array(offset))
        # Checks if all the points are off one side
        xon = not (np.all(0 > points2D[:, 0, 0]) or np.all(points2D[:, 0, 0] > w))
        yon = not (np.all(0 > points2D[:, 0, 1]) or np.all(points2D[:, 0, 1] > h))
        if xon and yon:
            M = cv2.getPerspectiveTransform(self.corners2D, points2D)
            cvsurface = surfacetocvimage(self.surface)
            # Transparent bordermode is not listed in docs...
            # Neither is there a simple way to keep transparency in conversion from cvimages to surfaces...
            # So currently, transparency is handled by using a dark pink border in the cvimage and
            #   setting the colorkey to this colour in the surface
            cvsurface = cv2.warpPerspective(cvsurface, M, screensize,
                                            borderMode=cv2.BORDER_CONSTANT, borderValue=(10, 0, 10))
            screen.blit(cvimagetosurface(cvsurface).convert_alpha(), (0, 0))
            self.surface.fill(self.col)


class Light:
    def __init__(self, pos):
        self.pos = pos


class Silhouette:
    def __init__(self, surface, pos, ang=0):
        self.surface = surface.convert_alpha()
        self.rect = surface.get_rect().move(*pos[:2])
        self.pos = pos
        self.ang = radians(ang)
        self.z = pos[2]
        rightedgex = self.rect.left + (self.rect.width * cos(self.ang))
        rightedgez = self.z + (self.rect.width * sin(self.ang))
        self.corners3D = np.float32([[*self.rect.topleft, self.z],
                                     [rightedgex, self.rect.top, rightedgez],
                                     [rightedgex, self.rect.bottom, rightedgez],
                                     [*self.rect.bottomleft, self.z]])
        self.xvec = self.corners3D[1] - self.corners3D[0]
        self.yvec = self.corners3D[3] - self.corners3D[0]
        self.planevec = np.cross(self.xvec, self.yvec)
        self.corners2D = np.float32([[0, 0],
                                     [self.rect.width, 0],
                                     self.rect.size,
                                     [0, self.rect.height]]).reshape(4, 1, 2)
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
            cvsurface = surfacetocvimage(self.surface)
            # Transparent bordermode is not listed in docs...
            # Neither is there a simple way to keep transparency in conversion from cvimages to surfaces...
            # So currently, transparency is handled by using a dark pink border in the cvimage and
            #   setting the colorkey to this colour in the surface
            cvsurface = cv2.warpPerspective(cvsurface, M, screensize,
                                            borderMode=cv2.BORDER_CONSTANT, borderValue=(10, 0, 10))
            screen.blit(cvimagetosurface(cvsurface).convert_alpha(), (0, 0))


Backdrop((w/2, h/3, w, h/1.5), 150, -10)
Backdrop((-w*2, 0, w*4, h), 200, 0)
Silhouette(manimg, (0, h - manimg.get_height(), 0))
pos = np.array([0, 0, 0])
while True:
    screen.fill(0)
    keys = pygame.key.get_pressed()
    mpos = pygame.mouse.get_pos()
    pos += np.array([keys[K_RIGHT] - keys[K_LEFT],
                     0,
                     keys[K_UP] - keys[K_DOWN]]) * 10
    backdrops.sort(key=lambda B: B.z, reverse=True)
    lightpos = np.array([pos[0] + w/2, h/1.3, -50])
    for i, B in enumerate(backdrops):
        for B2 in backdrops[:i] + backdrops[i+1:]:
            B.project(lightpos, B2)
        B.show(pos)
    pygame.draw.circle(screen, (255, 0, 255), transformpoints(lightpos - pos)[0][0], 10)
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    pygame.display.flip()
