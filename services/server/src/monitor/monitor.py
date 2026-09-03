from lottery import Lottery, Bet
import threading
import os

AGENCY_QUORUM_MIN = int(os.environ["AGENCY_QUORUM_MIN"])

class Monitor:
    def __init__(self) -> None:
        # La loteria es el recurso compartido en el server por los clientes
        self.lottery = Lottery(storage_path="bets.csv")
        # Lock que garantiza un unico acceso a la vez a la sección protegida
        self.lock = threading.Lock()
        self.agencys = 0
        self.condition = threading.Condition(self.lock) # Para esperar quorum de ej 7 sin busy wait

    
    # Se encarga de  guardar las apuestas (seccion critica)
    def store_bet(self, bets: list[Bet]) -> None:
        self.lock.acquire()
        try:
            self.lottery.store_bets(bets)
        finally:
            self.lock.release() # Libero siempre


    # Recupera los ganadores segun la agencia
    def get_winners(self, agency: str) -> list[Bet]:
        with self.condition:
            while self.agencys < AGENCY_QUORUM_MIN:
                self.condition.wait()
            # Cuando se cumple la condicion se hace el load. Con with no necesito hacer realese
            bets = self.lottery.load_bets()

        # Esta parte no es critica, no necesito mantener el lock
        # Todos los ganadores de esta agencia ya estan en el listado
        winners = []
        for bet in bets:
            if self.lottery.has_won(bet):
                if bet.agency_id == int(agency):
                    winners.append(bet)
        return winners

    # Por cada hilo (agencia) nuevo, se agrega uno al contador
    def register_agency(self) -> None:
        self.lock.acquire()
        try:
            self.agencys += 1
            if self.agencys >= AGENCY_QUORUM_MIN:
                self.condition.notify_all() # Por no tener esto no se despertaban los primeros hilos
        finally:
            self.lock.release()
            