import cv2
import numpy as np
import pygame
from pygame.locals import *
from scipy.ndimage.filters import convolve
from scipy.stats import linregress
from time import sleep

pygame.init()

screen = pygame.display.set_mode((1000, 500))
w, h = screen.get_size()
print(w, h)
screen.fill(255)
pygame.display.flip()
keys = set()

blobfinder = -5 * np.ones([17, 17])
blobfinder = cv2.circle(blobfinder, (8, 8), 6, 10, -1)

face_cascade = cv2.CascadeClassifier(r"C:\Users\charl\AppData\Local\Programs\Python"
                                     r"\Python37-32\Lib\site-packages\cv2\data"
                                     r"\haarcascade_frontalface_alt2.xml")
eye_cascade = cv2.CascadeClassifier(r"C:\Users\charl\AppData\Local\Programs\Python"
                                    r"\Python37-32\Lib\site-packages\cv2\data"
                                    r"\haarcascade_eye_tree_eyeglasses.xml")

cap = cv2.VideoCapture(0)
_, frame = cap.read()
framesize = np.array(frame.shape[1::-1])
framecentre = np.int32(framesize/2)

eyelr = []
dotlr = []
eyeud = []
dotud = []

cycles = 0
while cv2.waitKey(1) == -1:
    screen.fill(0)
    dotpos = np.int32([(np.sin(cycles / 3) + 1) * w / 2, (np.cos(cycles / 10) + 1) * h / 2])
    pygame.draw.circle(screen, (255, 0, 255), dotpos, 10)
    pygame.display.flip()
    sleep(0.1)
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.CV_8U)
        faces = face_cascade.detectMultiScale(frame, 1.1, 5)
        for i, (xf, yf, wf, hf) in enumerate(faces):
            faceframe = frame[yf:yf+hf, xf:xf+wf]
            eyes = eye_cascade.detectMultiScale(faceframe, 1.1, 5)
            for j, (xe, ye, we, he) in enumerate(eyes):
                eyeframe = faceframe[ye:ye+he, xe:xe+we]
                dotness = convolve(np.sum(eyeframe, axis=2), blobfinder, mode="constant", cval=0)
                pupil = np.int32(np.unravel_index(np.argmin(dotness), dotness.shape))
                eyelr.append(pupil[1])
                dotlr.append(dotpos[0])
                eyeud.append(pupil[0])
                dotud.append(dotpos[1])
                if len(dotud) > 3:
                    mlr, clr, rlr = [*linregress(eyelr, dotlr)][:3]  # (x, y) -> y = mx + c -> (m, c)
                    mud, cud, rud = [*linregress(eyeud, dotud)][:3]
                    maybepos = np.int32([(pupil[1] * mlr) + clr, (pupil[0] * mud) + cud])
                    print("[({},{}) {}] [({},{}) {}] {} {}".format(mlr, clr, rlr, mud, cud, rud, maybepos, dotpos))
                    print(np.var(eyelr), np.var(eyeud))
                    for k in range(len(dotud)):
                        pygame.draw.circle(screen, (255, 0, 0), (dotlr[k], eyelr[k] * 10), 5)
                        pygame.draw.circle(screen, (0, 255, 0), (eyeud[k] * 10, dotud[k]), 5)
                    pygame.draw.circle(screen, 255, maybepos, 10)
                cv2.circle(eyeframe, tuple(pupil[::-1]), 6, (255, 0, 255))
                # cv2.imshow("Face%s Eye%s" % (i, j), eyeframe)
                cv2.rectangle(faceframe, (xe, ye), (xe + we, ye + he), 0)
            pygame.display.flip()
            sleep(0.1)
            # cv2.imshow("Face%s" % i, faceframe)
            cv2.rectangle(frame, (xf, yf), (xf + wf, yf + hf), 0)
        cv2.imshow("Full", frame)
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                cap.release()
                quit()
        elif e.type == KEYUP:
            keys.discard(e.key)
    cycles += 1
cap.release()
