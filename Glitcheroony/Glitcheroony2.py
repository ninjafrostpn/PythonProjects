import cv2
import numpy as np
import pyautogui as pag
import random as r
from time import sleep

windowname = "ALL UR BASE R BELONG 2 US"


def printscreen():
    img = pag.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


sleep(2)

screengrab = printscreen()
cv2.namedWindow(windowname, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(windowname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.startWindowThread()

# Hey look, a plaintext password!
passcode = [103, 101, 116, 109, 101, 111, 117, 116, 27]  # getmeout[esc]
checkcode = []

flatmask = cv2.imread(r"D:\Users\Charles Turvey\Documents\Python\Projects\Glitcheroony\Skull.png")
flatmask = cv2.cvtColor(flatmask, cv2.COLOR_RGB2BGR)
flatmask = flatmask[:, :, 0] == 0

cycles = 0
started = False
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
        if not started:
            emboss(frame, flatmask)
            started = True
        if r.random() >= 0.5:
            bars(frame, barno=r.randrange(10), barwidth=5)
        else:
            jitter(frame, jitterno=r.randrange(5), maxjitterdist=50)
        cycles -= 1
        if cycles == 200:
            recolor(frame)
            cycles %= 200
            started = False
    else:
        frame = screengrab.copy()
        cycles += r.randrange(10)
    cv2.imshow(windowname, frame)
    
cv2.destroyAllWindows()
