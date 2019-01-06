from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

import game
import widgets


class FakeApp:
    def __init__(self):
        map = {
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
        self.game = game.Game(**map)
        self.login = 'test login'
        self.opponent = 'test opponent'
        self.color = 'white'
        self.opponent_color = 'black'

    @staticmethod
    def width():
        return 800

    @staticmethod
    def height():
        return 800

    def handle_press_cell(self, result):
        pass


class ContentGame(widgets.Content):
    def __init__(self, app):
        super().__init__(app)
        self.app.content_game = self
        self.content = _ContentGame(app, self)
        self.content.move(0, 0)
        self.setFixedSize(self.content.width() + 400, self.content.height())
        self.color_lbl = widgets.Label('({})'.format(app.color), self, 200, 50, 900, 100, alignment='center')
        self.vs_lbl = widgets.Label('playing vs.', self, 200, 50, 900, 150, alignment='center')
        self.opponent_lbl = widgets.Label(app.opponent, self, 200, 50, 900, 200, alignment='center')
        self.opponent_color_lbl = widgets.Label('({})'.format(app.opponent_color), self, 200, 50, 900, 250, alignment='center')
        self.turn_lbl = widgets.Label('', self, 200, 50, 900, 400, alignment='center')

        self.give_up_btn = widgets.PushButton(
            'Give up', self, 200, 100, 900, 600,
            app.send_give_up
        )

        self.repaint()

    def repaint(self):
        self.content.repaint()
        if self.content.game.locked:
            self.turn_lbl.setText('Opponent turn')
        else:
            self.turn_lbl.setText('Your turn')


class _ContentGame(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent=parent)
        self.app = app
        self.game = app.game

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
        self.qp.drawRect(j * self.cellsize + self.cellsize3, i * self.cellsize + self.cellsize3,
                         self.cellsize3, self.cellsize3)

    def paint_winning_cell(self, i, j):
        self.qp.drawRect(j * self.cellsize,
                         (i + 1) * self.cellsize - self.cellsize4,
                         self.cellsize, self.cellsize4)

    def paint_grid(self):
        self.qp.setPen(Qt.black)
        for i in range(self.game.height):
            self.qp.drawLine(
                0,
                i * self.cellsize,
                self.height(),
                i * self.cellsize)
        for i in range(self.game.width):
            self.qp.drawLine(
                i * self.cellsize,
                0,
                i * self.cellsize,
                self.width())

    def set_cell_color(self, i, j):
        celltype = self.game.map[i][j]
        if celltype == game.EMPTY:
            self.qp.setBrush(Qt.lightGray)
        elif celltype == game.BLOCK:
            self.qp.setBrush(Qt.darkGray)
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

    def paint_flags(self):
        for i in range(self.game.height):
            for j in range(self.game.width):
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
        result = self.game.press_cell(i, j)
        self.repaint()
        self.app.handle_press_cell(result)

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
        self.paint_flags()
        self.qp.end()


def main():
    qapp = QApplication([])
    content = ContentGame(FakeApp())
    content.show()
    qapp.exec_()


if __name__ == '__main__':
    main()
