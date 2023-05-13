from HandAct import HandAct
from deck import Deck


class Player:
    def __init__(self, id):
        self.name = None
        self.money = 6942
        self.is_turn = False
        #self.title = title
        self.cards = None
        self.playing = False
        self.id: str = id
        self.password = 'NONE'
        self.responseAct: HandAct = HandAct.NO_DEF
        self.firstBid = True
        self.bid = 0

    def get_is_turn(self):
        return self.is_turn

    def set_is_turn(self, bool):
        self.is_turn = bool

    def get_cards(self):
        return self.cards

    def set_cards(self, card1, card2):
        self.cards = (card1, card2)

    def generate_cards(self, deck):
        card1 = deck.get_card()
        card2 = deck.get_card()
        self.cards = (card1, card2)

    def add_money(self, money):
        self.money += money

    def sub_money(self, money):
        self.money -= money

    def set_money(self, money):
        self.money = money

    def get_money(self):
        return self.money

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
