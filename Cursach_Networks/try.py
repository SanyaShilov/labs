import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()

def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('192.168.1.239', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return addr, port

print(get_free_tcp_port())