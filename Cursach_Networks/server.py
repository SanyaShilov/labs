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
    db.users.find_and_modify({}, {'$set': {'online': False}})
    db.command(
        'collMod', 'users',
        validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['login', 'password', 'online'],
                'properties': {
                    'login': {
                        'bsonType': 'string',
                        'description': 'login description'
                    },
                    'password': {
                        'bsonType': 'string',
                        'description': 'password description'
                    },
                    'online': {
                        'bsonType': 'bool',
                        'description': 'online description'
                    }
                }
            }
        }
    )
    db.maps.ensure_index('name', unique=True)
    db.users.delete_many({})
    db.users.insert_one(
        {
            'login': '111',
            'password': '111',
            'online': False
        }
    )
    return db


class Server:
    def __init__(self):
        self.socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
        self.socket.setsockopt(socketlib.SOL_SOCKET, socketlib.SO_REUSEADDR, 1)
        self.socket.bind((const.SERVER_IP, const.SERVER_PORT))
        self.client_sockets = []
        self.waiting_socket = None
        self.users_online = {}  # socket.fileno(): user
        self.db = create_db()

    def run_forever(self):
        self.socket.listen()
        while True:
            rlst, wlst, xlst = select.select(
                [self.socket] + self.client_sockets, [], []
            )
            for socket in rlst:
                if socket.fileno() == self.socket.fileno():
                    new_socket, addr = socket.accept()
                    print(addr)
                    self.client_sockets.append(new_socket)
                else:
                    data = protocol.recv_data(socket)
                    if data is None:
                        self.execute_command(socket, {'command': 'SIGN_OUT'})
                        self.client_sockets.remove(socket)
                    else:
                        self.execute_command(socket, data)

    def execute_command(self, socket, data):
        command = data['command']
        if command == 'SIGN_IN':
            self.sign_in(socket, data)
        elif command == 'REGISTER':
            self.register(socket, data)
        elif command == 'SIGN_OUT':
            self.sign_out(socket)
        elif command == 'WANT_TO_PLAY':
            self.handle_want_to_play(socket, data)
        elif command == 'DONT_WANT_TO_PLAY':
            self.handle_dont_want_to_play(socket, data)

    def sign_in(self, socket, data):
        user = self.db.users.find_one_and_update(
            {
                'login': data['login'],
                'password': data['password'],
                'online': False
            },
            {
                '$set': {
                    'online': True
                }
            }
        )
        if user:
            self.users_online[socket.fileno()] = user
            protocol.send_data(socket, {'status': 'ok'})
        else:
            protocol.send_data(socket, {'status': 'error'})

    def register(self, socket, data):
        new_user = {
            'login': data['login'],
            'password': data['password'],
            'online': True
        }
        user = self.db.users.find_one_and_update(
            {
                '$or': [
                    {
                        'login': data['login']
                    },
                    {
                        'password': data['password']
                    }
                ]
            },
            {
                '$setOnInsert': new_user
            },
            upsert=True
        )
        if user:
            protocol.send_data(socket, {'status': 'error'})
        else:
            self.users_online[socket.fileno()] = new_user
            protocol.send_data(socket, {'status': 'ok'})

    def sign_out(self, socket):
        if socket.fileno() in self.users_online:
            self.db.users.find_one_and_update(
                {
                    'login': self.users_online[socket.fileno()]['login']
                },
                {
                    '$set': {
                        'online': False
                    }
                }
            )
            del self.users_online[socket.fileno()]

    def handle_want_to_play(self, socket, data):
        if not self.waiting_socket:
            self.waiting_socket = {
                'ip': data['ip'],
                'port': data['port']
            }
            protocol.send_data(socket, {'status': 'wait'})
        else:
            protocol.send_data(socket, {'status': 'ok', 'socket': self.waiting_socket})
            self.waiting_socket = None

    def handle_dont_want_to_play(self, socket, data):
        self.waiting_socket = None


if __name__ == '__main__':
    server = Server()
    server.run_forever()
