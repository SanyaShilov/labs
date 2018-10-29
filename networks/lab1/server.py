#!/usr/bin/python3.6

import socket

IP = '127.0.0.1'
PORT = 9090


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print(str(data, 'utf-8'))
    print(addr)
