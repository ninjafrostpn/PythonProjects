import cv2
from math import ceil, cos, pi, sin
import numpy as np
import pyautogui as pag
import random as r
from time import sleep

windowname = "ALL UR BASE R BELONG 2 US"

mode = r.randrange(0, 2)

if mode == 1:
    eye_cascade = cv2.CascadeClassifier(
        r'C:\Users\Charles Turvey\AppData\Local\Programs\Python\Python35-32\Lib\site-packages\cv2\data\haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    framesize = np.array(frame.shape[1::-1])
    framecentre = np.int32(framesize / 2)


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
    proportions = np.float32([(proportions[i] if proportions[i] > -1 else r.random() + 0.5) for i in range(3)])
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
        
        
def emboss(frame, mask, embossdist=(0, 50)):
    framedims = frame.shape[:2]
    maskdims = mask.shape[:2]
    left = r.randrange(embossdist[0], framedims[1] - maskdims[1] - embossdist[0])
    top = r.randrange(embossdist[1], framedims[0] - maskdims[0] - embossdist[1])
    right = left + maskdims[1]
    bottom = top + maskdims[0]
    xj = embossdist[0]
    yj = embossdist[1]
    frame[top + yj: bottom + yj, left + xj: right + xj][mask] = frame[top: bottom, left: right][mask]


def isfeaturevisible(cap, featuredetector):
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.CV_8U)
        features = featuredetector.detectMultiScale(frame, 1.3, 5)
        if len(features) > 0:
            return True
    return False


class Eye:
    def __init__(self, frame, size=(500, 200), pupilpos=(-1, -1), vertical=True):
        framedims = frame.shape[:2]
        self.size = np.int32(size)
        self.pos = np.int32([r.randrange(framedims[1] - self.size[0]), r.randrange(framedims[0] - self.size[1])])
        self.vertical = vertical
        self.pupilpos = np.float32([(pupilpos[i] if pupilpos[i] > -1 else r.randrange(framedims[i])) for i in range(2)]) - self.pos
        self.pupilrad = int(min(self.size) * 0.3)
        self.source = frame[self.pos[1]: self.pos[1] + self.size[1], self.pos[0]: self.pos[0] + self.size[0]]
        self.sourcecopy = self.source.copy()
        self.cycles = 0
        self.inc = int(size[int(self.vertical)] / 20)
    
    def show(self):
        self.source[:] = 0
        cv2.circle(self.source, tuple(np.int32(self.pupilpos)), self.pupilrad, (255, 255, 0), int(self.pupilrad/2))
        halfwidth = ceil(self.size[int(self.vertical)] / 2)
        if np.all(self.size * 0.4 < self.pupilpos) and np.all(self.pupilpos < self.size * 0.6):
            if self.inc > 0 or self.cycles >= halfwidth:
                if isfeaturevisible(cap, eye_cascade):
                    if self.cycles >= halfwidth:
                        self.cycles = halfwidth - 1
                    if self.inc > 0:
                        self.inc *= -1
            for i in range(self.pupilrad):
                self.source[int(self.pupilpos[1] + r.randrange(-int(self.pupilrad/2.5), int(self.pupilrad/2.5))),
                            int(self.pupilpos[0] + r.randrange(-int(self.pupilrad/2.5), int(self.pupilrad/2.5))), 1] = 255
        if self.cycles < halfwidth:
            if self.vertical:
                toplidfrom = self.cycles
                toplidto = halfwidth - toplidfrom
                btmlidfrom = self.size[1] - toplidfrom
                btmlidto = self.size[1] - toplidto
                self.source[:toplidto, :] = self.sourcecopy[toplidfrom: halfwidth, :]
                self.source[btmlidto:, :] = self.sourcecopy[halfwidth: btmlidfrom, :]
            else:
                leftlidfrom = self.cycles
                leftlidto = halfwidth - leftlidfrom
                rightlidfrom = self.size[0] - leftlidfrom
                rightlidto = self.size[0] - leftlidto
                self.source[:, :leftlidto] = self.sourcecopy[:, leftlidfrom: halfwidth]
                self.source[:, rightlidto:] = self.sourcecopy[:, halfwidth: rightlidfrom]
            if self.cycles <= 0 and self.inc < 0:
                return False, self.pupilpos + self.pos
        else:
            pupilmov = self.size / 2 - self.pupilpos
            self.pupilpos += pupilmov / 10
            if self.cycles >= halfwidth + self.inc * 200 and self.inc > 0:
                self.inc *= -1
        self.cycles = max(self.cycles + self.inc, 0)
        return True, self.pupilpos + self.pos


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
startpos = (-1, -1)
while True:
    if mode == 0:
        key = cv2.waitKey(33)
    elif mode == 1:
        key = cv2.waitKey(1)
    if key != -1:
        checkcode.append(key)
        if passcode == checkcode:
            break
        elif checkcode != passcode[:len(checkcode)]:
            print("Not", checkcode)
            checkcode = []
    if cycles > 200:
        if mode == 0:
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
                cycles = 0
                started = False
        elif mode == 1:
            try:
                ret, startpos = curreye.show()
                if not ret:
                    cycles = -1000
                    del curreye
            except NameError as e:
                if not isfeaturevisible(cap, eye_cascade):
                    curreye = Eye(frame,
                                  size=np.int32([r.randrange(50, 250), r.randrange(50, 250)]) * 2,
                                  pupilpos=startpos,
                                  vertical=r.random() < 0.5)
    else:
        frame = screengrab.copy()
        cycles += r.randrange(10)
    cv2.imshow(windowname, frame)
    
cv2.destroyAllWindows()
