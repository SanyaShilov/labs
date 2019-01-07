import abc
import json
import select
import socket as socket_module
import threading


N = 4


def convert_length_to_bytes(length):
    return bytes([(length >> i) % 256 for i in range((N - 1) * 8, -8, -8)])


def convert_bytes_to_length(bytes):
    return sum(bytes[i] << ((N - 1 - i) * 8) for i in range(N))


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


def send_data(socket, data):
    data = bytes(json.dumps(data), encoding='utf-8')
    length = len(data)
    socket.send(convert_length_to_bytes(length))
    socket.send(data)


class Participant(abc.ABC):
    IP = ''
    PORT = 0

    def __init__(self):
        self.listening_socket = socket_module.socket(
            socket_module.AF_INET, socket_module.SOCK_STREAM
        )
        self.listening_socket.bind((self.IP, self.PORT))
        self.listening_socket.listen()

        self.selected_sockets = []

    @staticmethod
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

    @staticmethod
    def send_data(socket, data):
        data = bytes(json.dumps(data), encoding='utf-8')
        length = len(data)
        socket.send(convert_length_to_bytes(length))
        socket.send(data)

    def run_forever(self):
        while True:
            rlst, _, _ = select.select(
                [self.listening_socket] + self.selected_sockets, [], []
            )
            for socket in rlst:
                if socket.fileno() == self.listening_socket.fileno():
                    new_socket, _ = socket.accept()
                    self.selected_sockets.append(new_socket)
                else:
                    data = recv_data(socket)
                    if data is None:
                        self.handle_empty_command(socket)
                        self.selected_sockets.remove(socket)
                    else:
                        self.execute_command(socket, data)

    def run_forever_in_thread(self):
        threading.Thread(target=self.run_forever).start()

    @abc.abstractmethod
    def handle_empty_command(self, socket):
        pass

    @abc.abstractmethod
    def execute_command(self, socket, command):
        pass
