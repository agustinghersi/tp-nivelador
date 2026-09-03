from lottery import Lottery, Bet
import threading

class Monitor:
    def __init__(self) -> None:
        # La loteria es el recurso compartido en el server por los clientes
        self.lottery = Lottery(storage_path="bets.csv")
        # Lock que garantiza un unico acceso a la vez a la sección protegida
        self.lock = threading.Lock()
    
    # Se encarga de  guardar las apuestas (seccion critica)
    def store_bet(self, bets: list[Bet]) -> None:
        self.lock.acquire()
        try:
            self.lottery.store_bets(bets)
        finally:
            self.lock.release() # Libero siempre


    # Recupera los ganadores segun la agencia
    def get_winners(self, agency: str) -> list[Bet]:
        self.lock.acquire()
        try:
            bets = self.lottery.load_bets()
        finally:
            self.lock.release()
            
        # Esta parte no es critica, no necesito mantener el lock
        # Todos los ganadores de esta agencia ya estan en el listado
        winners = []
        for bet in bets:
            if self.lottery.has_won(bet):
                if bet.agency_id == int(agency):
                    winners.append(bet)
        return winners
