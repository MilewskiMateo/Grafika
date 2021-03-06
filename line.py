from typing import Tuple
from line import *


class line:
    def __init__(self, cords2D, cords3D) -> None:
        self.cords2D = cords2D
        self.cords3D = cords3D

    def attachWall(self, wall) -> None:
        self.wall = wall

    def intersects(self, s0) -> bool:
        s1 = self.cords2D
        dx0 = s0[1][0]-s0[0][0]
        dx1 = s1[1][0]-s1[0][0]
        dy0 = s0[1][1]-s0[0][1]
        dy1 = s1[1][1]-s1[0][1]
        p0 = dy1*(s1[1][0]-s0[0][0]) - dx1*(s1[1][1]-s0[0][1])
        p1 = dy1*(s1[1][0]-s0[1][0]) - dx1*(s1[1][1]-s0[1][1])
        p2 = dy0*(s0[1][0]-s1[0][0]) - dx0*(s0[1][1]-s1[0][1])
        p3 = dy0*(s0[1][0]-s1[1][0]) - dx0*(s0[1][1]-s1[1][1])
        return (p0*p1 <= 0) & (p2*p3 <= 0)

    def line_intersection(self, line1) -> Tuple:
        line2 = self.cords2D
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('Równoległe bądź współliniowe')
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        return x, y
