# Because he asked me to ;)

import pygame
from pygame.locals import *
import numpy as np
import random
import glob
import time

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

textfont = pygame.font.Font(None, 50)
smolfont = pygame.font.Font(None, 20)

keys = set()

COL_WHITE = (255, 255, 255)
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_CYAN = (0, 255, 255)
COL_MAGENTA = (255, 0, 255)
COL_ORANGE = (255, 200, 0)
COL_WAHPURPLE = (84, 6, 116)
COL_WAHYELLOW = (255, 242, 0)

S_READY = -1
S_MAP_OUTWARD = 0
S_FIELD_INIT = 1
S_FIELD_MAIN = 2
S_MAP_HOMEWARD = 3
S_SCORE = 4


def drawwahorb(surface, pos, rad):
    pygame.draw.circle(surface, COL_WAHPURPLE, pos, int(rad))
    pygame.draw.rect(surface, COL_WAHYELLOW, pygame.Rect(*(pos - rad / 2), rad, rad / 3))
    pygame.draw.rect(surface, COL_WAHYELLOW, pygame.Rect(*(pos - rad / 2), rad / 3, rad * 1.2))


wahsounds = [pygame.mixer.Sound(file) for file in glob.glob(r"D:\Users\Charles Turvey\Music\SFX\Waluigi\Wahs\Wah*.wav")]
wahtexts = [smolfont.render(wahtext, True, COL_WHITE, (0, 0, 0)) for wahtext in ["Wwwah!",
                                                                                 "Wwahhh!",
                                                                                 "Wwwwah-haaa!",
                                                                                 "Wah-ha-haa!",
                                                                                 "Wah-haa!",
                                                                                 "Waaah!"]]
wahs = []


class Wah:
    def __init__(self, pos, wahid):
        self.wahid = wahid
        pygame.mixer.find_channel(True).play(wahsounds[self.wahid])
        self.pos = np.float32(pos.copy()) - np.float32(wahtexts[self.wahid].get_size())/2 + (0, 20)
        self.pos[0] = min(max(self.pos[0], 0), w - wahtexts[self.wahid].get_width())
        self.wahstart = time.time()
        wahs.append(self)

    def show(self):
        if time.time() - self.wahstart < 1.5:
            screen.blit(pygame.transform.rotate(wahtexts[self.wahid], (0.5 - random.random()) * 10), self.pos)
        else:
            wahs.remove(self)
            del self


simulations = []


class Simulation:
    # Each of these will house a predator, a home-site path, and a field of prey
    # Should function as state machines, and display as square displays
    def __init__(self, width, pos, pathlength, simid):
        # General variables
        self.simid = simid
        self.state = S_READY
        self.foreground = pygame.Surface((width, width))
        self.background = pygame.Surface((width, width))
        self.background.fill(0)
        self.imagesize = np.int32((width, width))
        self.pos = np.float32(pos)

        # Variables used in Map scene
        self.map_pred_pos = 0
        self.map_path_time = pathlength
        self.map_timer = 0

        # Variables used in Field scene
        self.field_prey_pos = None
        self.field_prey_vel = None
        self.field_prey_init_no = 100
        self.field_prey_eaten = 0
        self.field_pred_pos = self.imagesize/2
        self.field_pred_vel = np.float32((0, 0))
        self.field_pred_eating = 0
        self.field_timer = 0
        self.field_time_limit = 10000
        self.field_time_record = []
        self.field_energy_record = []
        self.field_efficiency_record = []

        simulations.append(self)

    def update(self):
        # Run once per global cycle for all Simulations
        # Runs the code for moving along the frame depending on the current state
        # Changes state if necessary
        if self.state == S_READY:
            if K_SPACE in keys:
                Wah(self.pos + self.imagesize/2, 2)
                self.state = S_MAP_OUTWARD

        elif self.state == S_MAP_OUTWARD:
            self.map_timer += 1
            # Predator moves along map path toward field
            self.map_pred_pos += 1
            if self.map_pred_pos >= self.map_path_time:
                self.state = S_FIELD_INIT

        elif self.state == S_FIELD_INIT:
            self.field_prey_pos = np.random.random_sample((self.field_prey_init_no, 2)) * self.imagesize
            self.field_prey_vel = 1 - (2 * np.random.random_sample((self.field_prey_init_no, 2)))
            # print(self.field_prey_pos.shape, self.field_prey_vel.shape)
            self.field_pred_pos = self.imagesize/2
            self.field_pred_vel = 4 * np.sin(np.float32([0, np.pi/2]) + (np.pi * np.random.random() * 2))
            self.field_timer = 0
            self.field_prey_eaten = 0
            self.field_time_record = []
            self.field_energy_record = []
            self.field_efficiency_record = []
            self.state = S_FIELD_MAIN
            self.background.fill(0)

        elif self.state == S_FIELD_MAIN:
            if self.field_timer < self.field_time_limit:
                self.map_timer += 1
                # Record data for data and display
                self.field_time_record.append(self.field_timer + (self.map_path_time * 2))
                self.field_energy_record.append(self.field_prey_eaten)
                self.field_efficiency_record.append(self.field_energy_record[-1] / self.field_time_record[-1])
                # Have the prey flee the predator slightly
                diffs = self.field_prey_pos - self.field_pred_pos
                dists = np.linalg.norm(diffs, axis=1)
                norms = (diffs.T / ((dists + 1) * 100)).T  # N.B. not actually normalised
                self.field_prey_vel += norms
                # Move the prey, find which ones would leave the box, and crudely bounce them back in
                self.field_prey_pos += self.field_prey_vel
                outsides = (self.field_prey_pos < 0) | (self.field_prey_pos > self.imagesize[0])
                self.field_prey_pos[outsides] = np.minimum(np.maximum(self.field_prey_pos[outsides], 0), self.imagesize[0])
                self.field_prey_vel[outsides] *= -1
                # Move predator, detect collision of predator with prey, and enact consumption procedure
                if self.field_pred_eating == 0:
                    self.field_pred_pos += self.field_pred_vel
                    outsides = (self.field_pred_pos < 0) | (self.field_pred_pos > self.imagesize[0])
                    self.field_pred_pos[outsides] = np.minimum(np.maximum(self.field_pred_pos[outsides], 0), self.imagesize[0])
                    self.field_pred_vel[outsides] *= -1
                    if dists.shape[0] != 0:
                        if np.min(dists) < 15:
                            self.field_prey_eaten += 1
                            i = np.argmin(dists)
                            Wah(self.field_prey_pos[i] + self.pos, self.simid)
                            self.field_prey_pos = np.delete(self.field_prey_pos, i, 0)
                            self.field_prey_vel = np.delete(self.field_prey_vel, i, 0)
                            self.field_pred_eating = 50
                else:
                    self.field_pred_eating -= 1
                self.field_timer += 1
            else:
                i = np.argmax(self.field_efficiency_record)
                pygame.draw.line(self.background, COL_CYAN,
                                 (0, self.imagesize[1]),
                                 (self.field_time_record[i] / 50,
                                  self.imagesize[1] - self.field_energy_record[i] * 4), 2)
                pygame.draw.line(self.background, COL_GREEN,
                                 (0, self.imagesize[1] - self.field_efficiency_record[i] * 7000),
                                 (self.imagesize[0], self.imagesize[1] - self.field_efficiency_record[i] * 7000), 1)
                pygame.draw.line(self.background, COL_GREEN,
                                 (self.field_time_record[i] / 100, 0),
                                 (self.field_time_record[i] / 100, self.imagesize[1]), 1)
                self.state = S_MAP_HOMEWARD

        elif self.state == S_MAP_HOMEWARD:
            self.map_timer += 1
            # Predator moves along map path toward home
            self.map_pred_pos -= 1
            if self.map_pred_pos <= 0:
                self.state = S_SCORE

        elif self.state == S_SCORE:
            pass

        else:
            pass

    def show(self):
        # Blits the Simulation to the screen (located by its own position?)
        # Allows the Simulation to be blitted multiple times without updating
        if self.state == S_READY:
            self.foreground.fill(0)
            self.foreground.blit(textfont.render("READY!", True, COL_WHITE), (0, 10))

        elif self.state in [S_MAP_OUTWARD, S_MAP_HOMEWARD]:
            self.foreground.fill(0)
            pathbeginpos = np.int32(self.imagesize / 2 + (-self.map_pred_pos * 2, 0))
            pathendpos = np.int32(self.imagesize / 2 + ((self.map_path_time - self.map_pred_pos) * 2, 0))
            pygame.draw.line(self.foreground, COL_WHITE, pathbeginpos, pathendpos, 20)
            for i in range(pathbeginpos[0] + 100, pathendpos[0], 100):
                if 0 <= i < self.imagesize[0]:
                    pygame.draw.line(self.foreground, COL_GREEN,
                                     (i, 50), (i, self.imagesize[1] - 50), 5)
            pygame.draw.circle(self.foreground, COL_CYAN, pathbeginpos, 30)
            pygame.draw.circle(self.foreground, COL_MAGENTA, pathendpos, 30)
            drawwahorb(self.foreground, np.int32(self.imagesize / 2), 20)
            self.foreground.blit(textfont.render(str(self.map_timer), True, COL_GREEN), (self.imagesize[0] / 2, 10))

        elif self.state == S_FIELD_MAIN:
            if len(self.field_energy_record) > 0:
                pygame.draw.circle(self.background, COL_ORANGE,
                                   np.int32((self.field_time_record[-1] / 100,
                                             self.imagesize[1] - 7000 * self.field_efficiency_record[-1])), 1)
                pygame.draw.circle(self.background, COL_MAGENTA,
                                   np.int32((self.field_time_record[-1] / 100,
                                             self.imagesize[1] - self.field_energy_record[-1] * 2)), 1)
            self.foreground.blit(self.background, (0, 0))
            if len(self.field_energy_record) > 1:
                pygame.draw.line(self.foreground, COL_CYAN,
                                 (0, self.imagesize[1]),
                                 (self.field_time_record[-1] / 50,
                                  self.imagesize[1] - self.field_energy_record[-1] * 4), 2)
                i = np.argmax(self.field_efficiency_record)
                pygame.draw.line(self.foreground, COL_CYAN,
                                 (0, self.imagesize[1]),
                                 (self.field_time_record[i] / 50,
                                  self.imagesize[1] - self.field_energy_record[i] * 4), 2)
                pygame.draw.line(self.foreground, COL_GREEN,
                                 (0, self.imagesize[1] - self.field_efficiency_record[i] * 7000),
                                 (self.imagesize[0], self.imagesize[1] - self.field_efficiency_record[i] * 7000), 1)
                pygame.draw.line(self.foreground, COL_GREEN,
                                 (self.field_time_record[i] / 100, 0),
                                 (self.field_time_record[i] / 100, self.imagesize[1]), 1)
            for prey_pos in self.field_prey_pos:
                pygame.draw.circle(self.foreground, COL_WHITE, np.int32(prey_pos), 5)
            drawwahorb(self.foreground, np.int32(self.field_pred_pos), 10)
            self.foreground.blit(textfont.render(str(self.field_time_limit - self.field_timer), True, COL_RED),
                                 (0, 10))
            self.foreground.blit(textfont.render(str(self.map_timer), True, COL_GREEN), (self.imagesize[0] / 2, 10))

        elif self.state == S_SCORE:
            self.foreground.blit(self.background, (0, 0))
            self.foreground.blit(textfont.render(str(self.map_timer), True, COL_GREEN), (self.imagesize[0] / 2, 10))

        else:
            pass

        screen.blit(self.foreground, self.pos)


Q = Simulation(w/2, (0, 0), 1000, 0)
R = Simulation(w/2, (w/2, 0), 2000, 1)
S = Simulation(w/2, (0, w/2), 3000, 4)
T = Simulation(w/2, screensize/2, 4000, 5)

while True:
    screen.fill(0)
    for S in simulations:
        S.update()
        S.show()
    for W in wahs:
        W.show()
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type == KEYUP:
            keys.discard(e.key)
