import pickle
import socket
import threading
from _thread import start_new_thread
from typing import List

from AccountsRepository import AccountsRepository
from EncryptionTool import EncryptionTool
from HandAct import HandAct
from ProtocolAct import ProtocolAct
from hands import Hand
from player import Player
from gameprotocol import GameProtocol
from table import Table
from deck import Deck
from game import Game
from gamemsg import Data
import time



class VTable:

    def __init__(self, name, age):
        self.lock = threading.Lock()
        self.hand_answers: dict[str, Player] = {}
        self.curr_hand = 0
        self.in_game_protocol = None
        self.name = name
        self.age = age
        self.handNum: int = 1
        self.handSocks: dict[str, socket] = {}
        self.deck = Deck()
        self.game = Game(1, self.deck)
        self.BUFFER_SIZE = 4096
        self.enc_tool: EncryptionTool = EncryptionTool()
        self.accountsRep = AccountsRepository()
        self.request_players = []


    def start_server(self):
        print("Hello my name is " + self.name)

        self.accountsRep.create_table()
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
            # cli_sock.setblocking(1)
            self.handSocks[str(self.handNum)] = cli_sock
            print("Send : HAND=" + str(self.handNum))
            cli_sock.send(self.enc_tool.public_key_data)
            start_new_thread(self.client_handler, (self.handNum, cli_sock))
            self.handNum += 1

        srv_sock.close()  # close the connection


    def client_handler(self, handNum, connection):
        connection.send(str.encode('You are now connected to the replay server... Type BYE to stop'))
        while True:
            data = connection.recv(self.BUFFER_SIZE)
            msg = self.enc_tool.decrypt_rsa(data)
            print("Receive from ", handNum)
            print("Received data ", msg)
            pr = GameProtocol()
            pr.from_message(msg)
            if pr.protocolAct == ProtocolAct.LOGIN:
                start_new_thread(self.client_login, (handNum, pr, connection))
            elif pr.protocolAct == ProtocolAct.SIGNUP:
                start_new_thread(self.client_signup, (handNum, pr, connection))
            elif pr.protocolAct == ProtocolAct.REQUEST_START:
                start_new_thread(self.client_request_game, (handNum, pr))
            elif pr.protocolAct == ProtocolAct.APPEND:
                start_new_thread(self.client_append_game, (handNum, pr))
            elif pr.protocolAct == ProtocolAct.GAME:
                # if self.curr_hand == handNum:
                start_new_thread(self.update_running_game, (handNum, pr))
            else:
                print("Error request:", pr.protocolAct)
            # msconnection.sendall(str.encode(reply)):

        connection.close()

    def send_update_screen(self):
        for numHand, player in self.game.players.items():
            sock = self.handSocks[str(numHand)]
            pr = GameProtocol()
            msg = pr.create_message1(ProtocolAct.UPDATE_SCREEN, player, self.game, 0, 0)
            sock.sendall(pickle.dumps(msg))


    def running_game(self):
        print("Start running_game")
        self.game.start_game()
        #
        # for numHand, player in self.game.players.items():
        #     player.set_cards(self.game.get_card(), self.game.get_card())
        #     sock = self.handSocks[str(numHand)]
        #     pr = GameProtocol()
        #     msg = pr.create_message1(ProtocolAct.UPDATE_SCREEN, player, self.game, 0, 0)
        #     sock.send(pickle.dumps(msg))
        # self.send_update_screen()
        self.hand_answers.clear()
        for numHand, player in self.game.players.items():
            player.set_cards(self.game.get_card(), self.game.get_card())
        # 3 cards; +1; +1
        for roundNum in range(1, 5):
            print(">>>>>>>>>>>>>>>>>>>>> ", )
            print("Round ", roundNum)
            self.hand_answers.clear()
            self.game.round = roundNum
            self.game.round_status = HandAct.NO_DEF
            if roundNum == 1:
                self.game.round_bid = 5
            elif roundNum == 2:
                self.game.round_bid = 0
                self.game.first_flop()
            elif roundNum == 3:
                self.game.round_bid = 0
                self.game.add_to_flop()
            elif roundNum == 4:
                self.game.round_bid = 0
                self.game.add_to_flop()
            else:
                raise NotImplementedError(f"Range ", roundNum)

            # for i in range(1, len(self.handSocks)+1): #get playera
            index: int = 0
            players: List[Player] = self.game.get_players().copy()
            # for player in players:
            while index < len(players):
                self.send_update_screen()
                player = players[index]
                index += 1

                print("Money on table :", self.game.jackpot)
                print("Cards on table :", self.game.flop)

                sock = self.handSocks[str(player.id)]
                self.hand_answers.clear()
                self.curr_hand = int(player.id)
                pr = GameProtocol()
                msg = pr.create_message1(ProtocolAct.GAME, player, self.game, roundNum, self.game.round_bid)
                print("player:" + str(player.id) + " send " + msg)
                sock.send(pickle.dumps(msg))
                self.hand_answers.clear()
                # while True:
                # print("Waiting for Response : HAND " + str(str(player.id)))
                # data = pickle.loads(sock.recv(self.BUFFER_SIZE))
                # data = sock.recv(self.BUFFER_SIZE)
                # msg = self.enc_tool.decrypt(data)
                # pr = GameProtocol()
                # pr.from_message(msg)
                # with self.lock:
                # time.sleep(3)
                received_player: Player = None
                while True:
                    # print("Waiting for client response....")
                    # time.sleep(5)
                    received_player = self.hand_answers.get(str(player.id))
                    if received_player is not None:
                        break
                print("Receive client response.")
                self.game.players[str(player.id)].responseAct = received_player.responseAct
                self.game.players[str(player.id)].bid = received_player.bid
                self.curr_hand = -1
                if roundNum == 1:
                    self.game.jackpot += received_player.bid

                print("player.response:", received_player.responseAct)
                # if received_player.responseAct != None:

                if received_player.responseAct == HandAct.RAISE or received_player.responseAct == HandAct.BET:
                    self.game.jackpot += received_player.bid
                    self.game.round_status = received_player.responseAct
                    self.game.round_bid = received_player.bid
                    players = self.game.get_players().copy()
                    players.remove(player)
                    self.hand_answers.clear()
                    index = 0

                if received_player.responseAct == HandAct.CALL:
                    self.game.jackpot += self.in_game_protocol.your_hand.bid

                self.game.add_player(received_player)


        self.game.find_winner()
        winner = self.game.get_winner()
        winner.add_money(self.game.jackpot)

        for numHand, player in self.game.players.items():
            player.set_cards(self.game.get_card(), self.game.get_card())
            sock = self.handSocks[str(numHand)]
            pr = GameProtocol()
            msg = pr.create_message1(ProtocolAct.WINNER, winner, self.game, 5, 0)
            sock.send(pickle.dumps(msg))

        print(f"the winner issss: {winner}")

        self.request_players.clear()
        print("End running_game")

    def client_append_game(self, handNum, pr: GameProtocol):
        self.request_players.append(handNum)
        pr.your_hand.id = handNum
        self.game.players[str(handNum)] = pr.your_hand
        if len(self.request_players) == 2:
            start_new_thread(self.running_game, ())

    def client_request_game(self, handNum, pr: GameProtocol):
        self.request_players.append(handNum)
        pr.your_hand.id = handNum
        self.game.players[str(handNum)] = pr.your_hand
        if len(self.request_players) == 2:
            start_new_thread(self.running_game, ())

    def update_running_game(self, handNum, pr: GameProtocol):
        print("update_running_game")
        self.in_game_protocol = pr
        self.hand_answers[str(handNum)] = pr.your_hand
        # self.lock.release()

    def client_login(self, handNum, pr: GameProtocol, connection):
        print("client_login")
        # self.client_signup(handNum, pr)
        playerId = self.accountsRep.login(pr.your_hand)
        if playerId == -1:
            pr1 = GameProtocol()
            message: str = pr1.create_message3(ProtocolAct.MESSAGE, pr.your_hand, "ERROR : Player doesn't exist")
            connection.send(pickle.dumps(message))
        else:
            pr1 = GameProtocol()
            message: str = pr1.create_message3(ProtocolAct.MESSAGE, pr.your_hand, "INFO : Player exists")
            connection.send(pickle.dumps(message))

            pr.your_hand.id = handNum
            self.game.players[str(handNum)] = pr.your_hand
            print(" Set playerId:", playerId)

    def client_signup(self, handNum, pr: GameProtocol, connection):
        is_signup, msg = self.accountsRep.signup(pr.your_hand)

        pr1 = GameProtocol()
        message: str = pr1.create_message3(ProtocolAct.MESSAGE, pr.your_hand, msg)
        connection.send(pickle.dumps(message))

    def myfunc1(self):
        print("Hello my name is " + self.name)

        # host = socket.gethostname()
        # port = 5000  # initiate port no above 1024

        host = "0.0.0.0"
        port = 5555

        self.accountsRep.create_table()
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
            pr = GameProtocol()
            message: str = pr.create_message1(ProtocolAct.GAME, player, self.game, 0, 0)

            cli_sock.sendall(pickle.dumps(message))
            data = pickle.loads(cli_sock.recv(self.BUFFER_SIZE))
            cli_sock.sendall(self.enc_tool.public_key_data)

            self.handNum += 1

            if self.handNum == 3:
                t = threading.Thread(target=self.start_game, args=())
                t.start()

        conn.close()  # close the connection


    def start_game(self):
        print("START start_game")
        self.game.start_game()

        # for key, sock in self.handSocks.items():
        #     sock.send(pickle.dumps(gameMsg))

        # for player in self.game.get_players():
        #     for i in range(2):
        #         player.set_cards(self.game.get_card(), self.game.get_card())
        #     sock = self.handSocks[str(player.id)]
        #     pr = GameProtocol()
        #     msg = pr.create_message1(ProtocolAct.GAME, player, self.game, 0, 0)
        #     sock.send(pickle.dumps(msg))

        # 3 cards; +1; +1
        for roundNum in range(1, 5):
            print(">>>>>>>>>>>>>>>>>>>>> ", )
            print("Round ", roundNum)
            self.game.round = roundNum
            if roundNum == 1:
                self.game.round_bid = 5
            elif roundNum == 2:
                self.game.round_bid = 0
                self.game.first_flop()
            elif roundNum == 3:
                self.game.add_to_flop()
            elif roundNum == 4:
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
                print("Money on table :", self.game.jackpot)
                print("Cards on table :", self.game.flop)

                sock = self.handSocks[str(player.id)]

                pr = GameProtocol()
                msg = pr.create_message1(ProtocolAct.GAME, player, self.game, roundNum, self.game.round_bid)
                sock.send(pickle.dumps(msg))

                while True:
                    print("Waiting for Response : HAND " + str(str(player.id)))
                    # data = pickle.loads(sock.recv(self.BUFFER_SIZE))
                    data = sock.recv(self.BUFFER_SIZE)
                    msg = self.enc_tool.decrypt(data)
                    pr = GameProtocol()
                    pr.from_message(msg)

                    if roundNum == 1:
                        self.game.jackpot += pr.your_hand.bid

                    print("player.response:", pr.your_hand.responseAct)
                    if pr.your_hand.responseAct != None:
                        current_player = self.game.get_player(pr.your_hand.id)
                        current_player.responseAct = pr.your_hand.responseAct

                        if pr.your_hand.responseAct == HandAct.RAISE:
                            self.game.jackpot += pr.your_hand.bid
                            self.game.round_status = HandAct.RAISE
                            self.game.round_bid = pr.your_hand.bid
                            players = self.game.get_players().copy()
                            players.remove(player)
                            index = 0

                        if pr.your_hand.responseAct == HandAct.CALL:
                            self.game.jackpot += pr.your_hand.bid

                        if pr.your_hand.responseAct == HandAct.BET:
                            self.game.jackpot += pr.your_hand.bid
                            self.game.round_status = HandAct.BET
                            self.game.round_bid = self.game.min_bid

                        self.game.add_player(pr.your_hand)

                        break

        # Send ALl START Game
        if roundNum == 4:
            print(f"the winner issss: {self.the_winner()}")

        print("END start_game")


if __name__ == '__main__':
    vtab = VTable("Miki", 50)
    vtab.start_server()
