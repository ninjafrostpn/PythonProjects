# Based on Couzin et al. (2002), but as a 2D simulation
import pygame
from pygame.locals import *
import numpy as np
from time import sleep

debug = False  # If True, shows zones of detection and allows their alteration with mouse position

# Interface initialisation
pygame.init()
w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))
keys = set()  # For keypress detection

# Set simulation parameters
N = 200      # Number of fish
s = 1        # Speed of fish (px per time unit)
T = 0.1      # Timestep (time units per cycle)
alpha = 270  # Visual range of fish (degrees, centred on front of fish)
theta = 40   # Turning speed of fish (degrees per time unit)
r_r = 10     # Outer radius of Zone of Repulsion
r_o = 12     # Outer radius of Zone of Orientation
r_a = 27     # Outer radius of Zone of Attraction

# The position vectors, c, and unit direction vectors, v, of the fish
c = np.random.random_sample((N, 2)) * screensize
v = np.float32([np.sin([ang + np.pi/2, ang]) for ang in (np.random.random_sample(N) * (np.pi * 2))])
v = (v.T / np.linalg.norm(v, axis=1)).T  # Normalisation. There's a lot of this in this program.

# A pair of arrays, covering every possible non-self interaction combination
# - pairs[0] are used as the fish doing the detecting, generally called fish i
# - pairs[1] are used as the fish being detected, generally called fish j
pairs = np.nonzero(np.tri(N, dtype="bool") ^ ~np.tri(N, k=-1, dtype="bool"))

while True:
    if debug:
        # The widths of the Zones of Orientation and Attraction are set by mouse x and y
        mpos = np.int32(pygame.mouse.get_pos())
        r_o = r_r + (mpos[0] / 10)
        r_a = r_o + (mpos[1] / 10)

    # The vector pointing from each fish i to each fish j
    r_ij = c[pairs[1]] - c[pairs[0]]         # Full vector
    r_ij_abs = np.linalg.norm(r_ij, axis=1)  # Distance
    r_ij_norm = (r_ij.T / r_ij_abs).T        # Normalised vector

    # The angle between the direction of travel for fish i and the line of sight from i to j
    ang_vis = np.arctan2(np.linalg.norm(np.cross(r_ij_norm, v[pairs[0]]).reshape(r_ij.shape[0], -1), axis=1),
                         np.einsum('ij, ij->i', r_ij_norm, v[pairs[0]]))
    # Mask (for the pair arrays) that singles out the pairings where fish i can see fish j
    # (einsum here takes the dot product of each pair of corresponding vectors very quickly)
    mask_visible = alpha / 2 > np.abs(ang_vis * (180 / np.pi))

    # Mask (for the pair arrays) that singles out the pairings where fish j is in fish i's zone of repulsion
    mask_zor = mask_visible & (r_ij_abs < r_r)

    # Generating the mask (for the pair arrays) that singles out fish i which have either:
    # - a tank wall in their repulsion zone (this is not in the model as per the paper)
    # - any fish in their repulsion zone
    mask_mode_r = np.zeros(r_ij_abs.shape, dtype="bool")
    # Masks (for the list of all fish i) that single out:
    mask_toplft = np.any(c < r_r, axis=1)               # those close to the top or left walls
    mask_btmrgt = np.any(c > screensize - r_r, axis=1)  # those close to the bottom or right walls
    # Fills in mask_mode_r with all the fish satisfying any of these conditions
    for i in set(pairs[0][mask_zor]):
        mask_mode_r |= (pairs[0] == i) | mask_toplft[pairs[0]] | mask_btmrgt[pairs[0]]

    # Masks (for the pair arrays) that single out pairings where fish j is in fish i's
    mask_zoo = mask_visible & ~mask_mode_r & (r_ij_abs < r_o)              # Zone of Orientation
    mask_zoa = mask_visible & ~mask_mode_r & ~mask_zoo & (r_ij_abs < r_a)  # Zone of Attraction

    # Generating the unit direction vectors representing the direction fish i would like to go
    d_i = np.zeros((N, 2))
    # Generating unit direction vectors for repulsion
    d_r = np.zeros((N, 2))
    d_r[pairs[0][mask_zor]] -= r_ij_norm[mask_zor]
    # (These must be redone separately to mask_topleft etc, else the fish move on a certain diagonal away from walls)
    d_r[c < r_r] += 1
    d_r[c > w - r_r] -= 1
    d_r[pairs[0][mask_zor]] = (d_r[pairs[0][mask_zor]].T / np.linalg.norm(d_r[pairs[0][mask_zor]], axis=1)).T
    d_i += d_r
    # Generating unit direction vectors for orientation
    d_o = np.zeros((N, 2))
    d_o[pairs[0][mask_zoo]] += v[pairs[1][mask_zoo]]
    d_o[pairs[0][mask_zoo]] = (d_o[pairs[0][mask_zoo]].T / np.linalg.norm(d_o[pairs[0][mask_zoo]], axis=1)).T
    d_i += d_o
    # Generating unit direction vectors for orientation
    d_a = np.zeros((N, 2))
    d_a[pairs[0][mask_zoa]] += r_ij_norm[mask_zoa]
    d_a[pairs[0][mask_zoa]] = (d_a[pairs[0][mask_zoa]].T / np.linalg.norm(d_a[pairs[0][mask_zoa]], axis=1)).T
    d_i += d_a
    # Mask (for the list of all fish i) that singles out all the fish i with zero vectors as their intended direction
    mask_zeroes = np.all(d_i == 0, axis=1)
    # Setting zero vectors to be the same direction the fish is currently going
    d_i[mask_zeroes] = v[mask_zeroes]
    # Ensure normalisation of all of the intended direction vectors
    # (Takes care of fish i with fish in both their Zones of Orientation and Attraction)
    d_i = (d_i.T / np.linalg.norm(d_i, axis=1)).T

    # The angle between each fish i's current and intended directions
    ang_turn = np.arctan2(np.cross(d_i, v), np.einsum('ij, ij->i', d_i, v))
    # Mask (for the list of all fish i) that singles out fish i who can cover their intended turn in one timestep
    mask_close = np.abs(ang_turn * (180/np.pi)) < theta * T
    # Turns said fish (but doesn't bother with fish who aren't turning at all)
    v[mask_close & ~mask_zeroes] = d_i[mask_close & ~mask_zeroes]
    # Current and new cardinal direction angle for fish i which can't cover their intended turn in one timestep
    ang_cur = np.arctan2(*(v[~mask_close & ~mask_zeroes].T[::-1]))
    ang_new = ang_cur - (np.sign(ang_turn[~mask_close & ~mask_zeroes]) * theta * (np.pi/180) * T)
    # Turns these fish
    v[~mask_close & ~mask_zeroes] = np.sin([ang_new + (np.pi/2), ang_new]).T

    c += v * s * T  # Movement of all fish i in the direction of v at speed s over one timestep, T
    c = np.minimum(np.maximum(c, 0), screensize)  # But stop them at the screen edge

    # Drawing things
    screen.fill(0)
    if debug:
        # Draw the outer limits of the zones for each fish
        for i in range(N):
            pygame.draw.circle(screen, (255, 0, 0), np.int32(c[i]), int(r_r), 1)
            pygame.draw.circle(screen, (255, 255, 0), np.int32(c[i]), int(r_o), 1)
            pygame.draw.circle(screen, (0, 255, 0), np.int32(c[i]), int(r_a), 1)
    for i in range(N):
        # Draw the fish, approximated as pink circles
        pygame.draw.circle(screen, (255, 0, 255), np.int32(c[i]), 2)
        # Draw the direction the fish is going (white) and wants to go (turquoise)
        pygame.draw.line(screen, (255, 255, 255), c[i], c[i] + (v[i] * 10))
        pygame.draw.line(screen, (0, 255, 255), c[i], c[i] + (d_i[i] * 10))
    pygame.display.flip()

    # Event handling
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
        elif e.type == KEYUP:
            keys.discard(e.key)
