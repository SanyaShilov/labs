#!/usr/bin/python3.6

from pprint import pprint
import select
import socket as socketlib
import sys
import time

import pymongo

import const
import protocol


def create_db():
    mongo_client = pymongo.MongoClient()
    db = mongo_client.networks
    db.users.ensure_index('login', unique=True)
    db.users.ensure_index('password', unique=True)
    db.maps.ensure_index('name', unique=True)
    return db


class Server:
    def __init__(self):
        self.socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
        self.socket.setsockopt(socketlib.SOL_SOCKET, socketlib.SO_REUSEADDR, 1)
        self.socket.bind((const.SERVER_IP, const.SERVER_PORT))
        self.client_sockets = []
        self.db = create_db()

    def run_forever(self):
        self.socket.listen()
        while True:
            rlst, wlst, xlst = select.select(
                [self.socket] + self.client_sockets, [], []
            )
            for socket in rlst:
                if socket.fileno() == self.socket.fileno():
                    new_socket = socket.accept()[0]
                    self.client_sockets.append(new_socket)
                else:
                    data = protocol.recv_data(socket)
                    pprint(data)
                    if data is None:
                        self.client_sockets.remove(socket)
                    else:
                        self.execute_command(socket, data)

    def execute_command(self, socket, data):
        pass


if __name__ == '__main__':
    pass
    server = Server()
    server.run_forever()
