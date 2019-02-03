import json
import select
import socket as socketlib


N = 4

SERVER_IP = '192.168.1.239'
SERVER_PORT = 9090


def convert_length_to_bytes(length):
    return bytes([(length >> i) % 256 for i in range((N - 1) * 8, -8, -8)])


def convert_bytes_to_length(bytes):
    return sum(bytes[i] << ((N - 1 - i) * 8) for i in range(N))


def send_data(socket, data):
    data = bytes(json.dumps(data), encoding='utf-8')
    length = len(data)
    socket.send(convert_length_to_bytes(length))
    socket.send(data)


def recv_data(socket):
    try:
        data = socket.recv(N)
    except Exception:
        data = None
    if not data:
        return None
    length = convert_bytes_to_length(data)
    data = socket.recv(length)
    return json.loads(str(data, encoding='utf-8'))


class Participant:
    IP = ''
    PORT = 0

    def __init__(self):
        self.listening_socket = socketlib.socket(
            socketlib.AF_INET, socketlib.SOCK_STREAM
        )
        self.listening_socket.setsockopt(
            socketlib.SOL_SOCKET, socketlib.SO_REUSEADDR, 1
        )
        self.listening_socket.bind((self.IP, self.PORT))
        self.listening_socket.listen()

        self.selected_sockets = []

    @staticmethod
    def recv_data(socket):
        return recv_data(socket)

    @staticmethod
    def send_data(socket, data):
        send_data(socket, data)

    def select(self, timeout=None):
        rlst, _, _ = select.select(
            [self.listening_socket] + self.selected_sockets, [], [], timeout
        )
        for socket in rlst:
            if socket.fileno() == self.listening_socket.fileno():
                new_socket, _ = socket.accept()
                self.selected_sockets.append(new_socket)
                self.handle_new_socket(new_socket)
            else:
                data = self.recv_data(socket)
                if data is None:
                    self.selected_sockets.remove(socket)
                    self.handle_empty_command(socket)
                else:
                    self.execute_command(socket, data)

    def run_forever(self):
        while True:
            self.select()

    def handle_new_socket(self, socket):
        pass

    def handle_empty_command(self, socket):
        pass

    def execute_command(self, socket, data):
        pass
