from card import *
import random


class Deck():
    def __init__(self):
        self.cards = []
        self.flop = []
        values = list(CardRank)
        suits = list(Suit)   # ♠ ♣ ♥ ♦
        for value in values:
            for suit in suits:
                card = Card(value, suit)
                self.cards.append(card)
        self.shuffle()

    def set_flop(self, flop):
        self.flop = flop


    def get_cards(self):
        return self.cards

    def get_flop(self):
        return self.flop

    def shuffle(self):
        random.shuffle(self.cards)

    def get_card(self):
        card = self.cards.pop()
        return card

    def add_to_flop(self):
        card = self.get_card()
        self.flop.append(card)

    def first_flop(self):
        for i in range(3):
            card = self.get_card()
            self.flop.append(card)


