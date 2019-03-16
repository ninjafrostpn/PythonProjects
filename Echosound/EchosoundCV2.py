import cv2
import numpy as np

K_ESC = 27

w, h = 500, 500
wavescreen = np.zeros([w, h], dtype="float32")
screen = np.zeros([w, h, 3], dtype="uint8")
screensize = np.float32((w, h))
screencorners = np.int32([(0, 0), (0, h), (0, w), (w, h)])

circles = []


class EnergyCircle:
    def __init__(self, pos, energy):
        self.r = 1
        self.pos = np.float32(pos)
        self.energy = energy
        self.spreadenergy = self.energy / (self.r ** 2)
        self.maxr = np.max(np.linalg.norm(self.pos - screencorners, axis=1))

    def update(self):
        self.r += 1
        if self.r > self.maxr or abs(self.spreadenergy) < 0.001:
            circles.remove(self)
        else:
            self.spreadenergy = self.energy / (self.r ** 2)
        blank = np.zeros(wavescreen.shape[:2], dtype="float32")
        if self.energy > 0:
            cv2.circle(blank, tuple(self.pos), self.r, self.spreadenergy, 2)
            wavescreen[:, :] += blank
        else:
            cv2.circle(blank, tuple(self.pos), self.r, -self.spreadenergy, 2)
            wavescreen[:, :] -= blank


class CircleGenerator:
    def __init__(self, pos):
        self.pos = np.float32(pos)

    def update(self, cycles):
        cv2.circle(screen, tuple(self.pos), 3, 1, -1)
        if (0 <= (cycles % 100) < 30) and (cycles % 2 == 0):
            circles.append(EnergyCircle(self.pos, np.sin(t * 30 * (np.pi / 180)) * 10))


class Reflector:
    def __init__(self, pos):
        self.pos = np.float32(pos)

    def update(self):
        cv2.circle(screen, tuple(self.pos), 3, 1)
        val = wavescreen[int(self.pos[1]), int(self.pos[0])]
        if val != 0:
            circles.append(EnergyCircle(self.pos, -val))


generators = [CircleGenerator((w / 2 + 30 * i, h / 2)) for i in range(-2, 3)]
R = Reflector((w/2, h * 0.7))

t = 0
while True:
    wavescreen[:] = 0
    screen[:] = 0
    for G in generators:
        G.update(t)
    for C in circles:
        C.update()
    R.update()
    t += 1
    screen[:, :, 0][wavescreen <= 0] += np.uint8(np.log(np.abs(wavescreen[wavescreen <= 0]) / 1000))
    screen[:, :, 1][wavescreen >= 0] += np.uint8(np.log(wavescreen[wavescreen >= 0] / 1000))
    cv2.imshow("Echo...", screen)
    k = cv2.waitKeyEx(1)
    if k == K_ESC:
        break
