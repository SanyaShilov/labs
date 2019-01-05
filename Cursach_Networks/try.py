import socket


def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    ip_address = sock.getsockname()[0]
    sock.close()
    return ip_address
