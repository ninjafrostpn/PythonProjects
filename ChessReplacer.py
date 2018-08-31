import cv2
import numpy as np

debug = False

img = np.rot90(cv2.imread(r"D:\Users\Charles Turvey\Pictures\Art\Hand\Hand.jpg"))
imgsize = img.shape[:2]
imgcorners = np.float32([[0,0], [imgsize[1], 0], imgsize[::-1], [0, imgsize[0]]])

cap = cv2.VideoCapture(0)#r"D:\Users\Charles Turvey\Videos\WIN_20180511_14_16_04_Pro.mp4")
_, frame = cap.read()
framesize = np.array(frame.shape[1::-1])
framecentre = np.int32(framesize/2)

fourcc = cv2.VideoWriter_fourcc(*"XVID")  # The protocol used for video
out = cv2.VideoWriter(r"SavedImages\Test.avi", fourcc, 20, tuple(framesize))

chesssize = (3, 4)  # format is (height - 1, width - 1)

while cv2.waitKey(1) == -1:
    ret, frame = cap.read()
    if ret:
        ret, points = cv2.findChessboardCorners(frame, chesssize)  # TODO: work out why findcirclesgrid exits python
        if ret:
            framesize = frame.shape[:2]
            corners = np.float32([points[-1, 0], points[-chesssize[0], 0], points[0, 0], points[chesssize[0] - 1, 0]])
            M = cv2.getPerspectiveTransform(imgcorners, corners)
            overlay = cv2.warpPerspective(img, M, framesize[::-1], borderValue=(100, 0, 100))
            alphamask = overlay != (100, 0, 100)
            frame[alphamask] = overlay[alphamask]
            if debug:
                centre = np.mean(corners, axis=0)
                radius = np.max(np.linalg.norm(corners - centre, axis=0))
                for corner in corners:
                    cv2.circle(frame, tuple(corner), int(radius/10), 0)
                cv2.line(frame, tuple(framecentre), tuple(centre), (255, 0, 255))
                cv2.circle(frame, tuple(centre), int(radius), (255, 0, 255))
        cv2.imshow("Test", frame)
        out.write(frame)
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
