from typing import Tuple
from line import *
import numpy as np


class wall:
    def __init__(self, color) -> None:
        self.color = color
        self.inOut = False
        self.lines = []

    def attachLine(self, line) -> None:
        self.lines.append(line)

    def createEquation(self):
        tmp = set()
        for l in self.lines:
            for p in l.cords3D:
                tmp.add(tuple(p[:3]))

        p1 = np.array(tmp.pop())
        p2 = np.array(tmp.pop())
        p3 = np.array(tmp.pop())

        v1 = p3 - p1
        v2 = p2 - p1
        cp = np.cross(v1, v2)
        a, b, c = cp
        d = np.dot(cp, p3)

        # print('{0}x + {1}y + {2}z = {3}'.format(a, b, c, d))

        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def getZ(self, x, y):
        return (self.d - self.a*x - self.b*y)/self.c
