import pygame
from pygame.locals import *
import numpy as np
from scipy.spatial import distance_matrix as spdistmat
from time import sleep

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))
keys = set()
textfont = pygame.font.Font(None, 15)

N = 100
pos = np.random.random_sample([N, 2]) * (w, h)
vel = np.zeros([N, 2], "float32")
points = np.zeros(N, "float32")
proportion = 0
temppos = np.float32([[((i // (N**0.5)) + 1) * np.min(screensize) / (N**0.5 + 1),
                       ((i % (N**0.5)) + 1) * np.min(screensize) / (2 * (N**0.5 + 1))]
                      for i in range(N)])

HAWK = 0
DOVE = 1

pointdisplays = [dict(), dict()]
cols = [(150, 0, 0), (0, 200, 255)]

victory = 1
wound = 1.5

oldcollisions = set()

cycles = 0

ACTION = 0
TRANSITION1 = 1
TRANSITION2 = 2
state = -1

proportion = min(max(proportion, 1/N), (N - 1)/N)
while True:
    screen.fill(0)
    if state == ACTION:
        pos += vel
        vel += (np.random.random_sample((N, 2)) - 0.5)
        vel = np.minimum(np.maximum(vel, -5), 5)
        vel[(pos < 0) | (pos > screensize)] *= -1
        pos = np.minimum(np.maximum(pos, 0), screensize)
        for i in range(N):
            strat = int(i >= int(N * proportion))
            try:
                pointdisplay = pointdisplays[strat][points[i]]
            except KeyError:
                pointdisplay = pointdisplays[strat][points[i]] = textfont.render(str(points[i]), False,
                                                                                 cols[(strat + 1) % 2])
            pygame.draw.circle(screen, cols[strat], np.int32(pos[i]), 10)
            screen.blit(pointdisplay, pos[i] - np.float32(pointdisplay.get_size()) / 2)
        collisions = np.argwhere((spdistmat(pos, pos) + np.tri(N, N) * 20) < 20)
        newcollisions = set()
        for collision in collisions:
            newcollisions.add(tuple(collision))
            if tuple(collision) not in oldcollisions:
                strats = np.int32(collision >= int(N * proportion))
                if HAWK in strats:
                    if DOVE in strats:
                        points[collision[strats == HAWK]] += victory
                        # print("{:04}: HAWK-DOVE: {:03} scares off {:03}".format(cycles, *collision))
                    else:
                        winner = collision[np.random.randint(2)]
                        loser = collision[(winner + 1) % 2]
                        points[winner] += victory
                        points[loser] -= wound
                        # print("{:04}: HAWK-HAWK: {:03} fights off {:03}".format(cycles, winner, loser))
                else:
                    points[collision] += victory / 2
                    # print("{:04}: DOVE-DOVE: {:03} works with {:03}".format(cycles, *collision))
                pygame.draw.circle(screen, (155, 255, 50), np.int32(np.mean(pos[collision], axis=0)), 20, 3)
        oldcollisions = newcollisions
        cycles += 1
        if cycles == 1000:
            state = TRANSITION1
            cycles = -50
            vel[:] = 0
            hawkpoints = np.unique(points[:int(N * proportion)], return_counts=True)
            dovepoints = np.unique(points[int(N * proportion):], return_counts=True)
            lopoints = min(min(points) - 1, 0)
            hipoints = max(points) + 1
            maxfreq = np.max(np.append(hawkpoints[1], dovepoints[1]))
            hawkx = (hawkpoints[0] - lopoints) * (w - 100) / (hipoints - lopoints)
            hawky = hawkpoints[1] * h * 0.2 / maxfreq
            dovex = (dovepoints[0] - lopoints) * (w - 100) / (hipoints - lopoints)
            dovey = dovepoints[1] * h * 0.2 / maxfreq
            try:
                avghawkpoints = np.average(hawkpoints[0], weights=hawkpoints[1])
            except ZeroDivisionError:
                avghawkpoints = 0
            try:
                avgdovepoints = np.average(dovepoints[0], weights=dovepoints[1])
            except ZeroDivisionError:
                avgdovepoints = 0
            shift = (avghawkpoints - avgdovepoints) / 100
            avghawkx = (avghawkpoints - lopoints) * (w - 100) / (hipoints - lopoints)
            avgdovex = (avgdovepoints - lopoints) * (w - 100) / (hipoints - lopoints)
            zerox = -lopoints * (w - 100) / (hipoints - lopoints)
    elif state in [TRANSITION1, TRANSITION2]:
        currpos = pos + (temppos - pos) * min(max(cycles, 0), 25) / 25
        for i in range(N):
            strat = int(i >= int(N * proportion))
            try:
                pointdisplay = pointdisplays[strat][points[i]]
            except KeyError:
                pointdisplay = pointdisplays[strat][points[i]] = textfont.render(str(points[i]), False,
                                                                                 cols[(strat + 1) % 2])
            pygame.draw.circle(screen, cols[strat], np.int32(currpos[i]), 10)
            screen.blit(pointdisplay, currpos[i] - np.float32(pointdisplay.get_size()) / 2)
        cycles += [1, -1][state - 1]
        if cycles >= 25:
            currval = lopoints + ((hipoints - lopoints) * (cycles - 25) / 25)
            currx = (w - 100) * (cycles - 25) / 25
            if currval >= 0:
                pygame.draw.line(screen, (255, 255, 255),
                                 (50 + zerox, (h * 0.75) - min(max(currx - zerox, 0), h * 0.2)),
                                 (50 + zerox, (h * 0.75) + min(max(currx - zerox, 0), h * 0.2)))
                pygame.draw.circle(screen, (255, 255, 255),
                                   np.int32([50 + zerox, (h * 0.75) - min(max(currx - zerox, 0), h * 0.2) - 5]),
                                   5, 1)
                pygame.draw.circle(screen, (255, 255, 255),
                                   np.int32([50 + zerox, (h * 0.75) + min(max(currx - zerox, 0), h * 0.2) + 5]),
                                   5, 1)
            if currval >= avghawkpoints:
                pygame.draw.line(screen, (100, 100, 100),
                                 (50 + avghawkx, h * 0.75),
                                 (50 + avghawkx, (h * 0.75) + min(max(currx - avghawkx, 0), h * 0.22)))
                pygame.draw.polygon(screen, cols[0],
                                    [(50 + avghawkx, (h * 0.75) + min(max(currx - avghawkx, 0), h * 0.22)),
                                     (45 + avghawkx, (h * 0.75) + min(max(currx - avghawkx, 0), h * 0.22) + 10),
                                     (55 + avghawkx, (h * 0.75) + min(max(currx - avghawkx, 0), h * 0.22) + 10)],
                                    1)
            if currval >= avgdovepoints:
                pygame.draw.line(screen, (100, 100, 100),
                                 (50 + avgdovex, h * 0.75),
                                 (50 + avgdovex, (h * 0.75) - min(max(currx - avgdovex, 0), h * 0.22)))
                pygame.draw.polygon(screen, cols[1],
                                    [(50 + avgdovex, (h * 0.75) - min(max(currx - avgdovex, 0), h * 0.22)),
                                     (45 + avgdovex, (h * 0.75) - min(max(currx - avgdovex, 0), h * 0.22) - 10),
                                     (55 + avgdovex, (h * 0.75) - min(max(currx - avgdovex, 0), h * 0.22) - 10)],
                                    1)
            for i in np.argwhere(hawkpoints[0] < currval):
                pygame.draw.line(screen, cols[0],
                                 (50 + hawkx[i], h * 0.75),
                                 (50 + hawkx[i], (h * 0.75) + min(max(currx - hawkx[i], 0), hawky[i])))
            for i in np.argwhere(dovepoints[0] < currval):
                pygame.draw.line(screen, cols[1],
                                 (50 + dovex[i], h * 0.75),
                                 (50 + dovex[i], (h * 0.75) - min(max(currx - dovex[i], 0), dovey[i])))
            pygame.draw.line(screen, (255, 255, 255), (50, h * 0.75), (50 + min(currx, w - 100), h * 0.75))
            pygame.draw.polygon(screen, (255, 255, 255),
                                ((50 + min(currx, w - 100), h * 0.75 - 5),
                                 (60 + min(currx, w - 100), h * 0.75),
                                 (50 + min(currx, w - 100), h * 0.75 + 5)),
                                1)
        if cycles == 150:
            state = TRANSITION2
            pos = np.random.random_sample([N, 2]) * (w, h)
        if state == TRANSITION2:
            if cycles > 100:
                proportion = min(max(proportion + shift / 50, 1/N), (N - 1)/N)
                points[:] = 0
        if cycles < -50:
            state = ACTION
            cycles = 0
    pygame.draw.rect(screen, cols[0], (0, 0, w * proportion, 10))
    pygame.draw.rect(screen, cols[1], (w, 0, w * (proportion - 1), 10))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            keys.add(e.key)
            if e.key == K_ESCAPE:
                quit()
            elif e.key == K_SPACE and state == -1:
                state = ACTION
        elif e.type == KEYUP:
            keys.discard(e.key)
    if state != ACTION:
        sleep(0.01)
