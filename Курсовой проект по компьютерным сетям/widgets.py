from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox)


FONT = QFont('Times New Roman', 24, 1)


class Content(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent=parent)
        self.app = app
        if self.app.login:
            self.login_lbl = Label(
                app.login, self, 200, 50, 900, 50, alignment='center'
            )


class PushButton(QPushButton):
    def __init__(self, string='', parent=None,
                 width=None, height=None,
                 pos_x=None, pos_y=None,
                 slot=None):
        super().__init__(string, parent)
        self.setFont(FONT)
        if width is not None and height is not None:
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None:
            self.move(pos_x, pos_y)
        if slot is not None:
            self.clicked.connect(slot)


class Label(QLabel):
    def __init__(self, string='', parent=None,
                 width=None, height=None,
                 pos_x=None, pos_y=None,
                 alignment=None, font=FONT):
        super().__init__(string, parent)
        self.setFont(font)
        if width is not None and height is not None:
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None:
            self.move(pos_x, pos_y)
        if alignment is not None:
            if alignment == 'center':
                self.setAlignment(Qt.AlignCenter)


class LineEdit(QLineEdit):
    def __init__(self, string='', parent=None,
                 width=None, height=None,
                 pos_x=None, pos_y=None):
        super().__init__(string, parent)
        self.setFont(FONT)
        if width is not None and height is not None:
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None:
            self.move(pos_x, pos_y)


class MessageBox(QMessageBox):
    def __init__(self, title='', text='',
                 standard_buttons=0, default_button=0):
        super().__init__()
        self.setWindowTitle(title)
        self.setInformativeText(text)
        self.setStandardButtons(standard_buttons)
        self.setDefaultButton(default_button)


class Item(QTableWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlags(self.flags() & (~ Qt.ItemIsEditable))


class Table(QTableWidget):
    def __init__(self, parent=None,
                 width=None, height=None,
                 pos_x=None, pos_y=None):
        super().__init__(parent)
        self.setFont(FONT)
        if width is not None and height is not None:
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None:
            self.move(pos_x, pos_y)
