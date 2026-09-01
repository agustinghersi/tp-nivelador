import socket

# recibo la cantidad de bytes idicados en size por el socket
def recv_all(socket: socket.socket, size):
    bytesReceived = bytearray()
    while len(bytesReceived) < size:
        bytesToRecv = socket.recv(size - len(bytesReceived))
        if not bytesToRecv:
            raise ConnectionError("No se recibio ningun byte")
        bytesReceived.extend(bytesToRecv)
    return bytesReceived

# Envio los bytes
def send_all(socket: socket.socket, bytes):
    BytesSent = 0
    while BytesSent < len(bytes):
        bytesSent = socket.send(bytes[BytesSent:])
        if bytesSent == 0:
            raise Exception("No se pudo enviar ningun byte")
        BytesSent += bytesSent
    return None
