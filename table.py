
class Table:
    def __init__(self, id, *args):
        self.id = id
        self.players = list(args)
        self.num_of_players = 0
        self.num_of_rounds = 0
        self.money_on_table = 0
        self.avg_money_in_round = 0
        self.avg_player_money = 0

    def get_id(self):
        return self.id

    def add_player(self, player):
        self.players.append(player)

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

    def get_money_on_table(self):
        return self.money_on_table

    def set_money_on_table(self, money):
        self.money_on_table = money

    def add_money_on_table(self, money):
        self.money_on_table += money

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



