from card import *
import random


class Deck():
    def __init__(self):
        self.cards = []
        values = list(CardRank)
        suits = list(Suit)   # ♠ ♣ ♥ ♦
        for value in values:
            for suit in suits:
                card = Card(value, suit)
                self.cards.append(card)
        self.shuffle()


    def get_cards(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def get_card(self):
        card = self.cards.pop()
        return card



