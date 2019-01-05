import random
import select
import socket

from PyQt5.QtWidgets import (QApplication, QMainWindow)

import const
import protocol

import content_champions
import content_game
import content_main
import content_main_not_signed
import content_register
import content_sign_in
import content_waiting

import messageboxes


class Application(QMainWindow):
    def __init__(self):
        self.qapp = QApplication([])
        super().__init__()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((const.SERVER_IP, const.SERVER_PORT))

        self.own_server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.own_server_socket.bind((self.server_socket.getsockname()[0], 0))
        self.own_server_socket.listen()

        self.client_socket = None

        self.selected_sockets = []

        self.go_back_func = None
        self.timer_id = None

        self.map = None

        self.setFixedSize(1200, 800)
        self.move(400 + random.randint(-100, 100), 100 + random.randint(-50, 50))
        self.show_content_main_not_signed()
        self.setWindowTitle(
            'Курсовой проект по компьютерным сетям Шилов ИУ7-72')

    # contents

    def show_content_champions(self):
        self.setCentralWidget(content_champions.ContentChampions(self))

    def show_content_main(self):
        self.setCentralWidget(content_main.ContentMain(self))

    def show_content_main_not_signed(self):
        self.setCentralWidget(
            content_main_not_signed.ContentMainNotSigned(self))

    def show_content_game(self):
        self.setCentralWidget(content_game.ContentGame(self))

    def show_content_register(self):
        self.setCentralWidget(content_register.ContentRegister(self))

    def show_content_sign_in(self):
        self.setCentralWidget(content_sign_in.ContentSignIn(self))

    def show_content_waiting(self):
        self.setCentralWidget(content_waiting.ContentWaiting(self))

    # actions

    def sign_in(self, login, password):
        protocol.send_data(
            self.server_socket,
            {
                'command': 'SIGN_IN',
                'login': login,
                'password': password
            }
        )
        data = protocol.recv_data(self.server_socket)
        if data['status'] == 'ok':
            self.show_content_main()

    def register(self, login, password):
        protocol.send_data(
            self.server_socket,
            {
                'command': 'REGISTER',
                'login': login,
                'password': password
            }
        )
        data = protocol.recv_data(self.server_socket)
        if data['status'] == 'ok':
            self.show_content_main()

    def sign_out(self):
        protocol.send_data(
            self.server_socket,
            {
                'command': 'SIGN_OUT',
            }
        )
        self.show_content_main_not_signed()

    def want_to_play(self):
        protocol.send_data(
            self.server_socket,
            {
                'command': 'WANT_TO_PLAY',
                'ip': self.own_server_socket.getsockname()[0],
                'port': self.own_server_socket.getsockname()[1],
            }
        )
        data = protocol.recv_data(self.server_socket)
        if data['status'] == 'wait':
            self.selected_sockets.append(self.own_server_socket)
            self.show_content_waiting()
        else:
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(
                (data['socket']['ip'], data['socket']['port']))
            self.selected_sockets.append(self.client_socket)
            self.map = data['map']
            protocol.send_data(
                self.client_socket,
                {
                    'command': 'LOAD_MAP',
                    'map': self.map
                }
            )
            self.show_content_game()
        self.timer_id = self.startTimer(100)

    def remove_client_socket(self):
        if self.client_socket in self.selected_sockets:
            self.selected_sockets.remove(self.client_socket)
        self.client_socket.close()
        self.client_socket = None

    def recv_give_up(self):
        self.remove_client_socket()
        messageboxes.opponent_give_up(self)
        self.show_content_main()

    def send_give_up(self):
        if messageboxes.sure_to_give_up(self) == messageboxes.YES:
            self.remove_client_socket()
            self.show_content_main()

    def dont_want_to_play(self):
        protocol.send_data(
            self.server_socket,
            {
                'command': 'DONT_WANT_TO_PLAY'
            }
        )
        self.killTimer(self.timer_id)
        self.selected_sockets.remove(self.own_server_socket)
        self.show_content_main()

    def load_map(self, data):
        self.map = data['map']
        self.show_content_game()

    # other

    def execute_command(self, data):
        if data['command'] == 'LOAD_MAP':
            self.load_map(data)

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
        rlst, _, _ = select.select(
            self.selected_sockets, [], [], 0
        )
        for socket in rlst:
            if socket.fileno() == self.own_server_socket.fileno():
                self.client_socket = socket.accept()[0]
                self.selected_sockets.append(self.client_socket)
                self.selected_sockets.remove(self.own_server_socket)
            else:
                data = protocol.recv_data(socket)
                if data is None:
                    self.recv_give_up()
                else:
                    self.execute_command(data)
