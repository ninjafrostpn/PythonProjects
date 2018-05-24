import cv2
import numpy as np
import pyautogui as pag
import random as r
from time import sleep

ESCAPE = 27
SPACE = 32
LEFT = 2424832
RIGHT = 2555904
UP = 2490368
DOWN = 2621440

windowname = "CAMOUFLAGE"

directions = {LEFT: np.int32([-1, 0]),
              RIGHT: np.int32([1, 0]),
              UP: np.int32([0, -1]),
              DOWN: np.int32([0, 1])}


def printscreen():
    img = pag.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        
def emboss(frame, mask, frompos, topos):
    # framedims = frame.shape[:2]
    maskdims = mask.shape[:2]
    frame[topos[1]: topos[1] + maskdims[1], topos[0]: topos[0] + maskdims[0]][mask] =\
        frame[frompos[1]: frompos[1] + maskdims[1], frompos[0]: frompos[0] + maskdims[0]][mask]


sleep(2)

screengrab = printscreen()
cv2.namedWindow(windowname, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(windowname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.startWindowThread()

flatmask = np.ones((100, 100, 3), dtype='bool')
flatmask[10:90, 10:90] = False
# flatmask = cv2.cvtColor(flatmask, cv2.COLOR_RGB2BGR)
# flatmask = flatmask[:, :, 0] == 0

cycles = 0
started = False
pos = np.int32([0, 0])
while True:
    frame = screengrab.copy()
    key = cv2.waitKeyEx(33)
    if key == ESCAPE:
        break
    elif key in directions.keys():
        pos += directions[key] * 20
    elif key != -1:
        print(key)
    emboss(frame, flatmask, (0, 0), pos)
    cv2.imshow(windowname, frame)
    
cv2.destroyAllWindows()
