__author__ = 'Charlie'
from graphics import *
w = GraphWin()
i = 0
while True:
    pt = Point(i, i)
    pt.draw(w)
    i = (i + 1) % 201
