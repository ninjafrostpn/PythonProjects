# Based on Couzin et al. (2002)
import pygame
from pygame.locals import *
import numpy as np
from time import sleep

pygame.init()
debug = False

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()

N = 100
c = np.random.random_sample((N, 2)) * screensize
v = np.float32([np.sin([ang + np.pi/2, ang]) for ang in (np.random.random_sample(N) * (np.pi * 2))])
v = (v.T / np.linalg.norm(v, axis=1)).T

s = 1
alpha = 270
theta = 40
T = 0.1

r_r = 10
r_o = 12
r_a = 27

pairs = np.nonzero(np.tri(N, dtype="bool") ^ ~np.tri(N, k=-1, dtype="bool"))

while True:
    if debug:
        mpos = np.int32(pygame.mouse.get_pos())
        r_o = r_r + (mpos[0] / 10)
        r_a = r_o + (mpos[1] / 10)

    screen.fill(0)
    r_ij = c[pairs[1]] - c[pairs[0]]
    r_ij_abs = np.linalg.norm(r_ij, axis=1)
    r_ij_norm = (r_ij.T / r_ij_abs).T  # Issue with nans when r_ij is (0, 0)

    # mask for the pair arrangement that excludes all pairings where fish i can't see fish j
    # (einsum here takes the dot product of each pair of corresponding vectors very quickly)
    ang_vis = np.arctan2(np.linalg.norm(np.cross(r_ij_norm, v[pairs[0]]).reshape(r_ij.shape[0], -1), axis=1),
                         np.einsum('ij, ij->i', r_ij_norm, v[pairs[0]]))
    mask_visible = alpha / 2 > np.abs(ang_vis * (180 / np.pi))

    # masks for the pair arrangement that single out i-j pairings where i and j are in each other's zone of repulsion
    mask_zor = mask_visible & (r_ij_abs < r_r)

    # mask for the pair arrangement that singles out individuals in repulsion mode
    mask_mode_r = np.zeros(r_ij_abs.shape, dtype="bool")
    mask_toplft = np.any(c < r_r, axis=1)
    mask_btmrgt = np.any(c > screensize - r_r, axis=1)
    for i in set(pairs[0][mask_zor]):
        mask_mode_r |= (pairs[0] == i) | mask_toplft[pairs[0]] | mask_btmrgt[pairs[0]]

    # masks for the pair arrangement that single out i-j pairings where i and j are in each other's...
    mask_zoo = mask_visible & ~mask_mode_r & (r_ij_abs < r_o)              # ... zone of orientation...
    mask_zoa = mask_visible & ~mask_mode_r & ~mask_zoo & (r_ij_abs < r_a)  # ... or zone of attraction

    # The intended-direction calculation for each fish i
    d_i = np.zeros((N, 2))

    d_r = np.zeros((N, 2))
    d_r[pairs[0][mask_zor]] -= r_ij_norm[mask_zor]
    d_r[mask_toplft] += 1
    d_r[mask_btmrgt] -= 1
    d_r[pairs[0][mask_zor]] = (d_r[pairs[0][mask_zor]].T / np.linalg.norm(d_r[pairs[0][mask_zor]], axis=1)).T
    d_i += d_r

    d_o = np.zeros((N, 2))
    d_o[pairs[0][mask_zoo]] += v[pairs[1][mask_zoo]]
    d_o[pairs[0][mask_zoo]] = (d_o[pairs[0][mask_zoo]].T / np.linalg.norm(d_o[pairs[0][mask_zoo]], axis=1)).T
    d_i += d_o

    d_a = np.zeros((N, 2))
    d_a[pairs[0][mask_zoa]] += r_ij_norm[mask_zoa]
    d_a[pairs[0][mask_zoa]] = (d_a[pairs[0][mask_zoa]].T / np.linalg.norm(d_a[pairs[0][mask_zoa]], axis=1)).T
    d_i += d_a

    mask_zeroes = np.all(d_i == 0, axis=1)
    d_i[mask_zeroes] = v[mask_zeroes]

    d_i = (d_i.T / np.linalg.norm(d_i, axis=1)).T

    ang_turn = np.arctan2(np.cross(d_i, v), np.einsum('ij, ij->i', d_i, v))
    mask_close = np.abs(ang_turn * (180/np.pi)) < theta * T
    v[mask_close & ~mask_zeroes] = d_i[mask_close & ~mask_zeroes]
    angs = np.arctan2(*(v[~mask_close & ~mask_zeroes].T[::-1]))
    newangs = angs - (np.sign(ang_turn[~mask_close & ~mask_zeroes]) * theta * (np.pi/180) * T)
    v[~mask_close & ~mask_zeroes] = np.sin([newangs + (np.pi/2), newangs]).T

    c += v * s * T
    c = np.minimum(np.maximum(c, 0), screensize)
    if debug:
        for i in range(N):
            pygame.draw.circle(screen, (255, 0, 0), np.int32(c[i]), int(r_r), 1)
            pygame.draw.circle(screen, (255, 255, 0), np.int32(c[i]), int(r_o), 1)
            pygame.draw.circle(screen, (0, 255, 0), np.int32(c[i]), int(r_a), 1)
    for i in range(N):
        pygame.draw.circle(screen, (255, 0, 255), np.int32(c[i]), 2)
        pygame.draw.line(screen, (255, 255, 255), c[i], c[i] + (v[i] * 10))
        pygame.draw.line(screen, (0, 255, 255), c[i], c[i] + (d_i[i] * 10))
    pygame.display.flip()

    # print(np.arctan2(np.cross(screensize, mpos - (screensize/2)),
    #                  np.dot(screensize, mpos - (screensize/2))) * (180/np.pi))

    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type == KEYUP:
            keys.discard(e.key)
    # sleep(T)
