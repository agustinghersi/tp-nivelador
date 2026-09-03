from lottery import Lottery, Bet

class Monitor:
    def __init__(self) -> None:
        # La loteria es el recurso compartido en el server por los clientes
        self.lottery = Lottery(storage_path="bets.csv")
    
    # Se encarga de  guardar las apuestas (seccion critica)
    def store_bet(self, bets: list[Bet]) -> None:
        self.lottery.store_bets(bets)

    # Devuelve el listado de apuestas
    def load_bets(self) -> list[Bet]:
        return self.lottery.load_bets()

    # Recupera los ganadores segun la agencia
    def get_winners(self, bets: list[Bet], agency: str) -> list[Bet]:
        winners = []
        for bet in bets:
            if self.lottery.has_won(bet):
                if bet.agency_id == int(agency):
                    winners.append(bet)
        return winners
