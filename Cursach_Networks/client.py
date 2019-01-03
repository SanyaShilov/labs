#!/usr/bin/python3.6

from pprint import pprint
import socket
import os

import const
import protocol
from view import View


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const.SERVER_IP, const.SERVER_PORT))
        protocol.send_data(
            self.sock,
            {
                'command': 'SIGN_IN',
                'login': 'sanyash',
                'password': 'nyash_myash',
            }
        )
        protocol.send_data(self.sock, {'command': 'SHOW'})


if __name__ == '__main__':
    client = Client()
    view = View()
    view.init()
    view.start_application()
