__author__ = 'Charlie'
import time as t
import win32api as w
import ctypes as c
import math as m

j = 0


def clicked(*values):
    correct = True
    for i in range(0, len(values)):
        if w.GetAsyncKeyState(values[i]) >= 0:
            correct = False
    return correct

while True:
    ctrl = 0x11   # finds state of ctrl key
    shift = 0x10  # and then the shift key
    vold = 0xAE   # the volume down key
    volu = 0xAF   # the volume up key
    f2 = 0x71     # the f2 key
    f10 = 0x79    # the f10 key
    mute = 0xAD   # mute/unmute key
    vkQ = 0x52    # Q key

    if clicked(ctrl, vold) or clicked(ctrl, volu):
        print("MUTED/UNMUTED")
        w.keybd_event(mute, mute)  # simulates mute/unmute key press
        t.sleep(0.3)
    elif clicked(ctrl, f2) and False:  # currently inactive quit prevention
        w.keybd_event(shift, shift)
        w.keybd_event(f10, f10)
        t.sleep(0.3)