from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QPushButton,QTableWidget, QTableWidgetItem,
                             QMessageBox, QComboBox, QTextEdit, QHBoxLayout)

general_font = QFont('Times New Roman', 24, 1)
title_font = QFont('Times New Roman', 24, 1)


def base_init (self, base_cls, string, parent) :
    if isinstance(string, str) :
        base_cls.__init__(self, string, parent)
    elif isinstance(string, QWidget):
        base_cls.__init__(self, string)
    else :
        base_cls.__init__(self, parent)


def yes_no (boolean) :
    if boolean :
        return 'Yes'
    else :
        return 'No'


class Content (QWidget):
    def __init__ (self, app):
        super().__init__()
        self.app = app


class Header (QWidget) :
    def __init__ (self) :
        super().__init__()

        self.hbox = QHBoxLayout(self)
        self.hbox.addStretch(0)

    def add (self, btn) :
        self.hbox.addWidget(btn)


class PushButton (QPushButton) :
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None,
                  slot = None) :
        base_init(self, QPushButton, string, parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)
        if slot is not None :
            self.clicked.connect(slot)


class Label(QLabel):
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None,
                  alignment = None, font = general_font) :
        base_init(self, QLabel, string, parent)
        self.setFont(font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)
        if alignment is not None:
            if alignment == 'center':
                self.setAlignment(Qt.AlignCenter)


class TextEdit(QTextEdit):
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None) :
        base_init(self, QTextEdit, string, parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)


class LineEdit(QLineEdit):
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None) :
        base_init(self, QLineEdit, string, parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)


class List (QComboBox) :
    def __init__ (self, parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None) :
        super().__init__(parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)


class MessageBox (QMessageBox) :
    pass


class Item (QTableWidgetItem) :
    def __init__ (self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.setFlags(self.flags() & (~ Qt.ItemIsEditable))


class Table (QTableWidget) :
    def __init__ (self, parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None) :
        super().__init__(parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)
