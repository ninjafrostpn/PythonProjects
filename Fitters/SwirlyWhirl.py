import pygame
from pygame.locals import *
import numpy as np
from scipy.optimize import minimize as sp_minimise
from time import sleep

pygame.init()

deg2rad = np.pi / 180

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()


def motion(args, kwargs={"t": [], "ssq": False, "s_obs": 0}):
    a, b, c = np.reshape(np.float32(args), (3, -1))
    t = kwargs["t"]
    ssq = kwargs["ssq"]
    s_obs = kwargs["s_obs"]
    s_pred = [np.sum(np.float32(a) * np.sin(np.float32([b]) + (np.float32(c) * i * deg2rad))) + 250 for i in t]
    if ssq:
        ssq = np.sum((np.float32(s_obs) - s_pred) ** 2)
        return ssq
    return s_pred


frametstep = 5
targetdisplay = [
    "----- -----  ---- -   -",
    "-       -   -     -   -",
    "-----   -    ---  -----",
    "-       -       - -   -",
    "-     ----- ----  -   -",
]

targetarray = np.bool_([[(i == '-') for i in line] for line in targetdisplay])
targetframe = np.bool_([targetarray[:, i:i+5] for i in range(0, targetarray.shape[1], 6)])
count = np.sum(targetframe, axis=(1, 2))
if not np.all(count == count[0]):
    raise Exception("Inconsistent Point Count" + str(count))
count = count[0]

repeats = 3
targett = np.arange(0, targetframe.shape[0] * repeats) + 8
for i in range(repeats):
    targett[i * targetframe.shape[0]:] += 2
targett *= frametstep
print(targett)

targety, targetx = ((np.float32([np.random.permutation(np.argwhere(frame)) for frame in targetframe]) - 2.5) * 50).T + 250
targetx = np.tile(targetx, (1, repeats))
targety = np.tile(targety, (1, repeats))

terms = 10
params_x = np.zeros((count, terms * 3), dtype="float32")
params_y = np.zeros((count, terms * 3), dtype="float32")
for m in range(count):
    ssq_total = 2000
    while ssq_total > 100 * repeats:
        res_x = sp_minimise(motion, (0.5 - np.random.random_sample(terms * 3)) * 100,
                            args={"t": targett, "ssq": True, "s_obs": targetx[m]},
                            method="Nelder-Mead")
        res_y = sp_minimise(motion, (0.5 - np.random.random_sample(terms * 3)) * 100,
                            args={"t": targett, "ssq": True, "s_obs": targety[m]},
                            method="Nelder-Mead")
        ssq_total = res_x["fun"] + res_y["fun"]
        print(ssq_total)
    print("Victory", m)
    params_x[m] = res_x["x"]
    params_y[m] = res_y["x"]
print(params_x, params_y)

cycles = 0
while True:
    screen.fill(0)
    for m in range(count):
        if abs((cycles % frametstep) - frametstep) < 0.5:
            pygame.draw.circle(screen, (255, 0, 255),
                               [int(motion(params_x[m], {"t": [cycles], "ssq": False, "s_obs": 0})[0]),
                                int(motion(params_y[m], {"t": [cycles], "ssq": False, "s_obs": 0})[0])], 10)
        else:
            pygame.draw.circle(screen, (255, 255, 255),
                               [int(motion(params_x[m], {"t": [cycles], "ssq": False, "s_obs": 0})[0]),
                                int(motion(params_y[m], {"t": [cycles], "ssq": False, "s_obs": 0})[0])], 10)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type == KEYUP:
            keys.discard(e.key)
    cycles += 0.01
    sleep(0.001)
