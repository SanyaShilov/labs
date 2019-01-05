from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

import game
import widgets


class FakeApp:
    def __init__(self):
        self.map = {
            'map': [
                [1, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 5, 5],
                [0, 0, 0, 0, 0, 0, 5, 5],
            ],
            'white_winning_position': [
                [6, 6], [6, 7], [7, 6], [7, 7]
            ],
            'black_winning_position': [
                [0, 0], [0, 1], [1, 0], [1, 1]
            ]
        }

    @staticmethod
    def width():
        return 800

    @staticmethod
    def height():
        return 800


class ContentGame(widgets.Content):
    def __init__(self, app):
        super().__init__(app)
        self.game = game.Game(**app.map)

        self.cellsize = min(app.width() // self.game.width,
                            app.height() // self.game.height)
        self.cellsize3 = self.cellsize // 3
        self.cellsize4 = self.cellsize // 4
        self.setFixedSize(self.cellsize * self.game.width,
                          self.cellsize * self.game.height)
        self.cellsize6 = self.cellsize // 6
        self.cellsize23 = self.cellsize3 * 2
        self.cellsize34 = self.cellsize4 * 3
        self.qp = QPainter()

    def paint_cell(self, i, j):
        self.qp.drawRect(j * self.cellsize, i * self.cellsize,
                         self.cellsize, self.cellsize)

    def paint_flag(self, i, j):
        self.qp.drawRect(j * self.cellsize, i * self.cellsize,
                         self.cellsize4, self.cellsize4)

    def paint_winning_cell(self, i, j):
        self.qp.drawRect(j * self.cellsize,
                         (i + 1) * self.cellsize - self.cellsize4,
                         self.cellsize, self.cellsize4)

    def paint_grid(self):
        self.qp.setPen(Qt.black)
        for i in range(self.game.height):
            self.qp.drawLine(0, i * self.cellsize, self.height(), i * self.cellsize)
        for i in range(self.game.width):
            self.qp.drawLine(i * self.cellsize, 0, i * self.cellsize, self.width())

    def set_cell_color(self, i, j):
        celltype = self.game.map[i][j]
        if celltype == game.EMPTY:
            self.qp.setBrush(Qt.NoBrush)
        elif celltype == game.BLOCK:
            self.qp.setBrush(Qt.black)
        elif celltype in game.TYPE1:
            self.qp.setBrush(Qt.green)
        elif celltype in game.TYPE2:
            self.qp.setBrush(Qt.blue)
        elif celltype in game.TYPE3:
            self.qp.setBrush(Qt.yellow)
        elif celltype in game.TYPE4:
            self.qp.setBrush(Qt.red)

    def paint_field(self):
        self.qp.setPen(Qt.black)
        for i in range(self.game.height):
            for j in range(self.game.width):
                self.set_cell_color(i, j)
                self.paint_cell(i, j)
                if self.game.map[i][j] in game.WHITE_FIGURES:
                    self.qp.setBrush(Qt.white)
                    self.paint_flag(i, j)
                if self.game.map[i][j] in game.BLACK_FIGURES:
                    self.qp.setBrush(Qt.black)
                    self.paint_flag(i, j)

    def paint_winning_position(self):
        self.qp.setBrush(Qt.white)
        for i, j in self.game.white_winning_position:
            self.paint_winning_cell(i, j)
        self.qp.setBrush(Qt.black)
        for i, j in self.game.black_winning_position:
            self.paint_winning_cell(i, j)

    def mousePressEvent(self, event):
        i, j = self.pressed_cell(event)
        self.game.press_cell(i, j)
        self.repaint()

    def pressed_cell(self, event):
        pos = event.pos()
        return pos.y() // self.cellsize, pos.x() // self.cellsize

    def paint_selected_cell(self):
        i, j = self.game.selected_cell
        self.set_cell_color(i, j)
        self.qp.drawRect(j * self.cellsize - self.cellsize6,
                         i * self.cellsize - self.cellsize6,
                         self.cellsize + self.cellsize3,
                         self.cellsize + self.cellsize3)

    def paint_available_move(self, i, j):
        self.qp.drawRect(j * self.cellsize + self.cellsize6,
                         i * self.cellsize + self.cellsize6,
                         self.cellsize23, self.cellsize23)

    def paint_available_moves(self):
        for i, j in self.game.available_moves:
            self.paint_available_move(i, j)

    def paintEvent(self, event):
        self.qp.begin(self)
        self.paint_grid()
        self.paint_field()
        self.paint_winning_position()
        if self.game.selected_cell:
            self.paint_selected_cell()
            self.paint_available_moves()
        self.qp.end()


if __name__ == '__main__':
    qapp = QApplication([])
    wtf = ContentGame(FakeApp())
    wtf.show()
    qapp.exec_()
