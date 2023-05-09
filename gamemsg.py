from player import Player


class Data:
    def __init__(self, game, player):
        self.game = game
        self.player: Player = player

    def getGame(self):
        return self.game

    def getPlayer(self) -> Player:
        return self.player

    def setGame(self, game):
        self.game = game

    def setPlayer(self, player):
        self.player = player

