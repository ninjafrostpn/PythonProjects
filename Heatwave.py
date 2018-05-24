import cv2
from math import sin, cos, pi, radians
import numpy as np

img = cv2.imread(r"D:\Users\Charles Turvey\Pictures\Art\Wah\WaluigiHead.png")


def wavify(src, pos, size, cycles, intensity=1):
    pos = np.int32(pos)
    size = np.int32(size)
    out = src.copy()
    for y in range(int(max(pos[1] - size[1]/2, 0)), int(min(pos[1] + size[1]/2, src.shape[0]))):
        theta = pi * ((y - pos[1]) / size[1])
        halfwidth = int(size[0] * (4 + cos(theta)) / 8)  # Adds slight medial bulge
        xoff = int(size[0]/4 * sin(radians(cycles * intensity) + theta))
        out[y, pos[0] - halfwidth + xoff: pos[0] + halfwidth + xoff] = out[y, pos[0] - halfwidth: pos[0] + halfwidth].copy()
    if intensity > 1:
        return wavify(out, pos, size, cycles + intensity, intensity - 1)
    else:
        return out


cycles = 0
while cv2.waitKey(1) == -1:
    cv2.imshow("", wavify(img, np.int32(img.shape[:2])/2, (100, 100), cycles, 5))
    cycles += 1
