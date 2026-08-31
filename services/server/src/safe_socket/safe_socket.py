import socket

# TODO: Complete with a short-read/short-write tolerant implementation

def recv_all(socket: socket.socket, size):
    message = bytearray()

    while len(message) < size:
        bytesRecv = socket.recv(size - len(message))
        if not bytesRecv:
            raise ConnectionError("No se recibio ningun byte")
        message.extend(bytesRecv)
    return bytes(message)


def send_all(socket: socket.socket, bytes):
    BytesSent = 0
    while BytesSent < len(bytes):
        bytesSent = socket.send(bytes[BytesSent:])
        if bytesSent == 0:
            raise Exception("No se pudo enviar ningun byte")
        BytesSent += bytesSent
    return None
