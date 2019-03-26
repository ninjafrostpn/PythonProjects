import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()

rotatrix = lambda theta: np.sin([[theta + (np.pi/2), -theta],
                                 [theta, theta + (np.pi/2)]])

w, h = 1000, 600
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()

fishno = 500
fishpos = np.random.random_sample((fishno, 2)) * screensize/2
fishdir = np.random.random_sample(fishno) * (np.pi * 2)
fishspd = np.random.random_sample(fishno) * 10
fishvel = (fishspd * np.sin([fishdir + (np.pi / 2), fishdir])).T

repulserad = 30
orientrad = 60
attractrad = 70

repulseresp = 0.2
orientresp = 0.01
attractresp = 0.1

while True:
    screen.fill(0)
    toplftmask = fishpos < repulserad
    btmrgtmask = fishpos > (screensize - repulserad)
    if np.any(toplftmask):
        fishvel[toplftmask] += repulseresp  # / (np.maximum(fishpos[toplftmask], 1) ** 2)
    if np.any(btmrgtmask):
        fishvel[btmrgtmask] -= repulseresp  # / (np.maximum((w - fishpos[btmrgtmask]), 1) ** 2)
    # Use complex numbers and meshgrids to make light of distance calculation
    cfishpos = np.array([complex(*pos) for pos in fishpos])
    m, n = np.meshgrid(cfishpos, cfishpos)
    fishdist = np.float32(abs(m - n))
    # Moves the self-distances beyond the edge of the screen in distance, meaning they are disregarded
    fishdist[np.tri(fishno, dtype="bool") & ~np.tri(fishno, k=-1, dtype="bool")] = w * h
    repulsemask = np.nonzero((fishdist > 0) & (fishdist < repulserad))
    orientmask = np.nonzero((fishdist > repulserad) & (fishdist < orientrad))
    attractmask = np.nonzero((fishdist > orientrad) & (fishdist < attractrad))

    if np.any(repulsemask):
        repulsedist = fishdist.flatten()[np.ravel_multi_index(repulsemask, fishdist.shape)]
        repulsevec = ((fishpos[repulsemask[0]] - fishpos[repulsemask[1]]).T / repulsedist).T * repulseresp
        fishvel[repulsemask[0]] += repulsevec
        fishvel[repulsemask[1]] -= repulsevec

    if np.any(attractmask):
        attractdist = fishdist.flatten()[np.ravel_multi_index(attractmask, fishdist.shape)]
        attractvec = ((fishpos[attractmask[0]] - fishpos[attractmask[1]]).T / attractdist).T * attractresp
        fishvel[attractmask[0]] -= attractvec
        fishvel[attractmask[1]] += attractvec

    if np.any(orientmask):
        # for i in set(orientmask[0]):
        #     orientdist = fishdist[i][orientmask[1][orientmask[0] == i]]
        #     rotation = rotatrix(np.sign(((np.average(fishdir[orientmask[1][orientmask[0] == i]])
        #                                   - fishdir[i]) % (np.pi * 2)) - np. pi)
        #                         * orientresp)
        #     fishvel[i] = rotation.dot(fishvel[i])
        orientamt = np.sign(np.cross(fishvel[orientmask[0]], fishvel[orientmask[1]])) * orientresp
        for i in range(len(orientamt)):
            rotation = rotatrix(orientamt[i])
            fishvel[orientmask[0][i]] = rotation.dot(fishvel[orientmask[0][i]])

    fishspd = np.linalg.norm(fishvel, axis=1)
    fishdir[fishspd > 0] = np.arctan2(fishpos[fishspd > 0][:, 1], fishpos[fishspd > 0][:, 0])
    fishpos += fishvel
    fishpos = np.minimum(np.maximum(fishpos, 0), screensize)
    for i in range(fishno):
        pygame.draw.circle(screen, (255, 0, 255), np.int32(fishpos[i]), 2)
        pygame.draw.line(screen, (255, 255, 255),
                         fishpos[i],
                         fishpos[i] - (fishvel[i] * 2))
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
    #sleep(0.01)
