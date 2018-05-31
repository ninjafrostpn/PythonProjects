import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(r'C:\Users\Charles Turvey\AppData\Local\Programs\Python\Python35-32\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
_, frame = cap.read()
framesize = np.array(frame.shape[1::-1])
framecentre = np.int32(framesize/2)

while cv2.waitKey(1) == -1:
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.CV_8U)
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), 0)
        cv2.imshow("Test", frame)
cap.release()
