import cv2
from math import radians, cos, sin
import numpy as np
from random import randrange as rand

w = 500
h = 500
size = (w, h)
allpoints = np.float32([[x, y, 0] for x in range(w) for y in range(h)]).reshape(-1, 1, 2)

allcolours = set()
palette = []
maxdepth = 400

cv2.namedWindow("")

# https://stackoverflow.com/a/46048098
# x is to the right, y is down, z is into the screen
obj_points = np.float32([0, 0, 10,
                         w, 0, 10,
                         w, h, 10,
                         0, h, 10,
                         w/2, h/2, 0]).reshape(1, -1, 3)
img_points = np.float32([100, 100,
                         w - 100, 100,
                         w - 100, h - 100,
                         100, h - 100,
                         w/2, h/2]).reshape(1, -1, 2)

camera_matrix = np.zeros((3, 3))
camera_matrix[0, 0] = 100  # F_y
camera_matrix[1, 1] = 100  # F_x
camera_matrix[2, 2] = 1.0
camera_matrix[0, 2] = h/2  # C_y
camera_matrix[1, 2] = w/2  # C_x
dist_coefs = np.zeros(4, dtype="float32")
retval, produced_camera_matrix, produced_dist_coefs, rvec, tvec = cv2.calibrateCamera(obj_points, img_points,
                                                                                      size, camera_matrix,
                                                                                      dist_coefs,
                                                                                      flags=cv2.CALIB_USE_INTRINSIC_GUESS)


def transformpoints(*points):
    point3D = np.float32(points).reshape(1, -1, 3)
    point2D, _ = cv2.projectPoints(point3D, np.float32(rvec), np.float32(tvec),
                                   produced_camera_matrix, produced_dist_coefs)
    return point2D[:, 0]


class Image:
    def __init__(self, image, alphamask=True):
        self.alphamask = alphamask
        self.colours = [tuple(colour) for colour in np.unique(image.reshape(-1, 3), axis=0)]
        self.colourmask = np.zeros(image.shape[:2], dtype='uint8')
        for colour in self.colours:
            print(colour)
            if colour not in allcolours:
                allcolours.add(colour)
                palette.append(colour)
            colourpos = (image == colour)[:, :].any(axis=2)
            colourindex = palette.index(colour)
            self.colourmask[colourpos] = colourindex
        self.w, self.h = self.colourmask.shape[:2]
        self.corners2D = np.float32([[0, 0],
                                    [self.w, 0],
                                    [self.w, self.h],
                                    [0, self.h]]).reshape(4, 1, 2)
        
    def render(self, y, x, z):
        points3D = np.array([[x, y, z],
                             [x + self.w, y, z],
                             [x + self.w, y + self.h, z],
                             [x, y + self.h, z]])
        points2D = transformpoints(points3D)
        xon = not (np.all(0 > points2D[:, 0]) or np.all(points2D[:, 0] > w))
        yon = not (np.all(0 > points2D[:, 1]) or np.all(points2D[:, 1] > h))
        if xon and yon:
            M1 = cv2.getPerspectiveTransform(self.corners2D, points2D)
            talpha = cv2.warpPerspective(np.float32(self.alphamask), M1, size[::-1],
                                         borderMode=cv2.BORDER_TRANSPARENT) > 0
            tcolour = cv2.warpPerspective(np.array(palette)[self.colourmask], M1, size[::-1],
                                          borderMode=cv2.BORDER_TRANSPARENT)
            
            M2 = cv2.getPerspectiveTransform(points2D, self.corners2D)
            M3, _ = cv2.findHomography(self.corners2D, points3D)
            tdepth = cv2.perspectiveTransform(cv2.perspectiveTransform(allpoints, M2), M3).reshape(*size, -1)[:, :, 2]
            
            drawpixels = (screendepth > tdepth) & talpha
            
            screendepth[drawpixels] = tdepth[drawpixels]
            screen[drawpixels] = tcolour[drawpixels]


imagealpha = np.ones((40, 40), dtype='bool')
imagealpha[10:21, 10:21] = 0
squareno = 16
squares = []
for i in range(squareno):
    imagecolour = np.zeros((40, 40, 3), dtype='uint8')
    imagecolour[:, :] = (0, rand(256), rand(256))
    squares.append(Image(imagecolour, imagealpha))
    
imagealpha = np.ones((80, h - 50), dtype='bool')
imagecolour = np.zeros((80, h - 50, 3), dtype='uint8')
imagecolour[:, :] = (rand(256), 0, rand(128))
tower = Image(imagecolour, imagealpha)

cycles = 0
while True:
    screendepth = np.zeros((w, h), dtype='float64')
    screendepth[:, :] = maxdepth
    screen = np.zeros((w, h, 3), dtype='uint8')
    for i, I in enumerate(squares):
        I.render((w/2 * (cos(radians(cycles + (i * (360/squareno)))) + 1)) - 20,
                 h/2,
                 (w/2 * (sin(radians(cycles + (i * (360/squareno)))) + 1)) - 20)
    tower.render(w/2 - 40, 0, 100)
    cv2.imshow("", cv2.cvtColor(np.rot90(np.fliplr(screen)), cv2.COLOR_RGB2BGR))
    cycles += 1
    key = cv2.waitKey(1)
    if key == 27:
        break
print("Nooooo...")
