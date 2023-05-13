from gamemsg import Data
from game import Game
from player import Player
from card import *


def dict_of_cards():
    cards = []
    values = list(CardRank)
    suits = list(Suit)  # 1-♣ 2-♦ 3-♥ 4-♠
    for value in values:
        for suit in suits:
            card = Card(value, suit)
            cards.append(card)

    dic = {}

    k = 0
    for i in range(2, 15):
        for j in range(1, 4):
            dic[cards] = "i~j"
            k += 1

    return dic


class Protocol:
    def __init__(self, gameMsg):
        """
        example of a message :
        size|game status|round status|your hand(2 cards)|players$
        size : a number
        game status: string
        round status: string
        your hand :  2:card1,card2  (card: 2-14~1-4)
        players : len(players):player1,player2,.. (player: id~status)
        param: gameMsg
        """
        self.game = gameMsg.getGame()
        self.player = gameMsg.getPlayer()
        self.massage = self.create_massage()

    def create_massage(self):
        game_status = self.game.get_status()
        round_status = self.game.get_in_round()
        your_hand = "2:" + self.get_your_hand()
        players = self.get_players()
        mass = game_status + "|" + round_status + "|" + your_hand + "|" + players + "$"
        size = len(mass)
        return str(size) + "|" + mass

    def get_players(self):
        players = self.game.get_players()
        res = f"{len(players)}:"
        for i in range(len(players)):
            player = players[i]
            if i != len(players)-1:
                res += str(player.get_id()) + "~" + str(player.get_respone()) + "," # add get_respone in player
            else:
                res += str(player.get_id()) + "~" + str(player.get_respone())

        return res

    def get_your_hand(self):
        cards = self.player.get_cards()
        dictionary = dict_of_cards()
        card1 = dictionary[cards[0]]
        card2 = dictionary[cards[1]]
        return card1+","+card2




