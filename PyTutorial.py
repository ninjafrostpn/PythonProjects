# Pycharm and other installations (include style)
# What are variables anyway?
# Resources online and off it

# Imported functions and variables
import pygame
from pygame.locals import *
from time import sleep as slep


# How to function at 0512AM
def constrain(val, lo, hi):
    return min(max(lo, val), hi)  # In short


# Good place to start
pygame.init()

screen = pygame.display.set_mode((1000, 500))
w = screen.get_width()
h = screen.get_height()

rect1x = 0
rect1y = 0

rect2x = 0
rect2y = 0

# Maybe start without this
while True:
    screen.fill(0)
    
    keys = pygame.key.get_pressed()
    
    # Need to explain dictionaries
    if keys[K_w]:
        rect1y -= 1
    if keys[K_a]:
        rect1x -= 1
    if keys[K_s]:
        rect1y += 1
    if keys[K_d]:
        rect1x += 1
    
    if keys[K_UP]:
        rect2y -= 1
    if keys[K_LEFT]:
        rect2x -= 1
    if keys[K_DOWN]:
        rect2y += 1
    if keys[K_RIGHT]:
        rect2x += 1

    rect1x = constrain(rect1x, 0, w - 10)
    rect1y = constrain(rect1y, 0, h - 20)
    
    rect2x = constrain(rect2x, 0, w - 10)
    rect2y = constrain(rect2y, 0, h - 20)
    
    
    if pygame.Rect(rect1x, rect1y, 10, 20).colliderect((rect2x, rect2y, 10, 20)):
        pygame.draw.rect(screen, (255, 0, 255), (rect1x, rect1y, 10, 20), 1)
        pygame.draw.rect(screen, (255, 0, 0), (rect2x, rect2y, 10, 20), 1)
    else:
        pygame.draw.rect(screen, (255, 0, 255), (rect1x, rect1y, 10, 20))
        pygame.draw.rect(screen, (255, 0, 0), (rect2x, rect2y, 10, 20))
    
    # Do not forget!
    pygame.display.flip()
    
    # Event handling!
    for e in pygame.event.get():
        # Most important
        if e.type == QUIT:
            quit()
        # The kinds of events they put signs up for
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
        if e.type == MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            # Unusual assignments
            rect1x, rect1y = mousepos
            rect2x, rect2y = mousepos
    slep(0.005)
