__author__ = 'Charlie'
"""
from time import sleep as slp
def unprint(words="Can you untype a sentence???????"):
    sentenc = input("Type something:\n")
    print("")
    sentlen = len(sentenc)
    for x in range(0, sentlen + 1):
        print("\r%s" % (sentenc[0: sentlen - x]), end="")
        slp(0.5)

unprint()
"""

import colorama as c
c.init()
Bk, Fr, St = c.Back, c.Fore, c.Style
pos = lambda x, y: "\x1b[%d;%dH" % (y, x)
clear = lambda: print("\x1b[2J")

import time as t

size = 1
difficulty = 1
speed = 1

welcome =("""
    Q       Q    /Q=Q=Q=Q   Q            /Q=Q=Q=Q
    Q       Q   Q           Q           Q
    Q   Q   Q   Q=Q=Q=Q=Q   Q           Q
    Q Q/ \Q Q   Q           Q           Q
    Q/     \Q    \Q=Q=Q=Q   Q=Q=Q=Q=Q    \Q=Q=Q=Q
    """)

while True:
    clear()


# python "E:\Program Files\Pycharm\Projects\textED.py"