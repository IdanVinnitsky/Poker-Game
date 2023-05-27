from GameStatus import GameStatus
from HandAct import HandAct
from deck import Deck
from player import Player


class Game:
    def __init__(self, id, deck):
        self.id = id
        self.deck = deck
        self.round = 0
        self.round_bid = 0
        self.min_bid = 5
        self.players: dict[str, Player] = {}
        self.players_in_the_round = []
        self.started = False
        self.ended = False
        self.status: GameStatus = GameStatus.NO_DEF
        self.in_round = False
        self.round_status: HandAct = HandAct.NO_DEF
        self.flop = []
        self.jackpot = 0

    def get_round(self):
        return self.round

    def set_table(self, table):
        self.table = table

    def set_deck(self, deck: Deck):
        self.deck = deck


    def get_table(self):
        return self.table

    def update_players(self):
        for player in self.players:
            if player not in self.players_in_the_round:
                self.players_in_the_round.append(player)

    def get_players_in_the_round(self):
        return self.players_in_the_round

    def get_in_round(self):
        return self.in_round

    def start_the_round(self):
        self.in_round = True

    def end_the_round(self):
        self.in_round = False

    def get_deck(self):
        return self.deck

    def update_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_id(self):
        return self.id

    def get_players(self):
        return list(self.players.values())

    def get_player(self, id: int):
        return self.players[str(id)]

    def get_num_of_p(self):
        return len(self.players)

    def add_player(self, player: Player):
        self.players[str(player.id)] = player

    def start_game(self):
        self.status = GameStatus.STARTED
        self.deck.shuffle()

    def init_game(self):
        self.status = GameStatus.INIT

    def set_flop(self, flop):
        self.flop = flop

    def get_flop(self):
        return self.flop

    def add_to_flop(self):
        card = self.get_card()
        self.flop.append(card)

    def first_flop(self):
        for i in range(3):
            card = self.get_card()
            self.flop.append(card)

    def get_card(self):
        card = self.deck.get_card()
        return card