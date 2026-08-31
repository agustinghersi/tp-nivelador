import socket
from safe_socket import recv_all
from lottery.bet import Bet

# Aca defino la primer comunicación del protocolo
# Recibo el largo de la linea en 4 bytes para que el server la lea dinamicamente
def recv_size(socket: socket.socket):
    BytesToRecv = recv_all(socket, 4)
    return int(BytesToRecv.decode('ascii')) # Paso de string a int

# Deserializo el mensaje y lo convierto en un Bet
def create_bet(message: str):
    bets = [] # Momentaneamente solo hay una hasta ej 6
    message = message.decode("utf-8") # Esto deberia ser util cuando prtocolo maneje binario

    array_message = message.split(",")
    bet = Bet(
        agency_id = 1, # Hacer una funcion de protocolo que al crear la conexion mande el id de la agencia una vez
        first_name = array_message[0],
        last_name = array_message[1],
        document = int(array_message[2]),
        birthdate = array_message[3],
        number = int(array_message[4]),
    )
    
    bets.append(bet)
    return bets
