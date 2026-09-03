import socket
import logger
import protocol
from monitor import Monitor

import threading

class Server:
    def __init__(self, server_host: str, server_port: int) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.monitor = Monitor()

    def _handle_client(self, client_socket, monitor: monitor):
        action = "handle-client"
        message_amount = 0
        chunk_amount = 0 # Para contar la cantidad de chunks recibidos
        try:
            logger.info(action, logger.LogResult.in_progress)

            agency = protocol.recv_agency(client_socket)
            logger.info(action, logger.LogResult.success, "agency", agency)
            while True:
                client_messages = protocol.recv_all(
                    client_socket
                )
                if len(client_messages) == 0:
                    logger.info(
                        action,
                        logger.LogResult.success,
                        "messages-amount",
                        message_amount,
                    )
                    break # No va a llegar nada mas
                message_amount += len(client_messages)
                chunk_amount += 1

                bets = protocol.create_bet(client_messages, agency)
                monitor.store_bet(bets) # Adentro del monitor veo temas de concurrencia
            
            # Sacar el codigo repetido con el ConectionError
            monitor.register_agency()
            winners = monitor.get_winners(agency)
            logger.info(action, logger.LogResult.success, "winners", winners)
            # Envio ganadores
            protocol.send_winners(client_socket, winners)


        # Caso de conexion cerrada por ya haber enviado todos los mensajes
        except ConnectionError:
            # YA con todos los mensages recibidos, se ve quien gano
            monitor.register_agency()
            winners = monitor.get_winners(agency)
            logger.info(action, logger.LogResult.success, "winners", winners)

            # Envio ganadores
            protocol.send_winners(client_socket, winners)

            logger.info(action, logger.LogResult.success, "messages-amount", message_amount)
            logger.info(action, logger.LogResult.success, "chunks-amount", chunk_amount)
            client_socket.close() # Ya no van a llegar mas mensajes
            return
        except Exception as e:
            logger.error(
                action, logger.LogResult.fail, "messages-amount", message_amount
            )
            raise e

    def run(self):
        action = "accept-connection"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.server_host, self.server_port))
            server_socket.listen()
            while True:
                try:
                    logger.info(action, logger.LogResult.in_progress)
                    client_socket, _ = server_socket.accept()
                except Exception as e:
                    logger.error(action, logger.LogResult.fail)
                    raise e
                logger.info(action, logger.LogResult.success)

                thread = threading.Thread(target=self._handle_client, args=(client_socket, self.monitor))
                thread.start()
                logger.info("thread running", logger.LogResult.success, "thread-started")
            # Queda colgado el join hasta llegar al ej 8 y poder salir del while
            thread.join()
