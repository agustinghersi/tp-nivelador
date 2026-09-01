import socket
from safe_socket import recv_all
from lottery.bet import Bet

# Aca defino la primer comunicación del protocolo
# Se recibe una sola vez la agencia del cliente con el que se comunica
def recv_agency(socket: socket.socket):
    return recv_all(socket, 1).decode('ascii')

# Recibo el largo de la linea en 4 bytes para que el server la lea dinamicamente
def recv_size(socket: socket.socket):
    BytesToRecv = recv_all(socket, 4)
    return int(BytesToRecv.decode('ascii')) # Paso de string a int

# Deserializo el mensaje y lo convierto en un Bet
def create_bet(message: str, agency: str):
    bets = [] # Momentaneamente solo hay una hasta ej 6
    message = message.decode("utf-8") # Esto deberia ser util cuando prtocolo maneje binario

    array_message = message.split(",")
    bet = Bet(
        agency_id = agency,
        first_name = array_message[0],
        last_name = array_message[1],
        document = int(array_message[2]),
        birthdate = array_message[3],
        number = int(array_message[4]),
    )
    
    bets.append(bet)
    return bets
