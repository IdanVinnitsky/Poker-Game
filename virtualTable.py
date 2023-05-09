import pickle
import socket
import threading
from player import Player
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
        self.table = Table(1)
        self.deck = Deck()
        self.game = Game(1, self.table, self.deck)
        self.BUFFER_SIZE = 4096


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

            player = Player("name" + str(self.handNum),self.handNum)
            self.game.add_player(player)
            gameMsg = Data(self.game, player)
            cli_sock.send(pickle.dumps(gameMsg))

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

        gameMsg:Data = Data(self.game, None)

        # for key, sock in self.handSocks.items():
        #     sock.send(pickle.dumps(gameMsg))

        for player in self.game.get_players():
            for i in range(2):
                player.get_cards(self.game.deck)
            sock = self.handSocks[str(player.id)]
            sock.send(pickle.dumps(gameMsg))

        # 3 cards; +1; +1
        for i in range(3):
            # for i in range(1, len(self.handSocks)+1): #get playera
            for player in self.game.get_players():
                print("player:" + str(i))
                sock = self.handSocks[str(player.id)]
                gameMsg.setPlayer(player)
                sock.send(pickle.dumps(gameMsg))
                while True:
                    print("Waiting for Response : HAND=" + str(i))
                    data = pickle.loads(sock.recv(self.BUFFER_SIZE))
                    if data.getPlayer().firstBid == True:
                        table.money_in_the_pot += data.getPlayer()
                    print("player.response:" + data.getPlayer().response)
                    if len(data.getPlayer().response) > 0:
                        break

        # Send ALl START Game


        print("END start_game")


if __name__ == '__main__':
    vtab = VTable("Miki", 50)
    vtab.myfunc()
