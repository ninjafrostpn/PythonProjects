import pygame
from pygame.locals import *
import numpy as np
from time import sleep

# pygame.init()

w, h = 500, 500
# screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

# keys = set()


class bifurc:
    def __init__(self, a, b):
        self.branches = [a, b]
        self.N = sum([p.N if isinstance(p, bifurc) else 1 for p in self.branches])
        self.branchcentres = [p.centre if isinstance(p, bifurc) else p for p in self.branches]
        self.centre = np.mean(self.branchcentres, axis=0)
        self.dist = np.linalg.norm(np.subtract(*self.branchcentres))

    def __str__(self):
        return "\n".join(self.textlines())

    def textlines(self, endspace=1):
        # Returns a text picture of the tree, separated into lines
        branchtext = [p.textlines(endspace) if isinstance(p, bifurc) else ["|"] for p in self.branches]
        branchN = [p.N if type(p) == bifurc else 1 for p in self.branches]
        return [
            "|",
            "-" * ((branchN[0] * (1 + endspace)) + 1),
            *[("{:%i}" % (branchN[0] * (1 + endspace))).format(branchtext[0][min(i, len(branchtext[0]) - 1)]) +
              branchtext[1][min(i, len(branchtext[1]) - 1)]
              for i in range(max(len(branchtext[0]), len(branchtext[1])))
              ]
        ]

    def __iter__(self):
        # Yields items sorted into the hierarchy from left to right
        for p in self.branches:
            if isinstance(p, bifurc):
                yield from p
            else:
                yield p


class tree:
    def __init__(self, points):
        self.points = np.float32(points)
        self.N = self.points.shape[0]
        self.centre = np.average(self.points, axis=0)
        if self.N < 2:
            self.hierarchy = None
        else:
            pointlist = [*self.points]
            for _ in range(self.N - 2):
                pairs = np.nonzero(np.tri(len(pointlist), k=-1, dtype="bool"))
                nppointlist = np.float32([p.centre if isinstance(p, bifurc) else p for p in pointlist])
                dist = np.linalg.norm(nppointlist[pairs[0]] - nppointlist[pairs[1]], axis=1)
                closest = np.argmin(dist)
                ilo, ihi = np.sort([pairs[0][closest], pairs[1][closest]])
                pointlist.insert(ilo, bifurc(pointlist.pop(ihi), pointlist.pop(ilo)))
            self.hierarchy = bifurc(*pointlist)
            self.points = np.float32([p for p in self.hierarchy])

    def __str__(self):
        numlength = len(str(self.N))
        hierarchytext = self.hierarchy.textlines(numlength + 3)
        return "\n".join([
            "Tree with {} elements (NOT TO SCALE):".format(self.N),
            *hierarchytext,
            "".join([("[{:%i}]  " % numlength).format(i) for i in range(self.N)]),
            "",
            *["{} = {}".format(i, p) for i, p in enumerate(self.points)]
        ])


data = np.random.random_sample((5000, 2)) * screensize
T = tree(data)
print(T)

# while True:
#     screen.fill(0)
#     pygame.display.flip()
#     for e in pygame.event.get():
#         if e.type == QUIT:
#             quit()
#         elif e.type == KEYDOWN:
#             keys.add(e.key)
#             if e.key == K_ESCAPE:
#                 quit()
#         elif e.type == KEYUP:
#             keys.discard(e.key)
#     sleep(0.001)
