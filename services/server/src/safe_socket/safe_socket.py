import socket

# TODO: Complete with a short-read/short-write tolerant implementation

# Aca defino la primer comunicación del protocolo
# Recibo el largo de la linea en 4 bytes para que el server la lea dinamicamente
def recv_size(socket: socket.socket):
    BytesToRecv = recv_all(socket, 4)
    return int(BytesToRecv.decode('ascii')) # Paso de string a int

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
