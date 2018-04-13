import numpy as np
import pygame
from pygame.locals import *
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils.np_utils import to_categorical

pygame.init()

# Plan:
# Two balls, one controlled by player, one controlled by AI
# Player moves ball with arrow keys, and data are recorded as follows:
# - relative (x,y) position of AI ball in past n cycles up to and including present, as 2n values
# - which of four arrow keys are currently pressed
# The former 2n data points are fed to the inputs, and the latter four as outputs, for training the neural net
# (This could perhaps be done at regular intervals, if it can't be done continuously)
# The neural net is fed the relative (x,y) position of the player ball over the last n cycles
# The output of said neural net is interpreted as keypresses
# We dance!

screen = pygame.display.set_mode((500, 500))
w = screen.get_width()
h = screen.get_height()

while True:
    screen.fill(0)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
