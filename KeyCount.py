__author__ = 'Charlie'

# may miscount if buttons held...

import win32api as w
import time as t

entry = dict()
j = 0x41
while j <= 0x5A:
    entry[str(j)] = 0
    w.WriteProfileVal("letters A-Z", str(j), 0, "E:\Program Files\Pycharm\Projects\storage.moo")
    w.GetAsyncKeyState(j)
    j += 1

while True:
    i = 0x41
    while i <= 0x5A:
        status = w.GetAsyncKeyState(i)
        if status != 0:
            entry[str(i)] += 1
            w.WriteProfileVal("letters A-Z", str(i), entry[str(i)], "E:\Program Files\Pycharm\Projects\storage.moo")
        i += 1
    t.sleep(0.1)