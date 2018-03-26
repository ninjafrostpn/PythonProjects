import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1000, 500))

posx = 100
posy = 100

# Draw loop
while True:
    screen.fill(0)
    
    posy += 0.5
    if posy > screen.get_height():
        posy = screen.get_height()
    
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        posx += 1
    if keys[K_LEFT]:
        posx -= 1
    
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
            if e.key == K_DOWN:
                posy += 20
            if e.key == K_UP:
                posy -= 50

    pygame.draw.circle(screen, (255, 0, 255), (int(posx), int(posy)), 10)
    pygame.display.flip()
