from lottery import Lottery, Bet

class Monitor:
    def __init__(self) -> None:
        # La loteria es el recurso compartido en el server por los clientes
        self.lottery = Lottery(storage_path="bets.csv")
    
    def store_bet(self, bets: list[Bet]) -> None:
        self.lottery.store_bets(bets)

    def load_bets(self) -> list[Bet]:
        return self.lottery.load_bets()

