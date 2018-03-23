import numpy as np
import cv2
import pygame
from pygame.locals import *
from time import time

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("SavedImages/{:.0f}.avi".format(time()), fourcc, 30, (640, 480))

pygame.init()
pygame.display.set_caption("Camera-Vision")
screen = pygame.display.set_mode((740, 480))

camon = True
while camon:
    ret, frame = cap.read()
    if ret:
        # cv2.imshow('frame', frame)
        out.write(frame)
        pframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pframe = np.rot90(np.fliplr(pframe))
        # print(pframe.shape)
        pframe = pygame.surfarray.make_surface(pframe)
        # print(pframe.get_size())
        screen.blit(pframe, (0, 0))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == QUIT:
                camon = False
            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    cv2.imwrite("SavedImages/{:.0f}.png".format(time()), frame)
                if e.key == K_ESCAPE:
                    camon = False

cap.release()
out.release()
cv2.destroyAllWindows()
