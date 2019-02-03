import socket as socketlib

import protocol


socket: socketlib.socket


# вызывающая сторона
command = {
    'command': 'SOME_COMMAND',
    'some_structured_data': {
        'array': [1, 2, 3],
        'str': 'str'
    }
}
protocol.send_data(socket, command)
result = protocol.recv_data(socket)

# принимающая сторона
command = protocol.recv_data(socket)
if command['command'] == 'SOME_COMMAND':
    result = work_with_data(command['some_structured_data'])
    protocol.send_data(socket, result)
elif command['command'] == 'ANOTHER_COMMAND':
    ...
