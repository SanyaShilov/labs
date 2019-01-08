#!/usr/bin/python3.6

import db
import protocol


class Server(protocol.Participant):
    IP = protocol.SERVER_IP
    PORT = protocol.SERVER_PORT

    def __init__(self):
        super().__init__()

        self.waiting_player = None
        self.users_online = {}  # socket.fileno(): user
        self.db = db.create_db()

    def execute_command(self, socket, data):
        command = data['command']
        if command == 'SIGN_IN':
            self.execute_sign_in(socket, data)
        elif command == 'REGISTER':
            self.execute_register(socket, data)
        elif command == 'SIGN_OUT':
            self.execute_sign_out(socket)
        elif command == 'WANT_TO_PLAY':
            self.execute_want_to_play(socket, data)
        elif command == 'DONT_WANT_TO_PLAY':
            self.execute_dont_want_to_play()

    def execute_sign_in(self, socket, data):
        if data['login'] in [
                user['login'] for user in self.users_online.values()
        ]:
            user = None
        else:
            user = self.db.users.find_one(
                {
                    'login': data['login'],
                    'password': data['password'],
                }
            )
        if user:
            self.users_online[socket.fileno()] = user
            self.send_data(socket, {'status': 'ok'})
        else:
            self.send_data(socket, {'status': 'error'})

    def execute_register(self, socket, data):
        new_user = {
            'login': data['login'],
            'password': data['password'],
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
            self.send_data(socket, {'status': 'error'})
        else:
            self.users_online[socket.fileno()] = new_user
            self.send_data(socket, {'status': 'ok'})

    def execute_sign_out(self, socket):
        if socket.fileno() in self.users_online:
            del self.users_online[socket.fileno()]

    def execute_want_to_play(self, socket, data):
        if not self.waiting_player:
            self.waiting_player = {
                'ip': data['ip'],
                'port': data['port'],
                'login': data['login']
            }
            self.send_data(socket, {'status': 'wait'})
        else:
            map = list(self.db.maps.aggregate([{'$sample': {'size': 1}}]))[0]
            map.pop('_id')
            self.send_data(
                socket,
                {
                    'status': 'ok',
                    'player': self.waiting_player,
                    'map': map,
                }
            )
            self.waiting_player = None

    def execute_dont_want_to_play(self):
        self.waiting_player = None

    def handle_empty_command(self, socket):
        self.execute_sign_out(socket)


def main():
    server = Server()
    server.run_forever()


if __name__ == '__main__':
    main()
