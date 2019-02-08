#!/usr/bin/python3.6

import random
import socket as socketlib

from PyQt5.QtWidgets import (QApplication, QMainWindow)

import protocol

import content_champions
import content_game
import content_main
import content_main_not_signed
import content_register
import content_sign_in
import content_waiting

import game

import messageboxes


class Application(QMainWindow, protocol.Participant):
    def __init__(self):
        self.qapp = QApplication([])
        QMainWindow.__init__(self)
        protocol.Participant.__init__(self)

        self.server_socket = socketlib.socket(
            socketlib.AF_INET, socketlib.SOCK_STREAM
        )
        self.server_socket.connect((protocol.SERVER_IP, protocol.SERVER_PORT))

        self.client_socket = None

        self.go_back_func = None
        self.timer_id = self.startTimer(100)

        self.login = None
        self.opponent = None
        self.color = None
        self.opponent_color = None
        self.game = None
        self.champions = None

        self.setFixedSize(1200, 800)
        self.move(
            400 + random.randint(-200, 200), 100 + random.randint(-100, 100)
        )
        self.show_content_main_not_signed()
        self.setWindowTitle(
            'Курсовой проект по компьютерным сетям Шилов ИУ7-72'
        )

    # show content

    def show_content_champions(self):
        self.setCentralWidget(content_champions.ContentChampions(self))

    def show_content_main(self):
        self.setCentralWidget(content_main.ContentMain(self))

    def show_content_main_not_signed(self):
        self.setCentralWidget(
            content_main_not_signed.ContentMainNotSigned(self)
        )

    def show_content_game(self):
        self.setCentralWidget(content_game.ContentGame(self))

    def show_content_register(self):
        self.setCentralWidget(content_register.ContentRegister(self))

    def show_content_sign_in(self):
        self.setCentralWidget(content_sign_in.ContentSignIn(self))

    def show_content_waiting(self):
        self.setCentralWidget(content_waiting.ContentWaiting(self))

    # send command

    def send_sign_in(self, login, password):
        self.send_data(
            self.server_socket,
            {
                'command': 'SIGN_IN',
                'login': login,
                'password': password
            }
        )
        data = self.recv_data(self.server_socket)
        if data['status'] == 'ok':
            self.login = login
            self.show_content_main()

    def send_register(self, login, password):
        self.send_data(
            self.server_socket,
            {
                'command': 'REGISTER',
                'login': login,
                'password': password
            }
        )
        data = self.recv_data(self.server_socket)
        if data['status'] == 'ok':
            self.login = login
            self.show_content_main()

    def send_sign_out(self):
        self.send_data(
            self.server_socket,
            {
                'command': 'SIGN_OUT',
            }
        )
        self.login = None
        self.show_content_main_not_signed()

    def send_want_to_play(self):
        self.send_data(
            self.server_socket,
            {
                'command': 'WANT_TO_PLAY',
                'ip': self.server_socket.getsockname()[0],
                'port': self.listening_socket.getsockname()[1],
                'login': self.login
            }
        )
        data = self.recv_data(self.server_socket)
        if data['status'] == 'wait':
            self.color = 'white'
            self.opponent_color = 'black'
            self.show_content_waiting()
        else:
            self.color = 'black'
            self.opponent_color = 'white'
            self.client_socket = socketlib.socket(
                socketlib.AF_INET, socketlib.SOCK_STREAM)
            self.client_socket.connect(
                (data['player']['ip'], data['player']['port']))
            self.selected_sockets.append(self.client_socket)
            self.game = game.Game(**data['map'])
            self.game.locked = True
            self.opponent = data['player']['login']
            self.send_data(
                self.client_socket,
                {
                    'command': 'START_PLAY',
                    'map': data['map'],
                    'opponent': self.login
                }
            )
            self.show_content_game()

    def send_give_up(self):
        if messageboxes.sure_to_give_up() == messageboxes.YES:
            self.clear()
            self.show_content_main()

    def send_dont_want_to_play(self):
        self.send_data(
            self.server_socket,
            {
                'command': 'DONT_WANT_TO_PLAY'
            }
        )
        self.clear()
        self.show_content_main()

    def send_show_champions(self, go_back_func):
        self.send_data(
            self.server_socket,
            {
                'command': 'SHOW_CHAMPIONS'
            }
        )
        data = self.recv_data(self.server_socket)
        self.champions = data['champions']
        self.go(self.show_content_champions, go_back_func)()

    def send_win(self):
        self.send_data(
            self.server_socket,
            {
                'command': 'WIN',
                'login': self.login,
                'opponent': self.opponent
            }
        )

    # execute command

    def execute_command(self, socket, data):
        if data['command'] == 'START_PLAY':
            self.execute_start_play(data)
        if data['command'] == 'MOVE':
            self.execute_move(data)
        if data['command'] == 'LOOSE':
            self.execute_loose(data)

    def execute_start_play(self, data):
        self.game = game.Game(**data['map'])
        self.opponent = data['opponent']
        self.show_content_game()

    def execute_move(self, data):
        self.game.locked = False
        self.game.press_cell(*data['from'])
        self.game.press_cell(*data['to'])
        self.content_game.repaint()

    def execute_loose(self, data):
        self.execute_move(data)
        self.clear()
        messageboxes.loose()
        self.show_content_main()

    # other

    def handle_press_cell(self, result):
        if result['result'] == 'MOVE':
            self.game.locked = True
            self.content_game.repaint()
            data = {
                'command': 'MOVE',
                'from': result['from'],
                'to': result['to']
            }
            if (
                    self.color == 'white' and self.game.white_win() or
                    self.color == 'black' and self.game.black_win()
            ):
                data['command'] = 'LOOSE'
            self.send_data(self.client_socket, data)
            if data['command'] == 'LOOSE':
                self.clear()
                self.send_win()
                messageboxes.win()
                self.show_content_main()

    def clear(self):
        self.selected_sockets.clear()
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None

    def go(self, func, go_back_func):
        def _go():
            self.go_back_func = go_back_func
            return func()

        return _go

    def go_back(self):
        self.go_back_func()

    def start(self):
        self.update()
        self.show()
        self.qapp.exec_()

    def timerEvent(self, event):
        self.select(0)

    def closeEvent(self, event):
        if self.client_socket:
            if messageboxes.sure_to_give_up() == messageboxes.YES:
                event.accept()
            else:
                event.ignore()

    def handle_new_socket(self, socket):
        self.client_socket = socket

    def handle_empty_command(self, socket):
        self.clear()
        self.send_win()
        messageboxes.opponent_give_up()
        self.show_content_main()


def main():
    app = Application()
    app.start()


if __name__ == '__main__':
    main()
