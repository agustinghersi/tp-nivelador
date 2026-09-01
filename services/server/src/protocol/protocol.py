import socket
import safe_socket
from lottery.bet import Bet

# Aca defino la primer comunicación del protocolo
# Se recibe una sola vez la agencia del cliente con el que se comunica
def recv_agency(socket: socket.socket):
    return safe_socket.recv_all(socket, 1).decode('ascii')

# Recibo el largo de la linea en 4 bytes para que el server la lea dinamicamente
# Luego recibo el resto del mensaje
def recv_all(socket: socket.socket):
    # primero recupero la longitud del mensaje
    BytesToRecv = safe_socket.recv_all(socket, 4)
    if not BytesToRecv:
        raise ConnectionError("No se recibio ningun byte") # Ya se recibio la ultima linea

    # Ahora recibo la apuesta sabiendo longitud
    sizeMessage = int(BytesToRecv.decode('ascii'))
    bytesRecv = safe_socket.recv_all(socket, sizeMessage)
    if not bytesRecv:
        raise Exception("No se recibio ningun byte") # Aca no deberia llegar
    
    return bytesRecv

# Deserializo el mensaje y lo convierto en un Bet
def create_bet(message: str, agency: str):
    bets = [] # Momentaneamente solo hay una hasta ej 6
    message = message.decode("utf-8")

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

# Preparo el formato para mandar ganadores al cliente
def send_winners(socket: socket.socket, winners: list[Bet]):
    for winner in winners:
        # Formato esperado para guardar en el OUTPUT_FILE
        message = ",".join([
            winner.first_name, 
            winner.last_name, 
            str(winner.document), 
            winner.birthdate, 
            str(winner.number)
        ])
        message = message.encode("utf-8")
        messageSize = len(message)
        firstMessage = f"{messageSize:04d}".encode("ascii") # 4 bytes que indican longitud
        
        # Armo el mensaje completo, con longitud y apuesta, y lo envio
        message = firstMessage + message
        bytesSent = safe_socket.send_all(socket, message)

