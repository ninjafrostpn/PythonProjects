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


def motion(args, kwargs={"t": [], "ssq": False, "s_obs": [0, 0]}):
    a, b, c, ra, rb, rc = np.reshape(np.float32(args), (6, -1))
    t = kwargs["t"]
    ssq = kwargs["ssq"]
    if ssq:
        x_pred = [np.sum(a * np.cos((b + (c * i)) * deg2rad)) + 250 for i in t]
        y_pred = [np.sum(a * np.sin((b + (c * i)) * deg2rad)) + 250 for i in t]
        r_pred = [min(max(np.sum(ra * np.sin((rb + (rc * i)) * deg2rad)), 0), 255) for i in t]
        x_obs = kwargs["s_obs"][0]
        y_obs = kwargs["s_obs"][1]
        r_obs = kwargs["s_obs"][2]

        ssq = np.sum((np.float32(x_obs) - x_pred) ** 2)\
            + np.sum((np.float32(y_obs) - y_pred) ** 2)\
            + np.sum((np.float32(r_obs) - r_pred) ** 2)
        return ssq
    x_pred = 250
    y_pred = 250
    for i in range(terms):
        x_next = x_pred + (a[i] * np.cos((b[i] + (c[i] * t)) * deg2rad))
        y_next = y_pred + (a[i] * np.sin((b[i] + (c[i] * t)) * deg2rad))
        pygame.draw.line(screen, (200, 200, 200), np.int32([x_pred, y_pred]), np.int32([x_next, y_next]))
        x_pred = x_next
        y_pred = y_next
    r_pred = min(max(np.sum(ra * np.sin((rb + (rc * t)) * deg2rad)), 0), 255)
    pygame.draw.circle(screen, (r_pred, 0, 255 - r_pred), np.int32([x_pred, y_pred]), 10)
    return x_pred, y_pred, r_pred


frametstep = 1
targetdisplay = [
    "bbbbb rrrrr  rrrr b   b|rrrrr bbbbb  bbbb r   r|",
    "b       r   r     b   b|r       b   b     r   r|",
    "bbbbb   r    rrr  bbbbb|rrrrr   b    bbb  rrrrr|",
    "b       r       r b   b|r       b       b r   r|",
    "b     rrrrr rrrr  b   b|r     bbbbb bbbb  r   r|",
]
palette = {' ': -1, '|': -1, 'b': 0, '-': 127.5, 'r': 255}

colarray = np.float32([[palette[i] for i in line] for line in targetdisplay])
colframe = np.float32([colarray[:, i:i+23] for i in range(0, colarray.shape[1], 24)])
targetframe = colframe >= 0
count = np.sum(targetframe, axis=(1, 2))
print(count)
if not np.all(count == count[0]):
    raise Exception("Inconsistent Point Count" + str(count))
count = count[0]

repeats = 2
targett = np.arange(0, targetframe.shape[0] * repeats) + 2
for i in range(repeats):
    targett[i * targetframe.shape[0]:] += 0
targett *= frametstep
print(targett)

# It works, I promise. Returns a 3 variable x ? arm x ? frame array. Repeats frames ABCD as ABCDABCD..., not AABBCCDD...
targety, targetx, targetr = np.float32(np.concatenate([np.concatenate([np.random.permutation(np.concatenate([np.argwhere(frame),
                                                                                                             np.reshape(colframe[i][frame], (-1, 1))
                                                                                                             ],
                                                                                                            axis=1
                                                                                                            )
                                                                                             ).reshape(1, -1, 3)
                                                                       for i, frame in enumerate(targetframe)
                                                                       ],
                                                                      axis=0
                                                                      )
                                                       for j in range(repeats)
                                                       ], axis=0
                                                      )
                                       ).T
targetx = ((targetx - (23/2)) * 15) + (w/2)
targety = ((targety - (5/2)) * 15) + (h/2)
targets = np.float32([targetx, targety, targetr])
print(targets.shape)

terms = 4
params = np.zeros((count, terms * 6), dtype="float32")
for m in range(count):
    ssq_total = 2000
    while ssq_total > 100 * repeats:
        res = sp_minimise(motion, (0.5 - np.random.random_sample(terms * 6)) * 100,
                          args={"t": targett, "ssq": True, "s_obs": targets[:, m]},
                          method="Nelder-Mead")
        ssq_total = res["fun"]
        print(ssq_total)
    print("Victory", m)
    params[m] = res["x"]
print(params)

cycles = 0
cyclesstep = 0.01
while True:
    screen.fill(0)
    for m in range(count):
        motion(params[m], {"t": cycles, "ssq": False, "s_obs": 0})
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
    cycles += cyclesstep
    if cycles > max(targett) * 1.5 and cyclesstep > -0.01:
        cyclesstep -= 0.0001
        print(cyclesstep)
    if cycles < 0 and cyclesstep < 0.01:
        cyclesstep += 0.0001
        print(cyclesstep)
    sleep(0.001)
