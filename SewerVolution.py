import cv2
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix as spdistmat

K_ESC = 27
K_RIGHT = 2555904
K_LEFT = 2424832
K_UP = 2490368
K_DOWN = 2621440

w = 600
h = 600
screensize = np.int32([w, h])
# https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html
screen = np.zeros([w, h, 3], dtype="uint8")

constrain = lambda val, lo, hi: np.minimum(np.maximum(lo, val), hi)


def normalise(vec, factor=1):
    mag = np.linalg.norm(vec, axis=-1)
    zerovecmask = mag == 0
    retvec = vec.copy()
    retvec[zerovecmask] = (0, 0)
    retvec[~zerovecmask] = ((retvec[~zerovecmask].T * factor) / mag[~zerovecmask]).T
    return retvec


def transformpoints(*points):
    point3D = np.float32(points).reshape(1, -1, 3)
    point2D, _ = cv2.projectPoints(point3D, np.float32(rvec), np.float32(tvec),
                                   produced_camera_matrix, produced_dist_coefs)
    return np.float32(point2D)


# Blits, but transparency is a binary option. If it's not 0, it's counted as 255
def blit(src, dest, pos=(0, 0)):
    pos = np.int32(pos)
    destsize = np.int32(dest.shape[:2])
    destpos = np.int32([constrain(pos, 0, destsize - 1),
                        constrain(pos + src.shape[:2], 0, destsize - 1)])
    srcpos = destpos - pos
    dest[destpos[0][0]:destpos[1][0],
         destpos[0][1]:destpos[1][1], :] = src[srcpos[0][0]:srcpos[1][0],
                                               srcpos[0][1]:srcpos[1][1], :]
    # dest[:20, :10, :3] = np.array([255, 0, 0])  # DEBUG


# Kills a particular critter
def killcrits(hitlist):
    pass


# https://stackoverflow.com/a/46048098
# x is to the right, y is up, z is into the screen
obj_points = [0, 0, 0,
              w, 0, 0,
              0, 0, h,
              w, 0, h,
              0, h / 2, h,
              w, h / 2, h]
img_points = [0, h,
              w, h,
              int(w / 6), int(h * (2 / 3)),
              int(w * (5 / 6)), int(h * (2 / 3)),
              int(w / 6), h / 2,
              int(w * (5 / 6)), h / 2]

obj_points = np.float32(obj_points).reshape(1, -1, 3)
img_points = np.float32(img_points).reshape(1, -1, 2)

camera_matrix = np.zeros((3, 3))
camera_matrix[0, 0] = 100  # F_x
camera_matrix[1, 1] = 100  # F_y
camera_matrix[2, 2] = 1.0
camera_matrix[0, 2] = 250  # C_x
camera_matrix[1, 2] = 492.5  # C_y

dist_coefs = np.zeros(4, dtype="float32")
_, produced_camera_matrix, produced_dist_coefs, rvec, tvec = cv2.calibrateCamera(obj_points, img_points,
                                                                                 tuple(screensize), camera_matrix,
                                                                                 dist_coefs,
                                                                                 flags=cv2.CALIB_USE_INTRINSIC_GUESS)

# A nice pool of light
ground = np.zeros([w, h, 3], dtype="uint8")
for i in range(h):
    cv2.circle(ground, tuple(np.int32([w/2, h/2])), int((h - i)/2),
               [int(i * 200/h)] * 3, 2)
groundcentre3D = np.float32([w/2, 0, 80 + h/2])
groundcentre2D = transformpoints(groundcentre3D)[0][0]
M = cv2.getPerspectiveTransform(np.float32([[0, 0],
                                            [w, 0],
                                            [w, h],
                                            [0, h]]),
                                transformpoints(np.float32([[[0, 0, 80],
                                                             [w, 0, 80],
                                                             [w, 0, 80 + h],
                                                             [0, 0, 80 + h]]])))

# Produce arrays characterising critters
N = 200
critspd = np.random.randint(1, 11, N)
critpos = np.random.random_sample([N, 2]) * screensize
critvel = np.zeros([N, 2])
critcol = np.random.randint(0, 256, (N, 3))
critrad = np.random.random_sample(N) * 5 + 5
critmaxnrg = (2/3) * np.pi * (critrad ** 3)  # Approximating the critters as hemispheres
critnrg = critmaxnrg.copy()
# Movement cost, approximated using surface area of underside * speed * volume, w/ fudge for density and gravity
critmovnrg = (2/3) * (critrad ** 5) * critspd * 0.00001

# Produce array of foods
foodstock = 100
foodpos = (np.random.random_sample([foodstock, 2]) * 0.6 + 0.2) * screensize
foodnrg = (np.random.random_sample(foodstock) * 9) + 1

k = -1
cycle = 0
temp = 0
phase = 0
foodphasedur = 100
tempstep = 1
maxtemp = 100
while k != 27:
    screen[:, :, :] = 0
    currground = ground.copy()
    # Move critters
    critvel += ((np.random.random_sample(critpos.shape) - 0.5).T * critspd).T
    critvel = normalise(critvel, critspd)
    critpos = constrain(critpos + (critvel.T * critspd).T, 0, screensize)
    # Takes energy costs and kills exhausted critters TODO: put this all in a dataframe
    critnrg -= critmovnrg
    hitlist = np.argwhere(critnrg <= 0)
    critspd = np.delete(critspd, hitlist, axis=0)
    critpos = np.delete(critpos, hitlist, axis=0)
    critvel = np.delete(critvel, hitlist, axis=0)
    critcol = np.delete(critcol, hitlist, axis=0)
    critrad = np.delete(critrad, hitlist, axis=0)
    critnrg = np.delete(critnrg, hitlist, axis=0)
    critmaxnrg = np.delete(critmaxnrg, hitlist, axis=0)
    critmovnrg = np.delete(critmovnrg, hitlist, axis=0)
    # Feeds appropriate critters
    critfooddist = spdistmat(critpos, foodpos)  # Array of distances with first indices [crit id, food id]
    eatpairs = np.argwhere((critfooddist.T < critrad + 3).T)  # Pairs of ids characterising critter-food collisions
    if eatpairs.shape[0]:
        foodcontenders = np.bincount(eatpairs[:, 1],
                                     minlength=foodstock)  # Number of critters trying to eat each food item
        foodpos[foodcontenders > 0] = -100  # Hurls eaten food offscreen
        critnrg[eatpairs[:, 0]] += foodnrg[eatpairs[:, 1]] / foodcontenders[eatpairs[:, 1]]
    # Draw foods as black 3x3 squares
    for i in range(len(foodpos)):
        currground[int(foodpos[i, 1] - 3): int(foodpos[i, 1] + 4),
                   int(foodpos[i, 0] - 3): int(foodpos[i, 0] + 4), :] = 100 - (foodnrg[i] * 10)
    # Draw critters as coloured circles
    critfillrad = ((critnrg * 3) / (2 * np.pi)) ** (1/3)
    for i in range(len(critpos)):
        cv2.circle(currground,
                   tuple(np.int32(critpos[i])), np.int32(critfillrad)[i],
                   [int(col)
                    for col in (h/2 - np.linalg.norm(screensize/2 - critpos[i])) * 400/(255 * h) * critcol[i % N]],
                   thickness=-1)
        cv2.circle(currground,
                   tuple(np.int32(critpos[i])), np.int32(critrad)[i],
                   0,
                   thickness=1)
    # currground[y:y+100] = np.uint8(currground[y:y+100] * 0.5)
    currground = np.uint8(currground * (1 - temp/100, 1 - temp/100, 1))
    tsurface = cv2.warpPerspective(currground, M, tuple(screensize),
                                   borderMode=cv2.BORDER_TRANSPARENT)
    blit(tsurface, screen)
    cv2.imshow("EVOLVE", screen)
    k = cv2.waitKeyEx(1)
    # critpos = np.append(critpos, np.random.random_sample([1, 2]) * screensize, axis=0)
    cycle += 1
    if phase == 0 and cycle > foodphasedur:
        cycle = 0
        phase = 1
    if phase == 1:
        temp += tempstep
        if temp > maxtemp:
            cycle = 0
            phase = 2
            eatenmask = foodpos[:, 0] < 0
            foodpos[eatenmask] = (np.random.random_sample([np.sum(eatenmask), 2]) * 0.6 + 0.2) * screensize
    if phase == 2:
        temp -= tempstep
        if temp <= 0:
            temp = 0
            cycle = 0
            phase = 0
