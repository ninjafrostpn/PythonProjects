import cv2
import socket
import threading
import numpy as np
from time import sleep

homeaddr = ("192.168.0.30", 9001)
framelock = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(homeaddr)

frame = np.zeros((480, 640, 3), dtype=np.uint8)

def receiving():
    rawdata = bytes()
    while True:
        rawdata += s.recv(921600)
        if len(rawdata) >= 921600:
            rawdata, framedata = rawdata[921600:], rawdata[:921600]
            frame[:] = np.frombuffer(framedata, dtype=np.uint8).reshape(480, 640, 3)

receiver = threading.Thread(target=receiving)
receiver.start()

while cv2.waitKey(1) == -1:
    cv2.imshow("frame2", frame)

cv2.destroyAllWindows()
