import pygame
from pygame.locals import *
import numpy as np

pygame.init()

w, h = 500, 500
screen = pygame.display.set_mode((w, h))
screensize = np.int32((w, h))

keys = set()

polygon = np.zeros([0, 2], "float64")

while True:
    screen.fill(0)
    if len(polygon) > 2:
        # Returns all left-turning vertices in an otherwise right-turning clockwise-defined polygon
        lefts = np.roll(np.cross(np.roll(polygon, -1, axis=0) - polygon,
                                 np.roll(polygon, -2, axis=0) - polygon) < 0, 1)
    else:
        lefts = np.zeros(len(polygon), "bool")
    if len(polygon) > 1:
        pygame.draw.lines(screen, 255, True, polygon)
    # The endpoints of additional lines generated from bisecting the concave vertices
    alsoptsa = np.zeros((0, 2), "float64")
    alsoptsb = np.zeros((0, 2), "float64")
    for i in np.nonzero(lefts)[0]:
        # https://stackoverflow.com/a/3252222
        # The vertices anticlockwise and clockwise of the concave one
        prevvec = polygon[i - 1] - polygon[i]
        nextvec = polygon[i - (len(polygon) - 1)] - polygon[i]
        # A vector representing a ray bisecting the interior angle of the concave vertex
        da = -((np.linalg.norm(prevvec) * nextvec) + (np.linalg.norm(nextvec) * prevvec))
        pygame.draw.line(screen, 255 << 16, polygon[i], polygon[i] + (da * 100))
        # An array including the vertices of the polygon as well as the first points of each new cut
        polyandalso = np.append(polygon, alsoptsa, axis=0)
        # Array of vectors pointing along each side or new cut
        db = np.append(np.roll(polygon, -1, axis=0), alsoptsb, axis=0) - polyandalso
        # Array of vectors pointing from each vertex of the polygon or end of a new cut to the concave vertex
        dp = polygon[i] - polyandalso
        # Vector perpendicular to da
        dap = (da * [1, -1])[::-1]
        # Numerator and denominator of the fraction representing distance of bisector's intersection along the side/cut
        num = np.sum(dap * dp, axis=1)
        denom = np.sum(dap * db, axis=1)
        # The fraction is 0 at one bounding vertex, 1 at the other (therefore true intersection where 0 <= frac <= 1)
        frac = num / denom
        # Points of intersection between concave angle bisector and the sides/cuts
        pts = (frac * db.T).T + polyandalso
        # Distance of these points from the concave angle
        r = np.sum(da * (pts - polygon[i]), axis=1)
        # Intersections which are between their two bounding points and directed from the concave angle into the shape
        goodptmask = (r > 0) & (frac <= 1) & (frac >= 0)
        if np.any(goodptmask):
            # Index of the intersection closest to the concave vertex
            closest = np.argmin(r[goodptmask])
            # Adds vertex and intersection as bounding points of this new cut
            alsoptsa = np.append(alsoptsa, [polygon[i]], axis=0)
            alsoptsb = np.append(alsoptsb, [pts[goodptmask][closest]], axis=0)
            pygame.draw.circle(screen, 255 << 16, np.int32(pts[goodptmask][closest]), 10, 1)
    for pt, left in zip(np.int32(polygon), lefts):
        pygame.draw.circle(screen, 255 << (16 if left else 8), pt, 5)
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
            if e.key == K_SPACE:
                polygon = np.zeros([0, 2], "int32")
        elif e.type == MOUSEBUTTONDOWN:
            polygon = np.append(polygon, [pygame.mouse.get_pos()], axis=0)
