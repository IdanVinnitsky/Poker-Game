from GameStatus import GameStatus
from HandAct import HandAct
from deck import Deck
from hands import Hand
from player import Player


def determine_winner(player1_hand, player2_hand):
    if player1_hand == player2_hand:
        return player1_hand
    elif player1_hand is None:
        return player2_hand
    elif player2_hand is None:
        return player1_hand
    else:
        player1_rank = player1_hand[0]  # HandRank of player 1
        player1_cards = player1_hand[1]  # Cards of player 1
        player2_rank = player2_hand[0]  # HandRank of player 2
        player2_cards = player2_hand[1]  # Cards of player 2

        # Compare the hand ranks
        if player1_rank.value > player2_rank.value:
            return player1_hand
        elif player1_rank.value < player2_rank.value:
            return player2_hand
        else:
            # Hand ranks are the same, compare the cards
            for i in range(len(player1_cards)):
                if player1_cards[i].getValue().value > player2_cards[i].getValue().value:
                    return player1_hand
                elif player1_cards[i].getValue().value < player2_cards[i].getValue().value:
                    return player2_hand

    # If no winner is determined, it's a tie
    #return "It's a tie!"


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
        self.winner = None

    def get_winner(self):
        return self.winner


    def find_winner(self):
        dict_hands = {}
        flop = self.flop
        for key, pl in self.players.items():
            dict_hands[key] = Hand(flop + list(pl.get_cards()))
        dict_ranks = {}
        for key, hand in dict_hands.items():
            dict_ranks[key] = hand.get_hand_rank()

        highest_key = None
        highest_value = None
        for key, value in dict_ranks.items():
            if highest_value is None or determine_winner(value, highest_value) == value:
                highest_key = key
                highest_value = value

        self.winner = self.players[highest_key]

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



if __name__ == '__main__':
    deck = Deck()
    game1 = Game(1, deck)
    player1 = Player(1)
    game1.add_player(player1)
    player2 = Player(2)
    game1.add_player(player2)
    player1.generate_cards(game1.get_deck())
    player2.generate_cards(game1.get_deck())
    game1.first_flop()

    game1.add_to_flop()
    game1.add_to_flop()

    game1.the_winner()

    print(f"the winner is {game1.winner()}")

