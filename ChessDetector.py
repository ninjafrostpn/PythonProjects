import cv2
import numpy as np
import serial
from time import sleep

sendable = lambda x: bytes(chr(x), 'utf-8')

cap = cv2.VideoCapture(1)
_, frame = cap.read()
framesize = np.array(frame.shape[1::-1])
framecentre = np.int32(framesize/2)
S = serial.Serial('COM5', 9600)
sleep(5)

ang = 90
S.write(sendable(ang))

while cv2.waitKey(1) == -1:
    ret, frame = cap.read()
    if ret:
        ret, corners = cv2.findChessboardCorners(frame, (7, 7))
        if ret:
            centre = np.mean(corners, axis=0)[0]
            radius = np.max(np.linalg.norm(corners - centre, axis=2))
            cv2.line(frame, tuple(framecentre), tuple(centre), (255, 0, 255))
            cv2.circle(frame, tuple(centre), int(radius), (255, 0, 255))
            print(centre, framecentre)
            if centre[0] < framecentre[0]:
                ang += 1
            if centre[0] > framecentre[0]:
                ang -= 1
            S.write(sendable(ang))
        cv2.imshow("Test", frame)
cap.release()
