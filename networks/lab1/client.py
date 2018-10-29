#!/usr/bin/python3.6

import socket

IP = '127.0.0.1'
PORT = 9090
MESSAGE = bytes('hello, world!', 'utf-8')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (IP, PORT))

