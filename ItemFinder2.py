import pygame, threading
from pygame.locals import *
import cv2
import numpy as np

print_lock = threading.Lock()

pygame.init()

largeimagepath = r"D:\Users\Charles Turvey\Pictures\DP Maps\999temp.png"
replacementpath = r"D:\Users\Charles Turvey\Pictures\DP Maps\pc.png"

largeimage = pygame.transform.scale2x(pygame.image.load_extended(largeimagepath))
w = int(largeimage.get_width()/2)
h = int(largeimage.get_height()/2)
largeimage = pygame.transform.smoothscale(largeimage, (w, h))
screen = pygame.display.set_mode((w, h))
largeimage = largeimage.convert_alpha()

replacement = pygame.image.load_extended(replacementpath).convert_alpha()

threshold = 0.8

def findrotatedpositions(target):
    locations = []
    for i in range(0, 360, 10):
        results = cv2.cv2.matchTemplate(pygame.surfarray.pixels3d(largeimage),
                                        pygame.surfarray.pixels3d(pygame.transform.rotate(target, i)),
                                        cv2.TM_CCOEFF_NORMED)
        thresholded = np.where(results >= threshold)
        locations += zip(*(thresholded[::-1]))
    # print(locations)
    return locations

def findpositions(target):
    results = cv2.cv2.matchTemplate(pygame.surfarray.pixels3d(largeimage),
                                    pygame.surfarray.pixels3d(target),
                                    cv2.TM_CCOEFF_NORMED)
    thresholded = np.where(results >= threshold)
    return zip(*(thresholded[::-1]))

def showrect(rectin, fill):
    if fill:
        screen.blit(pygame.transform.scale(replacement, rectin.size), rectin.topleft)
    else:
        pygame.draw.rect(screen, (255, 0, 255), rectin, 1)

chosen = False
selecting = False
selected = False
selectrect = pygame.Rect(0, 0, 0, 0)
locations = []
history = [largeimage]
historypointer = 0
screen.blit(largeimage, (0, 0))
while True:
    if selecting:
        chosen = False
        pos = pygame.mouse.get_pos()
        selectrect[2] = pos[0] - selectrect[0]
        selectrect[3] = pos[1] - selectrect[1]
        screen.blit(history[historypointer], (0, 0))
        showrect(selectrect, False)
    if selected:
        selectrect.normalize()
        screen.blit(history[historypointer], (0, 0))
        showrect(selectrect, chosen)
        if selectrect:
            selected = False
            locations = findpositions(largeimage.subsurface(selectrect))
            for location in locations:
                showrect(pygame.Rect(location[1], location[0], *selectrect.size), chosen)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
            if e.key == K_SPACE:
                chosen = not chosen
                selected = True
            if e.key == K_RETURN:
                historypointer += 1
                history.insert(historypointer, screen.copy())
                history = history[:historypointer + 1]
            if e.key == K_LEFT:
                historypointer = max(0, historypointer - 1)
                selected = True
            if e.key == K_RIGHT:
                historypointer = min(len(history) - 1, historypointer + 1)
                selected = True
            if e.key == K_UP:
                threshold += 0.1
                selected = True
            if e.key == K_DOWN:
                threshold -= 0.1
                selected = True
            print("History: {} of {}, Threshold: {:.1f}".format(historypointer + 1, len(history), threshold))
        elif e.type == MOUSEBUTTONDOWN and not selecting:
            selectrect.topleft = pygame.mouse.get_pos()
            selecting = True
        elif e.type == MOUSEBUTTONUP and selecting:
            selecting = False
            selected = True
