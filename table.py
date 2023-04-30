
class Table:
    def __init__(self, id):
        self.id = id
        self.num_of_players = 0
        self.num_of_rounds = 0
        self.money_in_the_pot = False
        self.jackpot = 0  # money_on_table
        self.money_to_call = 0

        self.avg_money_in_round = 0
        self.avg_player_money = 0

    def get_money_in_the_pot(self):
        return self.money_in_the_pot

    def update_money_in_the_pot(self):
        self.money_in_the_pot = True

    def new_round(self):
        self.money_in_the_pot = False
        self.money_to_call = 0

    def set_money_to_call(self, money):
        self.money_to_call = money

    def get_money_to_call(self):
        return self.money_to_call

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_num_of_players(self):
        return self.num_of_players

    def set_num_of_players(self, num):
        self.num_of_players = num

    def add_num_of_players(self, num):
        self.num_of_players += num

    def set_num_of_rounds(self, num):
        self.num_of_rounds = num

    def get_num_of_rounds(self):
        return self.num_of_rounds

    def add_num_of_rounds(self, num):
        self.num_of_rounds += num

    def get_jackpot(self):
        return self.jackpot

    def set_jackpot(self, money):
        self.jackpot = money

    def add_to_jackpot(self, money):
        self.jackpot += money

    def get_avg_money_in_round(self):
        return self.avg_money_in_round

    def set_avg_money_in_round(self, money):
        self.avg_money_in_round = money

    def add_avg_money_in_round(self, money):
        self.avg_money_in_round += money

    def get_avg_player_money(self):
        return self.avg_money_in_round

    def set_avg_player_money(self, avg):
         self.avg_money_in_round = avg

    def add_avg_player_money(self, avg):
        self.avg_money_in_round += avg


