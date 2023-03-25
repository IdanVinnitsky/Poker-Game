from deck import Deck


class Player:
    def __init__(self, name):
        self.mane = name
        self.money = 0
        #self.title = title
        self.cards = None
        self.playing = False

    def get_cards(self, deck):
        card1 = deck.get_card()
        card2 = deck.get_card()
        self.cards = (card1, card2)

    def add_money(self, money):
        self.money += money

    def set_money(self, money):
        self.money = money

    def get_money(self):
        return self.money

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title
