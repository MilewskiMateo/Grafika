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
colorsSTR = ["black", "red", "blue", "green", "yellow", "magenta", "gray"]


class Widget(QWidget):
    def __init__(self):
        self.blocks = read_file("cube1.dat")
        self.lens = 300
        self.screen_size = (SCREEN_SIZE, SCREEN_SIZE)
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)

        # painter.setPen(QPen(colors[1], 2))
        # print(self.blocks)

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
                    # tutaj sa rzutowane punkty
                    # x = (self.lens / p[1]) * p[0] + self.screen_size[0] / 2
                    # y = self.screen_size[1] / 2 - (self.lens / p[1]) * p[2]
                    x = (self.lens / p[1]) * p[0]
                    y = (self.lens / p[1]) * p[2]
                    viewedPoint = (x, y)
                    # if(p[1] > self.lens): // to jest usuwanie krawedzie po za ekranem
                    viewedLine.append(viewedPoint)

                # if(len(viewedLine) > 1):  to jest usuwanie krawedzie po za ekranem
                objL = line(viewedLine)
                # print(viewedLine)
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

                # stare rysowanie
                # painter.drawPolyline(QPolygon([QPoint(int(viewedLine[0][0]), int(viewedLine[0][1])), QPoint(int(viewedLine[1][0]), int(viewedLine[1][1]))]))

                counter += 1

            for w in walls:
                w.createEquation()
                allWalls.append(w)

            for i in range(SCREEN_SIZE):
<<<<<<< HEAD
                intersectionOrder = []

                scanLine = line(((0, i), (SCREEN_SIZE, i)))
                for edge in allLines:
                    if scanLine.intersects(edge):
                        try:
                            intersectionOrder.append(
                                scanLine.line_intersection(edge))
                        except:
                            continue
                sections = []
                intersectionOrder.sort()

                if(i == 70):
                    painter.setPen(QPen(colors[1], 1))
                    painter.drawPolyline(QPolygon([0, i, SCREEN_SIZE, i]))
                    for e in intersectionOrder:
                        print(e)
                        print(e[3])

                lastX = 0
                sectionCenterX = 0
                for point in intersectionOrder:
                    point[3].walls[0].changeInOut()
                    point[3].walls[1].changeInOut()
                    if lastX != 0:
                        sectionCenterX = lastX + \
                            math.fabs(math.fabs(point[0]) - math.fabs(lastX))/2
                        closestPlane = background
                        closestZ = 9999999.0
                        for plane in allWalls:
                            if plane.inOut:
                                planeZ = plane.getZ(sectionCenterX, i)
                                # print(planeZ)
                                if planeZ < closestZ:
                                    if planeZ > -999999.0:
                                        closestPlane = plane
                        sections.append(closestPlane.color)
                    else:
                        sections.append(colors[0])
                    lastX = point[0]
                lastX = 0

                if len(sections) != 0:
                    for section in range(len(sections)):
                        # if(lastX < 0 and intersectionOrder[section][0] > 0):
                        #     lastX = 0
                        # if(lastX < SCREEN_SIZE and )
                        painter.setPen(QPen(sections[section], 1))
                        painter.drawPolyline(
                            QPolygon([lastX, i, intersectionOrder[section][0], i]))
                        lastX = intersectionOrder[section][0]
                    if lastX < SCREEN_SIZE:
=======

                if not (i == 50):

                    intersectionOrder = []
                    scanLine = line(((0, i), (SCREEN_SIZE, i)))
                    for edge in allLines:
                        if scanLine.intersects(edge):
                            try:
                                intersectionOrder.append(
                                    scanLine.line_intersection(edge))
                            except:
                                continue
                    sections = []
                    intersectionOrder.sort()

                    if(i == 70):
                        painter.setPen(QPen(colors[1], 1))
                        painter.drawPolyline(QPolygon([0, i, SCREEN_SIZE, i]))
                        for e in intersectionOrder:
                            print(e)
                            print(e[3])

                    lastX = 0
                    sectionCenterX = 0
                    for point in intersectionOrder:

                        if lastX != 0:
                            sectionCenterX = lastX + \
                                math.fabs(
                                    math.fabs(point[0]) - math.fabs(lastX))/2
                            closestPlane = background
                            closestZ = 9999999.0
                            for plane in allWalls:
                                if plane.inOut:
                                    planeZ = plane.getZ(sectionCenterX, i)
                                    # print(planeZ)
                                    if planeZ < closestZ:
                                        closestPlane = plane
                            sections.append(closestPlane.color)
                        else:
                            sections.append(colors[0])
                        point[3].walls[0].changeInOut()
                        point[3].walls[1].changeInOut()
                        lastX = point[0]
                    lastX = 0

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
>>>>>>> mateo
                        painter.setPen(QPen(background.color, 1))
                        painter.drawPolyline(QPolygon([0, i, SCREEN_SIZE, i]))

            for w in allWalls:
                w.inOut = False

            # painter.drawPolyline(QPolygon([QPoint(int(scanLine.cords2D[0][0]),int(scanLine.cords2D[0][1])),
            # QPoint(int(scanLine.cords2D[1][0]),int(scanLine.cords2D[1][1]))]))

        # painter.setPen(QPen(colors[1], 2))
        # painter.drawPolyline(QPolygon([200, 599, 800, 599]))

        # Tutaj powinien być kontynulowany alogrytm
        # Powinny byc wszystkie linie wypelnione danymi
        # i wszystkie sciany tez

        # w przypadku obiektu ściany jest metoda która zwraca Z z wartosci X,Y

        # Natomiast w przypadku obiektu lini tam jest troche specyficznie bo sa dwie metody
        # jedna mowi czy dwa odcinki w ogole sie przecinaja
        # druga zwraca kordynaty miejsca przeciecia PROSTYCH stowrzynych na podstawie odcinkow
        # lepiej to by było jakos połaczyć w jedną metodę ale tam jest niezła kaszana jeżeli
        # chodzi o sytuacje współliniowości i równoległóści mozesz sobie
        # potestowac na jakims osobnym pliku by ogarnac

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
        ROTATION_STEP = numpy.radians(0.8)
        if event.key() == Qt.Key_PageUp:
            self.transformAllBy(0, -12, 0)
        if event.key() == Qt.Key_PageDown:
            self.transformAllBy(0, 12, 0)
        if event.key() == Qt.Key_Left:
            self.transformAllBy(12, 0, 0)
        if event.key() == Qt.Key_Right:
            self.transformAllBy(-12, 0, 0)
        if event.key() == Qt.Key_Up:
            self.transformAllBy(0, 0, -12)
        if event.key() == Qt.Key_Down:
            self.transformAllBy(0, 0, 12)

        if event.key() == Qt.Key_A:
            self.rotateAllByX(ROTATION_STEP)
        if event.key() == Qt.Key_D:
            self.rotateAllByX(-ROTATION_STEP)

        if event.key() == Qt.Key_W:
            self.rotateAllByY(ROTATION_STEP)
        if event.key() == Qt.Key_S:
            self.rotateAllByY(-ROTATION_STEP)

        if event.key() == Qt.Key_Q:
            self.rotateAllByZ(ROTATION_STEP)
        if event.key() == Qt.Key_E:
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

<<<<<<< HEAD
=======

def createWalls():
    for x in range(1, 7):
        walls.append(wall(colors[x]))
        # walls.append(wall(colors[random.randint(1,len(colors) - 1)]))
    # for b in blocks:
    #     counter = 0
    #     for edge in b:
    #         if counter in [0, 1, 2, 3]:
    #             wall[0].
    #         print(edge)
>>>>>>> mateo


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.resize(800, 800)
    ex.show()
    sys.exit(app.exec_())
