from typing import Tuple
from line import *
import numpy as np


class wall:
    def __init__(self, color) -> None:
        self.color = color
        self.inOut = False

    def attachLine(self, line) -> None:
        tmp = self.lines.append(line)
        self.lines = tmp

    def attachPoints(self, points3):
        self.points = points3

    def giveZ(self, x, y):
        p1 = np.array(self.points[0])
        p2 = np.array(self.points[1])
        p3 = np.array(self.points[2])

        # These two vectors are in the plane
        v1 = p3 - p1
        v2 = p2 - p1

        # the cross product is a vector normal to the plane
        cp = np.cross(v1, v2)
        a, b, c = cp

        # This evaluates a * x3 + b * y3 + c * z3 which equals d
        d = np.dot(cp, p3)

        print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))

        def getZ(x, y):
            return (d - a*x - b*y)/c
