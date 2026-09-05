import socket
import logger
import protocol
from monitor import Monitor

import threading
import signal

class Server:
    def __init__(self, server_host: str, server_port: int) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.monitor = Monitor()
        # Controla si llega la sigterm para terminar el hilo
        self.status = True # Espero encontrar un mejor nombre antes de la entrega final
        self.server_socket = None # Hasta crearlo en run()

    def _handle_client(self, client_socket, monitor):
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
            self.send_winners(client_socket, monitor, agency)

        # Caso de conexion cerrada por ya haber enviado todos los mensajes
        except ConnectionError:
            self.send_winners(client_socket, monitor, agency)
            return
        except Exception as e:
            logger.error(
                action, logger.LogResult.fail, "messages-amount", message_amount
            )
            raise e

    def send_winners(self, client_socket, monitor, agency):
         # YA con todos los mensages recibidos, se ve quien gano
        monitor.register_agency()
        winners = monitor.get_winners(agency)
        protocol.send_winners(client_socket, winners) # Envio ganadores
        client_socket.close() # Ya no van a llegar mas mensajes

    # Metodo que cierra el socket. Se hace aca porque el server se queda en el accept() y no termina el ciclo
    # Tambien hago el cambio de status para romper el while y liberar recursos
    def handle_signal(self, signum, frame):
        logger.info("SIGTERM-received", logger.LogResult.success, "signal", signum)
        self.status = False
        self.monitor.shutdown()
        self.server_socket.close()

    def run(self):
        action = "accept-connection"
        threads = []

        # Esto permite cambiar el status del server y luego liberar recursos saliendo del ultimo while
        signal.signal(signal.SIGTERM, self.handle_signal)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.server_host, self.server_port))
            server_socket.listen()
            self.server_socket = server_socket # El porque en handle_signal
            while self.status: # Sale solo cuando se recibe la SIGTERM
                try:
                    logger.info(action, logger.LogResult.in_progress)
                    client_socket, _ = server_socket.accept()
                except OSError as e:
                    if not self.status:
                        break # Este es el caso de SIGTERM. Corto el while y libero
                    raise e
                except Exception as e:
                    logger.error(action, logger.LogResult.fail)
                    raise e
                logger.info(action, logger.LogResult.success)

                thread = threading.Thread(target = self._handle_client, args = (client_socket, self.monitor), daemon = True)
                threads.append(thread)
                thread.start()
                logger.info("thread running", logger.LogResult.success, "thread-started")
        # YA habiendo salido del while por el SIGTERM, libero recursos
        for thread in threads:
            thread.join()
