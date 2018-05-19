import cv2
import numpy as np
import pyautogui as pag
import random as r
from time import sleep

windowname = "ALL UR BASE R BELONG 2 US"


def printscreen():
    img = pag.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def bars(frame, barwidth=30, barno=10):
    dims = frame.shape[:2]
    for i in range(barno):
        x1 = r.randrange(dims[1] - barwidth)
        x2 = r.randrange(max(0, x1 - barwidth), min(x1 + barwidth, dims[1] - barwidth))
        y1 = r.randrange(dims[0])
        y2 = dims[0] - y1
        portion1, portion2 = frame[y1:, x1:x1 + barwidth].copy(), frame[:y2, x2:x2 + barwidth].copy()
        frame[y1:, x1:x1 + barwidth], frame[:y2, x2:x2 + barwidth] = portion2, portion1


def recolor(frame, proportions=(-1, -1, -1)):
    proportions = np.float32([(proportions[i] if proportions[i] > -1 else r.random() * 1.5) for i in range(3)])
    frame[:, :] = np.minimum(np.maximum(np.int32(frame[:, :] * np.float32(proportions)), 0), 255)
    

def jitter(frame, maxjitterdist=10, jitterno=1):
    dims = frame.shape[:2]
    for i in range(jitterno):
        x1 = r.randrange(maxjitterdist, dims[1] - maxjitterdist)
        y1 = r.randrange(maxjitterdist, dims[0] - maxjitterdist)
        x2 = r.randrange(x1, dims[1] - maxjitterdist)
        y2 = r.randrange(y1, dims[0] - maxjitterdist)
        xj = r.randrange(-maxjitterdist, maxjitterdist)
        yj = r.randrange(-maxjitterdist, maxjitterdist)
        frame[y1 + yj: y2 + yj, x1 + xj: x2 + xj] = frame[y1: y2, x1: x2]


sleep(2)

screengrab = printscreen()
cv2.namedWindow(windowname, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(windowname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.startWindowThread()

# Hey look, a plainext password!
passcode = [103, 101, 116, 109, 101, 111, 117, 116]  # getmeout
checkcode = []

cycles = 0
while True:
    key = cv2.waitKey(33)
    if key != -1:
        checkcode.append(key)
        if passcode == checkcode:
            break
        elif checkcode != passcode[:len(checkcode)]:
            print("Not", checkcode)
            checkcode = []
    if cycles > 200:
        if r.random() >= 0.5:
            bars(frame, barno=r.randrange(10), barwidth=5)
        else:
            jitter(frame, jitterno=r.randrange(5), maxjitterdist=50)
        cycles -= 1
        if cycles == 200:
            recolor(frame)
            cycles %= 200
    else:
        frame = screengrab.copy()
        cycles += r.randrange(10)
    cv2.imshow(windowname, frame)
    
cv2.destroyAllWindows()
