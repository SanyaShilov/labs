import json


N = 4


def convert_length_to_bytes(length):
    return bytes([(length >> i) % 256 for i in range((N - 1) * 8, -8, -8)])


def convert_bytes_to_length(bytes):
    return sum(bytes[i] << ((N - 1 - i) * 8) for i in range(N))


def recv_data(sock):
    data = sock.recv(N)
    if not data:
        return None
    length = convert_bytes_to_length(data)
    data = sock.recv(length)
    return json.loads(str(data, encoding='utf-8'))


def send_data(sock, data):
    data = bytes(json.dumps(data), encoding='utf-8')
    length = len(data)
    sock.send(convert_length_to_bytes(length))
    sock.send(data)
