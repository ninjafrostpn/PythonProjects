import cv2
from math import radians, cos, sin
import numpy as np
from random import randrange as rand

res = (1920, 1080)
w = 800
h = 500

allcolours = set()
palette = []
maxdepth = 400

cv2.namedWindow("")
winpos = [0, 0]
cv2.moveWindow("", *winpos)


def col2num(r, g, b):
    return (r << 4) + (g << 2) + b


def followmouse(event, x, y, flags, param):
    winpos[0] += int(x - w/2)
    winpos[1] += int(y - h/2)
    cv2.moveWindow("", *winpos)
    

# cv2.setMouseCallback("", followmouse)


class Image:
    def __init__(self, image, depthmask, alphamask=True):
        self.depthmask = depthmask
        self.alphamask = alphamask
        self.colours = [tuple(colour) for colour in np.unique(image.reshape(-1, 3), axis=0)]
        self.colourmask = np.zeros(image.shape[:2], dtype='uint8')
        for colour in self.colours:
            print(colour)
            if colour not in allcolours:
                allcolours.add(colour)
                palette.append(colour)
            colourpos = (image == colour)[:, :].any(axis=2)
            colourindex = palette.index(colour)
            self.colourmask[colourpos] = colourindex
        self.w, self.h = self.colourmask.shape[:2]
        
    def render(self, x, y, z=0.0):
        intx, inty = int(x), int(y)
        destlft, desttop = min(max(intx, 0), w), min(max(inty, 0), h)
        destrgt, destbtm = min(max(intx + self.w, 0), w), min(max(inty + self.h, 0), h)
        srclft, srctop = destlft - intx, desttop - inty
        srcrgt, srcbtm = destrgt - intx, destbtm - inty
        
        currscreendepth = screendepth[destlft:destrgt, desttop:destbtm]
        currdepthmask = self.depthmask[srclft:srcrgt, srctop:srcbtm]
        currscreen = screen[destlft:destrgt, desttop:destbtm]
        currcolourmask = self.colourmask[srclft:srcrgt, srctop:srcbtm]
        curralphamask = self.alphamask[srclft:srcrgt, srctop:srcbtm]
        drawpixels = (currscreendepth > (currdepthmask + z)) & curralphamask
        
        currscreendepth[drawpixels] = currdepthmask[drawpixels] + z
        currscreen[drawpixels] = np.array(palette)[currcolourmask[drawpixels]]


imagealpha = np.ones((40, 40), dtype='bool')
imagealpha[10:21, 10:21] = 0
imagedepth = np.zeros((40, 40), dtype='float64')
squareno = 17
squares = []
for i in range(squareno):
    imagecolour = np.ones((40, 40, 3), dtype='uint32')
    imagecolour[:, :] = (rand(256), rand(256), rand(256))
    squares.append(Image(imagecolour, imagedepth, imagealpha))

imagealpha = np.ones((80, h - 50), dtype='bool')
imagedepth = np.zeros((80, h - 50), dtype='float64')
imagecolour = np.ones((80, h - 50, 3), dtype='uint32')
imagecolour[:, :] = (rand(256), rand(256), rand(256))
tower = Image(imagecolour, imagedepth, imagealpha)


cycles = 0
while cv2.waitKey(10) == -1:
    screendepth = np.zeros((w, h), dtype='float64')
    screendepth[:, :] = maxdepth
    screen = np.zeros((w, h, 3), dtype='uint8')  # float means colour values go from 0-1, int goes from 0-255
    for i, I in enumerate(squares):
        I.render(w/2 + (squareno * 20 * cos(radians(cycles + (i * (360/squareno))))) - 20,
                 h/2 + (squareno * 10 * cos(radians(cycles*2 + (i * (360/squareno))))) - 20,
                 squareno * 20 * sin(radians(cycles + (i * (360/squareno)))) - 20)
        I.render(w/2 + (squareno * 10 * cos(radians(cycles + (i * (360/squareno))))) - 20,
                 h/2 - (squareno * 5 * cos(radians(cycles*2 + (i * (360/squareno))))) - 20,
                 -squareno * 10 * sin(radians(cycles + (i * (360/squareno)))) - 20)
    tower.render(w/2 - 40, 50)
    cv2.imshow("", np.rot90(np.fliplr(screen)))
    cycles += 1
print("Nooooo...")
