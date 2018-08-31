import socket, threading
import cv2
import numpy as np

print_lock = threading.Lock()


def receiving():
    while True:
        data = s.recv(4096)
        with print_lock:
            print(data.decode("utf-8"))


addr = ("127.0.0.1", 9001)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

broken = True
while broken:
    try:
        s.connect(addr)
        broken = False
        print("Connected up :)")
    except:
        print("Nope")

debug = False

img = np.rot90(cv2.imread(r"D:\Users\Charles Turvey\Pictures\Art\Hand\Hand.jpg"))
imgsize = img.shape[:2]
imgcorners = np.float32([[0,0], [imgsize[1], 0], imgsize[::-1], [0, imgsize[0]]])

frontcap = cv2.VideoCapture(0)
_, frontframe = frontcap.read()
frontframesize = np.float32(frontframe.shape[1::-1])
frontframecentre = np.float32(frontframesize/2)

topcap = cv2.VideoCapture(1)
_, topframe = topcap.read()
topframesize = np.float32(topframe.shape[1::-1])
topframecentre = np.float32(topframesize/2)

#fourcc = cv2.VideoWriter_fourcc(*"XVID")  # The protocol used for video
#out = cv2.VideoWriter(r"SavedImages\Test.avi", fourcc, 20, tuple(framesize))

chesssize = (3, 4)  # format is (height - 1, width - 1)


def findchess(cap, name):
    ret, frame = cap.read()
    if ret:
        ret, points = cv2.findChessboardCorners(frame, chesssize)
        if debug:
            cv2.imshow(name, frame)
        if ret:
            corners = np.float32([points[-1, 0], points[-chesssize[0], 0], points[0, 0], points[chesssize[0] - 1, 0]])
            pos = np.mean(corners, 0)
            if debug:
                cv2.line(frame, tuple(corners[0]), tuple(corners[-1]), (0, 255, 0), 10)
                for i in range(3):
                    cv2.line(frame, tuple(corners[i]), tuple(corners[i + 1]), (255, 0, 255), 10)
                cv2.imshow(name, frame)
            return True, pos
    return False, None


handpos = np.float32([0, 0, 0])

receiver = threading.Thread(target=receiving)
receiver.start()

while cv2.waitKey(1) == -1:
    xyret, xypos = findchess(frontcap, "Front")
    xzret, xzpos = findchess(topcap, "Top")
    # print(xypos, xzpos)
    if xyret:
        handpos[1] = 1 - (xypos[1] / frontframecentre[1])
    if xzret:
        handpos[2] = (xzpos[1] / topframecentre[1]) - 1
        if xyret:
            handpos[0] = (2 - (xypos[0] / frontframecentre[0]) - (xzpos[0] / topframecentre[0])) / 2
        else:
            handpos[0] = 1 - (xzpos[0] / topframecentre[0])
    elif xyret:
        handpos[0] = 1 - (xypos[0] / frontframecentre[0])
    data = bytes([255] + [int((i + 1) * 127) for i in handpos])
    # with print_lock:
    #     print(data)
    s.send(data)
    if debug:
        print(handpos)
        showframe = np.zeros((200, 200, 3))
        cv2.circle(showframe, tuple(np.int32((handpos[:2] + 1) * 100)), int((handpos[2] + 1) * 10), (255, 0, 255))
        for i in range(3):
            cv2.putText(showframe, "{:+.2f}".format(handpos[i]), (0, 30 * (i + 1)), 5, 1, (255, 255, 255))
        cv2.imshow("Position", showframe)

frontcap.release()
topcap.release()
cv2.destroyAllWindows()


# import cv2
# import numpy as np
#
# trackcols = [(65.2, 18, 3.3), (61.9, 37.9, 45.9), (53.6, 83.6, 53.6)]
#
# frontcap = cv2.VideoCapture(0)
# _, frontframe = frontcap.read()
# frontframesize = np.array(frontframe.shape[1::-1])
# frontframecentre = np.int32(frontframesize/2)
#
# topcap = cv2.VideoCapture(1)
# _, topframe = topcap.read()
# topframesize = np.array(topframe.shape[1::-1])
# topframecentre = np.int32(topframesize/2)
#
#
# def findcolour(frame, colour):
#     frame = np.float32(frame)
#     colour = np.float32(colour)
#     frame -= colour
#     return np.linalg.norm(frame, axis=2)
#
#
# while cv2.waitKey(1) == -1:
#     frontret, frontframe = frontcap.read()
#     topret, topframe = topcap.read()
#     if frontret and topret:
#         frontelements = [findcolour(frontframe, frontframe[0, 0])]#[findcolour(frontframe, trackcols[i]) for i in range(3)]
#         topelements = [findcolour(topframe, topframe[0, 0])]#[findcolour(topframe, trackcols[i]) for i in range(3)]
#         for i in range(1):
#             frontframe[:, :, :] = 0
#             frontframe[:, :, i] = (1 - frontelements[i])
#             cv2.imshow("Front" + str(i), frontframe)
#             topframe[:, :, :] = 0
#             topframe[:, :, i] = (1 - topelements[i])
#             cv2.imshow("Top" + str(i), topframe)
# frontcap.release()
# topcap.release()
