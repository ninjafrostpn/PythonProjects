import cv2
import numpy as np
import time

K_ESC = 27
K_RIGHT = 2555904
K_LEFT = 2424832
K_UP = 2490368
K_DOWN = 2621440
K_W = 119
K_A = 97
K_S = 115
K_D = 100
K_0 = 48

handimg = cv2.imread(r"Crabs/Hand.png")

w, h = handimg.shape[:2]
screensize = np.int32([w, h])
screen = np.zeros([*screensize, 3], dtype="uint8")
# A good read: https://scipy-cookbook.readthedocs.io/items/Indexing.html
r = 90
mag = 10
f = 90
dstycoords = np.tile(np.arange(-r, r), 2 * r)
dstxcoords = np.repeat(np.arange(-r, r), 2 * r)
circlemask = ((dstycoords ** 2) + (dstxcoords ** 2)) <= (r ** 2)
dstycoords = dstycoords[circlemask]
dstxcoords = dstxcoords[circlemask]

starttime = time.time()

lensfuncset = [lambda q: np.int32(q / mag),
               lambda q: np.int32(q + (np.sin(np.deg2rad(q * (f / r))) * -mag)),
               lambda q: np.int32(q + (np.tan(np.deg2rad(q * (f / r))) * -mag)),
               np.abs,
               lambda q: q + ((np.random.random_sample(q.shape) - 0.5) * 2 * mag),
               lambda q: q + (np.random.normal(0, 1, q.shape) * mag * np.sin((time.time() - starttime) * 2)),
               ]
lensfunc = lensfuncset[0]
srcycoords = lensfunc(dstycoords)
srcxcoords = lensfunc(dstxcoords)

def updatelens():
    srcycoords[:] = lensfunc(dstycoords)
    srcxcoords[:] = lensfunc(dstxcoords)
    # print(time.time() - starttime)


x, y = (100, 100)

while True:
    screen[:] = handimg
    srccoords = [(srcxcoords + x) % w, (srcycoords + y) % h]
    dstcoords = [(dstxcoords + x) % w, (dstycoords + y) % h]
    screen[dstcoords] = handimg[srccoords]
    cv2.imshow("Window", screen)
    k = cv2.waitKeyEx(1)
    if k == K_ESC:
        break
    if k == K_RIGHT:
        y += 10
    if k == K_LEFT:
        y -= 10
    if k == K_UP:
        x -= 10
    if k == K_DOWN:
        x += 10
    if k == K_W:
        mag += 1
    if k == K_S:
        mag -= 1
    if k == K_A:
        f -= 10
    if k == K_D:
        f += 10
    if 0 <= (k - K_0) < 10:
        lensfunc = lensfuncset[k - K_0]
    updatelens()
    # if k != -1:
    #     print(k)
