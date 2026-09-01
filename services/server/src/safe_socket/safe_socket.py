import socket

# TODO: Complete with a short-read/short-write tolerant implementation

def recv_all(socket: socket.socket, size):
    return socket.recv(size)


def send_all(socket: socket.socket, bytes):
    """ BytesSent = 0
    while BytesSent < len(bytes):
        bytesSent = socket.send(bytes[BytesSent:])
        if bytesSent == 0:
            raise Exception("No se pudo enviar ningun byte")
        BytesSent += bytesSent
    return None """
    return socket.send(bytes)

def recv_agency(socket: socket.socket):
    agency = socket.recv(1) # Por protocolo
    if not agency:
        raise ConnectionError("No se recibio ningun byte")
    return agency