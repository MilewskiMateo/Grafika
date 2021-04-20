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
colors = [Qt.black, Qt.red, Qt.blue,  Qt.yellow, Qt.gray, Qt.magenta, Qt.green]
colorsSTR = ["black", "red", "blue",  "yellow", "gray", "magenta", "green", ]


class Widget(QWidget):
    def __init__(self):
        self.blocks = read_file("cube4.dat")
        self.lens = 300
        self.screen_size = (SCREEN_SIZE, SCREEN_SIZE)
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)

        allLines = []
        allWalls = []
        background = wall(colors[0], colorsSTR[0])

        for b in self.blocks:
            walls = []
            for x in range(1, 7):
                walls.append(wall(colors[x], colorsSTR[x]))
            counter = 0

            for l in b:
                viewedLine = []
                for p in l:
                    x = (self.lens / p[1]) * p[0] + self.screen_size[0] / 2
                    y = self.screen_size[1] / 2 - (self.lens / p[1]) * p[2]
                    viewedPoint = (x, y)
                    # if(p[1] > self.lens): // to jest usuwanie krawedzie po za ekranem
                    viewedLine.append(viewedPoint)

                # if(len(viewedLine) > 1):  to jest usuwanie krawedzie po za ekranem
                objL = line(viewedLine)
                objL.setCords3D(l)
                if counter in [0, 1, 2, 3]:
                    objL.attachWall(walls[0])
                    walls[0].attachLine(objL)
                if counter in [1, 4, 9, 6]:
                    objL.attachWall(walls[1])
                    walls[1].attachLine(objL)
                if counter in [9, 8, 11, 10]:
                    objL.attachWall(walls[2])
                    walls[2].attachLine(objL)
                if counter in [3, 7, 11, 5]:
                    objL.attachWall(walls[3])
                    walls[3].attachLine(objL)
                if counter in [6, 2, 10, 7]:
                    objL.attachWall(walls[4])
                    walls[4].attachLine(objL)
                if counter in [0, 4, 8, 5]:
                    objL.attachWall(walls[5])
                    walls[5].attachLine(objL)

                allLines.append(objL)

                counter += 1

            for w in walls:
                w.createEquation()
                allWalls.append(w)

            for i in range(SCREEN_SIZE):

                intersectionOrder = []
                scanLine = line(((-SCREEN_SIZE, i), (SCREEN_SIZE*2, i)))
                for edge in allLines:
                    if scanLine.intersects(edge):
                        try:
                            intersectionOrder.append(
                                scanLine.line_intersection(edge))
                        except:
                            continue
                sections = []
                intersectionOrder.sort()

                lastX = -SCREEN_SIZE
                sectionCenterX = -SCREEN_SIZE

                for point in intersectionOrder:

                    if lastX != -SCREEN_SIZE:
                        sectionCenterX = lastX + \
                            math.fabs(
                                math.fabs(point[0]) - math.fabs(lastX))/2
                        closestPlane = background
                        closestZ = -999999.0
                        for plane in allWalls:
                            if plane.inOut:
                                planeZ = plane.getY(
                                    sectionCenterX, i, self.lens)
                                if planeZ > closestZ:
                                    closestPlane = plane
                                    closestZ = planeZ
                        sections.append(closestPlane.color)
                    else:
                        sections.append(colors[0])
                    point[3].walls[0].changeInOut()
                    point[3].walls[1].changeInOut()
                    lastX = point[0]
                lastX = -SCREEN_SIZE

                if len(sections) != 0:
                    for section in range(len(sections)):
                        painter.setPen(QPen(sections[section], 1))
                        painter.drawPolyline(
                            QPolygon([lastX, i, intersectionOrder[section][0], i]))
                        lastX = intersectionOrder[section][0]
                    if lastX < SCREEN_SIZE:
                        painter.setPen(QPen(background.color, 1))
                        painter.drawPolyline(
                            QPolygon([lastX, i, SCREEN_SIZE, i]))
                else:
                    painter.setPen(QPen(background.color, 1))
                    painter.drawPolyline(QPolygon([0, i, SCREEN_SIZE, i]))

            for w in allWalls:
                w.inOut = False

    def transformAllBy(self, x, y, z):
        for b in range(len(self.blocks)):
            for p in range(len(self.blocks[b])):
                a = numpy.array(self.blocks[b][p]).T
                m = numpy.array([
                    [1, 0, 0, x],
                    [0, 1, 0, y],
                    [0, 0, 1, z],
                    [0, 0, 0, 1]])
                self.blocks[b][p] = numpy.matmul(m, a).T
        self.update()

    def rotateAllByY(self, kwant):
        for b in range(len(self.blocks)):
            for p in range(len(self.blocks[b])):
                a = numpy.array(self.blocks[b][p]).T
                m = numpy.array([
                    [math.cos(kwant), 0, math.sin(kwant), 0],
                    [0, 1, 0, 0],
                    [-math.sin(kwant), 0, math.cos(kwant), 0],
                    [0, 0, 0, 1]])
                self.blocks[b][p] = numpy.matmul(m, a).T
        self.update()

    def rotateAllByX(self, kwant):
        for b in range(len(self.blocks)):
            for p in range(len(self.blocks[b])):
                a = numpy.array(self.blocks[b][p]).T
                m = numpy.array([
                    [1, 0, 0, 0],
                    [0, math.cos(kwant), -math.sin(kwant), 0],
                    [0, math.sin(kwant), math.cos(kwant), 0],
                    [0, 0, 0, 1]])
                self.blocks[b][p] = numpy.matmul(m, a).T
        self.update()

    def rotateAllByZ(self, kwant):
        for b in range(len(self.blocks)):
            for p in range(len(self.blocks[b])):
                a = numpy.array(self.blocks[b][p]).T
                m = numpy.array([
                    [math.cos(kwant), -math.sin(kwant), 0, 0],
                    [math.sin(kwant), math.cos(kwant), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
                self.blocks[b][p] = numpy.matmul(m, a).T
        self.update()

    def keyPressEvent(self, event):
        ROTATION_STEP = numpy.radians(3.8)
        if event.key() == Qt.Key_Up:
            self.transformAllBy(0, -42, 0)
        if event.key() == Qt.Key_Down:
            self.transformAllBy(0, 42, 0)
        if event.key() == Qt.Key_Left:
            self.transformAllBy(42, 0, 0)
        if event.key() == Qt.Key_Right:
            self.transformAllBy(-42, 0, 0)
        if event.key() == Qt.Key_PageUp:
            self.transformAllBy(0, 0, -42)
        if event.key() == Qt.Key_PageDown:
            self.transformAllBy(0, 0, 42)

        if event.key() == Qt.Key_S:
            self.rotateAllByX(ROTATION_STEP)
        if event.key() == Qt.Key_W:
            self.rotateAllByX(-ROTATION_STEP)

        if event.key() == Qt.Key_Q:
            self.rotateAllByY(ROTATION_STEP)
        if event.key() == Qt.Key_E:
            self.rotateAllByY(-ROTATION_STEP)

        if event.key() == Qt.Key_D:
            self.rotateAllByZ(ROTATION_STEP)
        if event.key() == Qt.Key_A:
            self.rotateAllByZ(-ROTATION_STEP)

        if event.key() == Qt.Key_Z:
            self.lens -= 4
            self.update()
        if event.key() == Qt.Key_X:
            self.lens += 4
            self.update()


def read_file(file_name: str):
    blocks = []
    with open(file_name, 'r') as file:
        for block in file.read().split('/'):
            loaded_edges = []
            for line in block.split('\n'):
                points = [float(p) for p in line.split(', ')]
                beginPoint = points[:3]
                endPoint = points[3:]
                beginPoint.append(1)
                endPoint.append(1)
                loaded_edges.append([beginPoint, endPoint])
            blocks.append(loaded_edges)
        return blocks


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.resize(800, 800)
    ex.show()
    sys.exit(app.exec_())
