from typing import List

from GameStatus import GameStatus
from HandAct import HandAct
from ProtocolAct import ProtocolAct
from deck import Deck
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
            dic[cards] = str(i) + "~" + str(j)
            k += 1
    return dic


class GameProtocol:
    def __init__(self):
        """
        example of a message :
        size|protocol type|game status|round status|round num|round_bid|jackpot|your hand(2 cards)|players|flop$
        size : a number
        protocol action: GAME, LOGIN, UPDATE_SCREEN
        game status: string
        round status: string
        your hand :  id, hand action, bid, card1 value, card1 suit, card2 value, card2 suit  (card: 2-14~1-4)
        players : player1;player2;.. (player: id, name, status,card1 value, card1, card2 value, card2 ;)
        flop: card1 value, card1 suit;card2 value, card2 suit;...card5 value, card5 suit
        param:
        """
        self.size: int = 0
        self.protocolAct: ProtocolAct = ProtocolAct.NO_DEF
        self.game_status: GameStatus = GameStatus.NO_DEF
        self.round_status: HandAct = HandAct.NO_DEF
        self.round_num: int = 0
        self.round_bid: int = 0
        self.jackpot: int = 0
        self.your_hand: Player
        self.players: List[Player] = []
        self.flop: List[Card] = []
        self.message = ''

    def get_round_status(self):
        return self.round_status

    def get_players(self):
        return self.players

    def get_num_players(self):
        return len(self.players)

    def create_message1(self, protocolAct, player, game, roundNum, roundBid):
        self.protocolAct = protocolAct
        self.game_status = game.get_status()
        self.round_status = game.round_status
        your_hand: str = self.get_your_hand_str(player)
        players: str = self.get_players_str(game)
        flop:  str = self.get_flop_str(game)
        mass = str(self.protocolAct.value) + "|" + "|" + str(self.game_status.value) + "|" + str(self.round_status.value) + \
               "|" + str(roundNum) + "|" + \
               str(roundBid) + "|" + str(game.jackpot) + "|" + your_hand + "|" + players + "|" + flop
        size = len(mass)
        return str(size) + "|" + mass + "$"

    def create_message(self, protocolAct, player: Player):
        self.protocolAct = protocolAct
        your_hand = self.get_your_hand_str(player)
        msg = str(self.protocolAct.value) + "|" + "|" + str(self.game_status.value) + "|" + str(self.round_status.value) + \
              "|0|0|0|" + your_hand
        size = len(msg)
        return str(size) + "|" + msg + "$"

    def create_message3(self, protocolAct, player: Player, message: str):
        self.protocolAct = protocolAct
        your_hand = self.get_your_hand_str(player)
        msg = str(self.protocolAct.value) + "|" + message + "|" + str(self.game_status.value) + "|" + str(
            self.round_status.value) + \
              "|0|0|0|" + your_hand
        size = len(msg)
        return str(size) + "|" + msg + "$"

    def create_message2(self, protocolAct, game_status: GameStatus,  player: Player):
        self.protocolAct = protocolAct
        your_hand = self.get_your_hand_str(player)
        msg = str(self.protocolAct.value) + "|" + "|" + str(game_status.value) + "|" + str(self.round_status.value) + \
              "|0|0|0|" + your_hand
        size = len(msg)
        return str(size) + "|" + msg + "$"


    def get_players_str(self, game: Game):
        players = game.get_players()
        res = ''
        for pl in players:
            res += str(pl.id) + "," + str(pl.name) +  "," + str(pl.password) + "," + str(pl.responseAct.value) + "," + str(pl.bid)
            cards = pl.get_cards()
            if cards == None:
                res += "," + "," + "," + "," + ",;"
            else:
                res += "," + str(cards[0].getValue().value) + "," + str(cards[0].getSuit().value) + "," + str(
                    cards[1].getValue().value) + "," + str(cards[0].getSuit().value)
                res += ";"
        res = res[:-1]

        return res

    def get_your_hand_str(self, player):
        cards = player.get_cards()
        if cards == None:
            return str(player.id) + "," + str(player.name)  + "," + str(player.password) + "," + str(player.responseAct.value) + "," + str(player.bid) + "," + "," + \
                 "," + "," + ","
        # dictionary = dict_of_cards()
        # card1 = dictionary[cards[0]]
        # card2 = dictionary[cards[1]]
        return str(player.id) + "," + str(player.name) + "," + str(player.password) + "," + str(player.responseAct.value) + "," + str(player.bid) + "," + \
            str(cards[0].getValue().value) + "," + str(cards[0].getSuit().value) + "," + str(cards[1].getValue().value) + \
            "," + str(cards[1].getSuit().value)

    def get_flop_str(self, game):
        cards = game.flop
        if cards == None or len(cards) == 0:
            return ''
        res = ''
        for card in cards:
            res += str(card.getValue().value) + "," + str(card.getSuit().value) + ";"
        res = res[:-1]
        return res

    def parse_player(self, data: str):
        if len(data) == 0:
            return None
        parts = data.split(',')
        player = Player(parts[0])
        player.name = parts[1]
        player.password = parts[2]
        player.responseAct = HandAct(parts[3])
        player.bid = int(parts[4])
        if len(parts[5]) > 0:
            card1: Card = Card(CardRank(int(parts[5])), Suit(parts[6]))
            card2: Card = Card(CardRank(int(parts[7])), Suit(parts[8]))
            player.set_cards(card1, card2)
        return player

    def parse_flop(self, data: str):
        if len(data) == 0:
            return None
        self.flop.clear()
        cards = data.split(';')
        for card in cards:
            part_card = card.split(',')
            self.flop.append(Card(CardRank(int(part_card[0])), Suit(part_card[1])))

    def parse_players(self, msg: str):
        if len(msg) < 2:
            return
        parts = msg.split(';')
        self.players.clear()
        for p in parts:
            self.players.append(self.parse_player(p))
            # ws = p.split(',')
            # player = Player(int(ws[0]))
            # player.name = str(ws[2])
            # player.responseAct = HandAct(ws[2])
            # player.bid = int(parts[3])
            # if len(parts[4]) > 0:
            #     card1: Card = Card(CardRank(int(parts[4])), Suit(parts[5]))
            #     card2: Card = Card(CardRank(int(parts[6])), Suit(parts[7]))
            #     player.set_cards(card1, card2)


    def from_message(self, msg: str):
        msg = msg[:-1]
        parts = msg.split('|')
        self.size = int(parts[0])
        self.protocolAct = ProtocolAct(parts[1])
        self.message = parts[2]
        self.game_status = GameStatus(parts[3])
        self.round_status = HandAct(parts[4])
        self.round_num = int(parts[5])
        self.round_bid = int(parts[6])
        self.jackpot = int(parts[7])
        self.your_hand = self.parse_player(parts[8])
        if len(parts) == 9:
            return
        self.parse_players(parts[9])
        self.parse_flop(parts[10])
        # print("parts :", parts[5])




        # self.round_status = self.game.round_status
        # your_hand = "2:" + self.get_your_hand(player)
        # players = self.get_players()
        # mass = str(game_status.value) + "|" + str(round_status.value) + "|" + your_hand + "|" + players + "$"
        # size = len(mass)
        # return str(size) + "|" + mass


if __name__ == '__main__':
    deck = Deck()
    game = Game(11, deck)
    player = Player(1)
    player.generate_cards(deck)
    print("cards:", player.get_cards())

    p = GameProtocol()
    msg = p.create_message1(player,game)
    print("Message1:", msg)

    p.from_message(msg)
    print("Message2:", p.your_hand.get_cards())
    print("Message2:", p.your_hand.responseAct)
