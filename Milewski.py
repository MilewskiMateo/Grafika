from wall import wall
from line import line
import sys
import numpy
import math
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import Tuple
from PyQt5.QtWidgets import *


class Widget(QWidget):
    def __init__(self):
        self.lines = read_file("cube1.dat")
        self.lens = 300
        self.screen_size = (800, 800)
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        colors = [Qt.red, Qt.blue, Qt.green, Qt.yellow, Qt.magenta, Qt.gray]
        painter.setPen(QPen(colors[1], 2))
        # print(self.lines)

        allLines = []
        allWalls = []

        for b in self.lines:
            walls = []
            for x in range(6):
                walls.append(wall(colors[x]))
            counter = 0
            for l in b:
                viewedLine = []
                for p in l:
                    # tutaj sa rzutowane punkty
                    x = (self.lens / p[1]) * p[0] + self.screen_size[0] / 2
                    y = self.screen_size[1] / 2 - (self.lens / p[1]) * p[2]
                    viewedPoint = (x, y)
                    # if(p[1] > self.lens): // to jest usuwanie krawedzie po za ekranem
                    viewedLine.append(viewedPoint)

                # if(len(viewedLine) > 1):  to jest usuwanie krawedzie po za ekranem
                objL = line(viewedLine, l)
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
                painter.drawPolyline(QPolygon([QPoint(int(viewedLine[0][0]), int(
                    viewedLine[0][1])), QPoint(int(viewedLine[1][0]), int(viewedLine[1][1]))]))

                counter += 1

            for w in walls:
                w.createEquation()
                allWalls.append(w)

        print(allWalls)
        print(allLines)

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
        for b in range(len(self.lines)):
            for p in range(len(self.lines[b])):
                a = numpy.array(self.lines[b][p]).T
                m = numpy.array([
                    [1, 0, 0, x],
                    [0, 1, 0, y],
                    [0, 0, 1, z],
                    [0, 0, 0, 1]])
                self.lines[b][p] = numpy.matmul(m, a).T
        self.update()

    def rotateAllByY(self, kwant):
        for b in range(len(self.lines)):
            for p in range(len(self.lines[b])):
                a = numpy.array(self.lines[b][p]).T
                m = numpy.array([
                    [math.cos(kwant), 0, math.sin(kwant), 0],
                    [0, 1, 0, 0],
                    [-math.sin(kwant), 0, math.cos(kwant), 0],
                    [0, 0, 0, 1]])
                self.lines[b][p] = numpy.matmul(m, a).T
        self.update()

    def rotateAllByX(self, kwant):
        for b in range(len(self.lines)):
            for p in range(len(self.lines[b])):
                a = numpy.array(self.lines[b][p]).T
                m = numpy.array([
                    [1, 0, 0, 0],
                    [0, math.cos(kwant), -math.sin(kwant), 0],
                    [0, math.sin(kwant), math.cos(kwant), 0],
                    [0, 0, 0, 1]])
                self.lines[b][p] = numpy.matmul(m, a).T
        self.update()

    def rotateAllByZ(self, kwant):
        for b in range(len(self.lines)):
            for p in range(len(self.lines[b])):
                a = numpy.array(self.lines[b][p]).T
                m = numpy.array([
                    [math.cos(kwant), -math.sin(kwant), 0, 0],
                    [math.sin(kwant), math.cos(kwant), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
                self.lines[b][p] = numpy.matmul(m, a).T
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.resize(800, 800)
    ex.show()
    sys.exit(app.exec_())
