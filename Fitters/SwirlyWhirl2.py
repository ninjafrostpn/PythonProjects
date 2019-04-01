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
    a, b, c = np.reshape(np.float32(args), (3, -1))
    t = kwargs["t"]
    ssq = kwargs["ssq"]
    if ssq:
        x_pred = [np.sum(a * np.cos(b + (c * i * deg2rad))) + 250 for i in t]
        y_pred = [np.sum(a * np.sin(b + (c * i * deg2rad))) + 250 for i in t]
        x_obs = kwargs["s_obs"][0]
        y_obs = kwargs["s_obs"][1]
        ssq = np.sum((np.float32(x_obs) - x_pred) ** 2) + np.sum((np.float32(y_obs) - y_pred) ** 2)
        return ssq
    x_pred = 250
    y_pred = 250
    for i in range(terms):
        x_next = x_pred + (a[i] * np.cos(b[i] + (c[i] * t * deg2rad)))
        y_next = y_pred + (a[i] * np.sin(b[i] + (c[i] * t * deg2rad)))
        pygame.draw.line(screen, (200, 200, 200), np.int32([x_pred, y_pred]), np.int32([x_next, y_next]))
        x_pred = x_next
        y_pred = y_next
    return x_pred, y_pred


frametstep = 5
targetdisplay = [
    "----- -----  ---- -   -|           -------   --|        -------   --   |     -------   --      |  -------   --         ",
    "-       -   -     -   -|          -- ------ -- |       -- ------ --    |    -- ------ --       | -- ------ --          ",
    "-----   -    ---  -----|         ------------- |      -------------    |   -------------       |-------------          ",
    "-       -       - -   -|          --------- -- |       --------- --    |    --------- --       | --------- --          ",
    "-     ----- ----  -   -|           -------   --|        -------   --   |     -------   --      |  -------   --         ",
]

targetarray = np.bool_([[(i == '-') for i in line] for line in targetdisplay])
targetframe = np.bool_([targetarray[:, i:i+23] for i in range(0, targetarray.shape[1], 24)])
count = np.sum(targetframe, axis=(1, 2))
print(count)
if not np.all(count == count[0]):
    raise Exception("Inconsistent Point Count" + str(count))
count = count[0]

repeats = 1
targett = np.arange(0, targetframe.shape[0] * repeats) + 10
for i in range(repeats):
    targett[i * targetframe.shape[0]:] += 2
targett *= frametstep
print(targett)

targety, targetx = np.float32([np.concatenate([np.random.permutation(np.argwhere(frame)) for i in range(repeats)],
                                              axis=0)
                               for frame in targetframe]).T
targetx = ((targetx - (23/2)) * 15) + (w/2)
targety = ((targety - (5/2)) * 15) + (h/2)
targets = np.float32([targetx, targety])

terms = 5
params = np.zeros((count, terms * 3), dtype="float32")
for m in range(count):
    ssq_total = 2000
    while ssq_total > 100 * repeats:
        res = sp_minimise(motion, (0.5 - np.random.random_sample(terms * 3)) * 100,
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
        if abs((cycles % frametstep) - frametstep) < 0.1:
            pygame.draw.circle(screen, (255, 0, 255),
                               np.int32(motion(params[m], {"t": cycles, "ssq": False, "s_obs": 0})), 10)
        else:
            pygame.draw.circle(screen, (255, 255, 255),
                               np.int32(motion(params[m], {"t": cycles, "ssq": False, "s_obs": 0})), 10)
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
