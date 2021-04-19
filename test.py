from wall import wall
from line import line
import sys
import numpy
import math
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import Tuple
from PyQt5.QtWidgets import *
SCREEN_SIZE = 800
colors = [Qt.black, Qt.red, Qt.blue, Qt.green, Qt.yellow, Qt.magenta, Qt.gray]
lines = []

l1 = line([(2,3),(2,1)])
l1.setCords3D([[0,1,2],[-1,4,5]])
l2 = line([(2,3),(2,1)])
l2.setCords3D([[-1,4,5],[2,-2,3]])

w1 = wall(colors[1])

w1.attachLine(l1)
w1.attachLine(l2)

w1.createEquation()

