from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDockWidget)

import stuff

import content_champions
import content_main
import content_main_not_signed
import content_register
import content_sign_in


@stuff.singleton
class View (QMainWindow):
    def __init__ (self):
        self.qapp = QApplication([])
        super().__init__()
        self.go_back_func = None

    def init(self):
        self.setFixedSize(1200, 800)
        self.move(400, 100)
        self.show_content_main_not_signed()
        self.setWindowTitle('Курсовой проект по компьютерным сетям Шилов ИУ7-72')

    # contents

    def show_content_champions(self):
        self.setCentralWidget(content_champions.ContentChampions())

    def show_content_main(self):
        self.setCentralWidget(content_main.ContentMain())

    def show_content_main_not_signed(self):
        self.setCentralWidget(content_main_not_signed.ContentMainNotSigned(self))

    def show_content_register(self):
        self.setCentralWidget(content_register.ContentRegister())

    def show_content_sign_in(self):
        self.setCentralWidget(content_sign_in.ContentSignIn(self))

    # other

    def go(self, func, go_back_func):
        self.go_back_func = go_back_func
        return func

    def go_back(self):
        self.go_back_func()

    def start_application (self):
        self.update()
        self.show()
        self.qapp.exec_()

    def closeEvent (self, e):
        e.accept()
