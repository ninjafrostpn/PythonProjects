import cv2
import numpy as np

cap = cv2.VideoCapture(0)
_, frame = cap.read()
framesize = np.array(frame.shape[1::-1])
framecentre = np.int32(framesize/2)
squaretoplft = tuple(np.int32(framesize * 0.4))
squarebtmrgt = tuple(np.int32(framesize * 0.6))
coordmat = np.int32([[(i, j) for j in range(framesize[1])] for i in range(framesize[0])])

while True:
    while cv2.waitKey(1) == -1:
        ret, frame = cap.read()
        if ret:
            showframe = frame.copy()
            cv2.rectangle(showframe, squaretoplft, squarebtmrgt, (255, 0, 255), 1)
            cv2.imshow("Original", showframe)

    fullcolavg = np.average(np.average(frame, axis=0), axis=0)
    calsample = frame[squaretoplft[0]: squarebtmrgt[0],
                      squaretoplft[1]: squarebtmrgt[1]]
    calcolavg = np.average(np.average(calsample - fullcolavg, axis=0), axis=0)
    caldists = np.average(np.average(np.abs((calsample - fullcolavg) - calcolavg), axis=0), axis=0)
    print("Central colour:          ", calcolavg)
    print("Allowed colour variation:", caldists)

    while cv2.waitKey(1) == -1:
        ret, frame = cap.read()
        if ret:
            fullcolavg = np.average(np.average(frame, axis=0), axis=0)
            calmask = np.all(np.abs((frame - fullcolavg) - calcolavg) < caldists, axis=2)
            cv2.imshow("Original", frame)
            frame[~calmask] = 0
            cv2.imshow("Masked", frame)

cap.release()
