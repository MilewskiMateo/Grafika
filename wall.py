from typing import Tuple
from line import *
import numpy as np


class wall:
    def __init__(self, color, colorSTR) -> None:
        self.color = color
        self.colorSTR = colorSTR
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

        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def getY(self, x, z, focal):
        x = x - 400
        z = (z * -1) + 400
        return (-self.d)/((self.a * x/focal) + (self.c*z/focal) + self.b)

    def changeInOut(self):
        if self.inOut == True:
            self.inOut = False
        else:
            self.inOut = True
