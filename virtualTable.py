import pickle
import socket
import threading
from typing import List

from EncryptionTool import EncryptionTool
from HandAct import HandAct
from player import Player
from protocol import Protocol
from table import Table
from deck import Deck
from game import Game
from gamemsg import Data
import time


class VTable:


    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.handNum: int = 1
        self.handSocks: dict[str, socket] = {}
        deck = Deck()
        self.game = Game(1, deck)
        self.BUFFER_SIZE = 4096
        self.enc_tool: EncryptionTool = EncryptionTool()


    def myfunc(self):
        print("Hello my name is " + self.name)


        # host = socket.gethostname()
        # port = 5000  # initiate port no above 1024

        host = "0.0.0.0"
        port = 5555

        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            srv_sock.bind((host, port))
            srv_sock.listen()
            print("Waiting for a connection, Server Started")
        except socket.error as e:
            print("ERR~1~ error in connecting/binding")
            print(str(e))

        while True:
            cli_sock, addr = srv_sock.accept()
            cli_sock.setblocking(1)
            self.handSocks[str(self.handNum)] = cli_sock
            print("Send : HAND=" + str(self.handNum))

            player = Player(self.handNum)
            self.game.add_player(player)
            self.game.init_game()
            pr = Protocol()
            message: str = pr.create_message1(player, self.game, 0, 0)

            cli_sock.sendall(pickle.dumps(message))
            data = pickle.loads(cli_sock.recv(self.BUFFER_SIZE))
            cli_sock.sendall(self.enc_tool.public_key_data)


            self.handNum += 1
            if(self.handNum == 3):
                t = threading.Thread(target=self.start_game, args=())
                t.start()





            # # receive data stream. it won't accept data packet greater than 1024 bytes
            # data = conn.recv(1024).decode()
            # if not data:
            #     # if data is not received break
            #     break
            # print("from connected user: " + str(data))
            # data = input(' -> ')
            # conn.send(data.encode())  # send data to the clients

        conn.close()  # close the connection


    def start_game(self):
        print("START start_game")
        self.game.start_game()

        # for key, sock in self.handSocks.items():
        #     sock.send(pickle.dumps(gameMsg))

        for player in self.game.get_players():
            for i in range(2):
                player.set_cards(self.game.get_card(), self.game.get_card())
            sock = self.handSocks[str(player.id)]
            pr = Protocol()
            msg = pr.create_message1(player, self.game, 0, 0)
            sock.send(pickle.dumps(msg))

        # 3 cards; +1; +1
        for roundNum in range(4):
            if roundNum == 0:
                print("Round 1")
                self.game.round_bid = 5
            elif roundNum == 1:
                print("Round 2")
                self.game.round_bid = 0
                self.game.first_flop()
            elif roundNum == 2:
                print("Round 3")
                self.game.add_to_flop()
            elif roundNum == 3:
                print("Round 4")
                self.game.add_to_flop()
            else:
                raise NotImplementedError(f"Range ", roundNum)

            # for i in range(1, len(self.handSocks)+1): #get playera
            index: int = 0
            players: List[Player] = self.game.get_players().copy()
            # for player in players:
            while index < len(players):
                player = players[index]
                index += 1
                print("player:" + str(player.id))
                sock = self.handSocks[str(player.id)]

                pr = Protocol()
                msg = pr.create_message1(player, self.game, roundNum, self.game.round_bid)
                sock.send(pickle.dumps(msg))

                while True:
                    print("Waiting for Response : HAND " + str(str(player.id)))
                    msg = pickle.loads(sock.recv(self.BUFFER_SIZE))
                    pr = Protocol()
                    pr.from_message(msg)

                    if roundNum == 0:
                        self.game.jackpot += pr.your_hand.bid

                    print("player.response:" , pr.your_hand.responseAct)
                    if pr.your_hand.responseAct != None:
                        if pr.your_hand.responseAct == HandAct.RAISE:
                            players = self.game.get_players().copy()
                            players.remove(player)
                            index = 0
                        self.game.add_player(pr.your_hand)
                        break


        # Send ALl START Game


        print("END start_game")


if __name__ == '__main__':
    vtab = VTable("Miki", 50)
    vtab.myfunc()
