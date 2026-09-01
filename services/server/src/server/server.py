import socket
import logger
import safe_socket
import protocol
from lottery import Lottery, Bet

class Server:
    def __init__(self, server_host: str, server_port: int) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.lottery = Lottery(storage_path="bets.csv")

    def _handle_client(self, client_socket):
        action = "handle-client"
        message_amount = 0
        try:
            logger.info(action, logger.LogResult.in_progress)
            while True:
                message_size = protocol.recv_size(client_socket)
                client_message = safe_socket.recv_all(
                    client_socket, message_size
                )
                if not client_message:
                    logger.info(
                        action,
                        logger.LogResult.success,
                        "messages-amount",
                        message_amount,
                    )
                    return
                message_amount += 1
                safe_socket.send_all(client_socket, client_message)
                bets = protocol.create_bet(client_message)
                self.lottery.store_bets(bets)

        # Caso de conexion cerrada por ya haber enviado todos los mensajes
        except ConnectionError:
            # YA con todos los mensages recibidos, se ve quien gano
            loaded_bets = self.lottery.load_bets()
            winners = self.get_winners(loaded_bets)
            logger.info(action, logger.LogResult.success, "winners", winners)

            logger.info(action, logger.LogResult.success, "messages-amount", message_amount)
            client_socket.close() # Ya no van a llegar mas mensajes
            return
        except Exception as e:
            logger.error(
                action, logger.LogResult.fail, "messages-amount", message_amount
            )
            raise e

    def get_winners(self, bets: list[Bet]) -> list[Bet]:
        winners = []
        for bet in bets:
            if self.lottery.has_won(bet):
                winners.append(bet)
        return winners

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

                self._handle_client(client_socket)
