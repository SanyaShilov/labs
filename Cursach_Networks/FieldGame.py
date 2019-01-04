import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow)

from PyQt5.QtGui import (QPainter)

from PyQt5.QtCore import Qt

import Field


N = 3 # number of loaded field


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.visualField = VisualField()
        self.setCentralWidget(self.visualField)
        self.setFixedSize(self.visualField.width()+200,
                          self.visualField.height())
        desktop = QApplication.desktop()
        self.move((desktop.width()-self.width())//2-8,
                  (desktop.height()-self.height())//2-30)
        

class VisualField(QWidget):
    def __init__(self):
        super().__init__()
        self.field = Field.Field.load('field'+str(N)+'.txt')
        
        desktop = QApplication.desktop()
        self.cellsize = min((desktop.width()-200)//self.field.width,
                            (desktop.height()-200)//self.field.height)
        self.cellsize3 = self.cellsize//3
        self.setFixedSize(self.cellsize*self.field.width,
                          self.cellsize*self.field.height)
        self.cellsize6 = self.cellsize//6
        self.cellsize23 = self.cellsize3*2
        self.qp = QPainter()

    def paintCell(self, i, j):
        self.qp.drawRect(j*self.cellsize, i*self.cellsize,
                         self.cellsize, self.cellsize)
        
    def paintWinningCell(self, i, j):
        self.qp.drawRect(j*self.cellsize+self.cellsize3,
                         i*self.cellsize+self.cellsize3,
                         self.cellsize3, self.cellsize3)

    def paintGrid(self):
        self.qp.setPen(Qt.black)
        for i in range(self.field.height):
            self.qp.drawLine(0, i*self.cellsize, self.height(), i*self.cellsize)
        for i in range(self.field.width):
            self.qp.drawLine(i*self.cellsize, 0, i*self.cellsize, self.width())

    def setCellColor(self, i, j):
        celltype = self.field.index(i, j)
        if celltype == -1 :
            self.qp.setBrush(Qt.NoBrush)
        elif celltype == 0 :
            self.qp.setBrush(Qt.black)
        elif celltype == 1 :
            self.qp.setBrush(Qt.green)
        elif celltype == 2 :
            self.qp.setBrush(Qt.blue)
        elif celltype == 3 :
            self.qp.setBrush(Qt.yellow)
        elif celltype == 4 :
            self.qp.setBrush(Qt.red)

    def paintField(self):
        self.qp.setPen(Qt.black)
        for i in range(self.field.height):
            for j in range(self.field.width):
                self.setCellColor(i, j)
                self.paintCell(i, j)

    def paintWinningPosition(self):
        self.qp.setBrush(Qt.cyan)
        for i, j in self.field.winningPosition():
            self.paintWinningCell(i, j)

    def mousePressEvent(self, mousePressEvent):
        i, j = self.pressedCell(mousePressEvent)
        self.field.pressCell(i, j)
        self.repaint()

    def pressedCell(self, mousePressEvent):
        pos = mousePressEvent.pos()
        return pos.y()//self.cellsize, pos.x()//self.cellsize

    def paintSelectedCell(self):
        i, j = self.field.selectedCell()
        self.setCellColor(i, j)
        self.qp.drawRect(j*self.cellsize-self.cellsize6,
                         i*self.cellsize-self.cellsize6,
                         self.cellsize+self.cellsize3,
                         self.cellsize+self.cellsize3)

    def paintAvailableMove(self, i, j):
        self.qp.drawRect(j*self.cellsize+self.cellsize6,
                         i*self.cellsize+self.cellsize6,
                         self.cellsize23, self.cellsize23)

    def paintAvailableMoves(self):
        x, y = self.field.selectedCell()
        self.qp.setBrush(Qt.magenta)
        for i, j in self.field.availableMoves()[x][y]:
            self.paintAvailableMove(i, j)

    def paintEvent(self, e):
        self.qp.begin(self)
        self.paintGrid()
        self.paintField()
        if self.field.selectedCell():
            self.paintAvailableMoves()
            self.paintSelectedCell()
        self.paintWinningPosition()
        self.qp.end()


if __name__ == '__main__':
    qapp = QApplication([])
    wtf = MainWindow()
    wtf.show()
    sys.exit(qapp.exec_())
