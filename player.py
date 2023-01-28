
class Player:
    def __init__(self, name, title):
        self.mane = name
        self.money = 0
        self.title = title

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
