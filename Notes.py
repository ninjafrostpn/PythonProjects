import pygame
from pygame.locals import *
import numpy as np
from time import sleep

WHITE = (255, 255, 255)

pygame.init()

w, h = 1000, 400
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()

notesoutside = 10
notespacing = h / (8 + (notesoutside * 2))


class Note:
    def __init__(self, pitch):
        self.pitch = pitch
        self.rect = pygame.Rect(w,
                                h/2 - notespacing * (self.pitch + 1),
                                notespacing * 2.6,
                                notespacing * 2)
    
    def show(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right <= 0:
            return True
        pygame.draw.ellipse(screen, 0, self.rect)
        if self.pitch > 0:
            pygame.draw.line(screen, 0,
                             (self.rect.left + 3, self.rect.centery),
                             (self.rect.left + 3, self.rect.centery + (notespacing * max(6, self.pitch))),
                             3)
        else:
            pygame.draw.line(screen, 0,
                             (self.rect.right - 3, self.rect.centery),
                             (self.rect.right - 3, self.rect.centery - (notespacing * max(6, -self.pitch))),
                             3)
        if self.pitch >= 6:
            for i in range(6, self.pitch + 1, 2):
                pygame.draw.line(screen, 0,
                                 (self.rect.centerx - (self.rect.width * 0.75), h/2 - (i * notespacing)),
                                 (self.rect.centerx + (self.rect.width * 0.75), h/2 - (i * notespacing)),
                                 3)
        if self.pitch <= -6:
            for i in range(6, 1 - self.pitch, 2):
                pygame.draw.line(screen, 0,
                                 (self.rect.centerx - (self.rect.width * 0.75), h/2 + (i * notespacing)),
                                 (self.rect.centerx + (self.rect.width * 0.75), h/2 + (i * notespacing)),
                                 3)


notes = [Note(0)]

paused = False
cycles = 1
while True:
    if not paused:
        screen.fill(WHITE)
        for i in range(5):
            pygame.draw.line(screen, 0,
                             (0, h/2 + ((i - 2) * notespacing * 2)),
                             (w, h/2 + ((i - 2) * notespacing * 2)))
        if cycles % 70 == 0:
            notes.append(Note(max(-11, min(notes[-1].pitch + np.random.choice([-1, 1, -2, 2]), 8))))
        n = 0
        while n < len(notes):
            N = notes[n]
            if N.show():
                notes.remove(N)
            else:
                n += 1
        pygame.draw.line(screen, (255, 0, 0), (w/2, 0), (w/2, h), 3)
        pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
            if e.key == K_SPACE:
                paused = not paused
        elif e.type == KEYUP:
            keys.discard(e.key)
    sleep(0.01)
    cycles += 1
