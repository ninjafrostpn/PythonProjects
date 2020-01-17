import numpy as np
from time import sleep
import win32api as wa
import win32gui as wg

prevpos = np.int32(wg.GetCursorInfo()[2])
vel = np.zeros(2, "int32")
while True:
    newpos = np.int32(wg.GetCursorInfo()[2])
    if np.any(newpos != prevpos):
        vel = newpos - prevpos
    else:
        vel += [0, 1]
        nextpos = prevpos + vel
        wa.SetCursorPos(nextpos)
        newpos = np.int32(wg.GetCursorInfo()[2])
        hits = (newpos != nextpos)
        while np.any(hits):
            vel[hits] = np.int32(vel[hits] * -0.9)
            vel[~hits] = np.int32(vel[~hits] * 0.9999)
            nextpos[hits] -= nextpos[hits] - newpos[hits]
            wa.SetCursorPos(nextpos)
            newpos = np.int32(wg.GetCursorInfo()[2])
            hits = (newpos != nextpos)
    prevpos[:] = newpos[:]
    sleep(0.01)
