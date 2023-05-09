from deck import Deck
from player import Player


class Game:
    def __init__(self, id, table, deck):
        self.id = id
        self.table = table
        self.deck = deck
        self.round = 0
        self.players: dict[str, Player] = {}
        self.players_in_the_round = []
        self.started = False
        self.ended = False
        self.status = ""
        self.in_round = False

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

    def get_num_of_p(self):
        return len(self.players)

    def add_player(self, player: Player):
        self.players[str(player.id)] = player

    def start_game(self):
        self.started = True
        self.deck.shuffle()
