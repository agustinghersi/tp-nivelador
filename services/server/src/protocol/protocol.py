import socket
from safe_socket import recv_all

# Aca defino la primer comunicación del protocolo
# Recibo el largo de la linea en 4 bytes para que el server la lea dinamicamente
def recv_size(socket: socket.socket):
    BytesToRecv = recv_all(socket, 4)
    return int(BytesToRecv.decode('ascii')) # Paso de string a int