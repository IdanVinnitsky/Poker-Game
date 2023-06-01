import pickle
import socket
import threading

import rsa

from GameStatus import GameStatus
from HandAct import HandAct
from ProtocolAct import ProtocolAct
from player import Player
from gameprotocol import GameProtocol
from table import Table
from deck import Deck
from game import Game
from gamemsg import Data


class VHand:

    def __init__(self, ip):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.BUFFER_SIZE = 4096
        self.player = None
        self.server_public_key = None
        self.default_bit = 0
        self.screen = None
        self.flop = None
        self.otherHands = None
        self.playerAct: HandAct = HandAct.NO_DEF
        self.in_game_protocol: GameProtocol = GameProtocol()

    def connect(self):
        try:
            self.client_sock.connect(self.addr)
        except Exception as e:
            print(e)

    def send1(self, data):
        try:
            self.client_sock.send(pickle.dumps(data))
        except socket.error as e:
            print(str(e))

    def send(self, data):
        print("Sending ", data)
        if self.server_public_key == None:
            self.send1(data)
        else:
            try:
                obj_bytes = pickle.dumps(data)
                encrypted_data = rsa.encrypt(obj_bytes, self.server_public_key)
                self.client_sock.send(encrypted_data)
            except socket.error as e:
                print(str(e))

    def init_hand_game(self):
        self.conncting()

        pass

    def conncting(self):
        try:
            self.client_sock.connect(self.addr)

            # gameMsg = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            message: str = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = GameProtocol()
            pr.from_message(message)
            self.player = pr.your_hand

            if pr.game_status == GameStatus.INIT:
                send_msg = pr.create_message(ProtocolAct.GAME, self.player)
                self.send(send_msg)
                server_public_key_data = self.client_sock.recv(1024)
                self.server_public_key = rsa.PublicKey.load_pkcs1(server_public_key_data)
                print("key:", self.server_public_key)

            print("Receive player:" + str(self.player.id))
            self.player.password = 'CLIENT' + str(self.player.id)
            print("Waiting for starting game" + str(self.player.id))
            message = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = GameProtocol()
            pr.from_message(message)
            print("Game started" + str(pr.game_status))

        except Exception as e:
            print(e)

    def initUIHand1(self, sc):
        try:
            self.screen = sc
            self.client_sock.connect(self.addr)
        except Exception as e:
            print(e)

        t = threading.Thread(target=self.running_game, args=())
        t.start()

    def initUIHand(self, sc):
        try:
            self.screen = sc
            self.client_sock.connect(self.addr)

            server_public_key_data = self.client_sock.recv(1024)
            self.server_public_key = rsa.PublicKey.load_pkcs1(server_public_key_data)
            print("key:", self.server_public_key)

        except Exception as e:
            print(e)

    def append_game(self):
        try:
            self.flop = None
            self.otherHands = None
            pr = GameProtocol()
            msg = pr.create_message2(ProtocolAct.APPEND_GAME, GameStatus.REQUEST_START, self.player)
            self.send(msg)

            t = threading.Thread(target=self.running_game, args=())
            t.start()
        except Exception as e:
            print(e)

    def start_game(self):
        pr = GameProtocol()
        msg = pr.create_message2(ProtocolAct.REQUEST_START, GameStatus.REQUEST_START, self.player)
        self.send(msg)

        self.flop =None
        self.otherHands = None
        self.playerAct: HandAct = HandAct.NO_DEF
        self.in_game_protocol: GameProtocol = GameProtocol()

    def running_game(self):
        try:
            while True:
                try:
                    print("Waitning for data:")
                    message: str = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
                    self.in_game_protocol.from_message(message)

                    print("Receive data:", message)
                    if self.in_game_protocol.protocolAct == ProtocolAct.MESSAGE:
                        self.in_game_protocol.message.startswith("ERROR:")

                    if self.in_game_protocol.protocolAct == ProtocolAct.GAME:
                        if self.in_game_protocol.game_status == GameStatus.STARTED:
                            self.player = self.in_game_protocol.your_hand
                            self.otherHands = [x for x in self.in_game_protocol.players if x != self.player]
                            print(f"others : {self.otherHands}")
                            self.flop = self.in_game_protocol.flop
                            self.screen.disable_menu_buttons()
                            self.screen.update_screen(False)

                    if self.in_game_protocol.protocolAct == ProtocolAct.UPDATE_SCREEN:
                        self.player = self.in_game_protocol.your_hand
                        self.otherHands = [x for x in self.in_game_protocol.players if x != self.player]
                        self.flop = self.in_game_protocol.flop
                        self.screen.update_screen(True)

                    if self.in_game_protocol.protocolAct == ProtocolAct.WINNER:
                        winner = self.in_game_protocol.your_hand
                        if self.player.name == winner.name:
                            self.player.money = winner.money
                        self.screen.update_winner_screen(winner)
                        self.screen.enable_menu_buttons()

                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)

    def temp_send_player_response(self, act: HandAct, val: str):
        print("Player Action", act)
        player = self.in_game_protocol.your_hand

        player.responseAct = act
        if self.in_game_protocol.round_num == 1:
            player.bid = self.in_game_protocol.round_bid
            self.player.money -= self.in_game_protocol.round_bid

        if player.responseAct == HandAct.RAISE:
            print("RAISE")
            player.bid = int(val)

            # new_bet = self.printRaiseMenu(self.in_game_protocol)
            # show message
            # player.bid = new_bet
            # self.player.money -= new_bet

        if player.responseAct == HandAct.BET or player.responseAct == HandAct.CALL:
            self.player.money -= self.in_game_protocol.round_bid
            player.bid = self.in_game_protocol.round_bid

        msg = self.in_game_protocol.create_message(ProtocolAct.GAME, player)
        self.send(msg)

    def send_player_response(self, act: HandAct, val: str):
        print("Player Action", act)
        self.player.responseAct = act
        if self.in_game_protocol.round_num == 1:
            self.player.bid = self.in_game_protocol.round_bid
            self.player.money -= self.in_game_protocol.round_bid

        if act == HandAct.RAISE:
            print("RAISE")
            self.player.bid += int(val)
            self.player.money -= int(val)
            # new_bet = self.printRaiseMenu(self.in_game_protocol)
            # show message
            # player.bid = new_bet
            # self.player.money -= new_bet

        if act == HandAct.BET or act == HandAct.CALL:
            self.player.money -= self.in_game_protocol.round_bid
            self.player.bid = self.in_game_protocol.round_bid

        msg = self.in_game_protocol.create_message(ProtocolAct.GAME, self.player)
        self.send(msg)

    def running_game1(self):
        try:
            # self.client_sock.connect(self.addr)

            # gameMsg = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            message: str = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = GameProtocol()
            pr.from_message(message)
            self.player = pr.your_hand

            if pr.game_status == GameStatus.INIT:
                send_msg = pr.create_message(ProtocolAct.GAME, self.player)
                self.send(send_msg)
                server_public_key_data = self.client_sock.recv(1024)
                self.server_public_key = rsa.PublicKey.load_pkcs1(server_public_key_data)
                print("key:", self.server_public_key)

            print("Receive player:" + str(self.player.id))
            self.player.password = 'CLIENT' + str(self.player.id)
            print("Waiting for starting game" + str(self.player.id))
            message = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = GameProtocol()
            pr.from_message(message)
            print("Game started" + str(pr.game_status))

            while pr.game_status == GameStatus.STARTED:

                print("Waiting for server ...")
                request = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
                pr = GameProtocol()
                pr.from_message(request)
                self.player = pr.your_hand
                self.flop = pr.flop
                self.screen.set_player_answer(None)
                self.screen.update_screen(pr.get_num_players() - 1)

                print(">>>>>>>>>>>>>>>>>")
                print("Round num:" + str(pr.round_num))
                print("Game jackpot:", pr.jackpot)
                print("My cards:" + str(pr.your_hand.cards))
                # print("Flop cards:" + str(gameMsg.getGame().get_flop()))
                othersAnswer = ""
                for pl in pr.players:
                    if pl.id != pr.your_hand.id:
                        othersAnswer += "Player " + str(pl.id) + " says " + str(pl.responseAct) + " ;"
                print("Other Players:" + othersAnswer)

                if pr.your_hand.responseAct == HandAct.FOLD:
                    break

                ans = None
                while True:
                    ans = self.screen.get_player_answer()
                    if ans != None:
                        self.screen.set_player_answer(None)
                        break

                player = pr.your_hand
                # res = self.printGameMenu(pr)
                player.responseAct = ans
                if pr.round_num == 1:
                    if player.responseAct != HandAct.FOLD:
                        player.bid = pr.round_bid
                        self.player.money -= pr.round_bid

                if player.responseAct == HandAct.RAISE:
                    new_bet = self.printRaiseMenu(pr)
                    player.bid = new_bet
                    self.player.money -= new_bet

                if player.responseAct == HandAct.BET or player.responseAct == HandAct.CALL:
                    self.player.money -= pr.round_bid
                    player.bid = pr.round_bid

                msg = pr.create_message(ProtocolAct.GAME, player)
                self.send(msg)

        except Exception as e:
            print(e)

    def initHand(self):
        try:
            self.client_sock.connect(self.addr)

            # gameMsg = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            message: str = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = GameProtocol()
            pr.from_message(message)
            self.player = pr.your_hand

            if pr.game_status == GameStatus.INIT:
                send_msg = pr.create_message(ProtocolAct.GAME, self.player)
                self.send(send_msg)
                server_public_key_data = self.client_sock.recv(1024)
                self.server_public_key = rsa.PublicKey.load_pkcs1(server_public_key_data)
                print("key:", self.server_public_key)

            print("Receive player:" + str(self.player.id))
            self.player.password = 'CLIENT' + str(self.player.id)
            print("Waiting for starting game" + str(self.player.id))
            message = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = GameProtocol()
            pr.from_message(message)
            print("Game started" + str(pr.game_status))

            while pr.game_status == GameStatus.STARTED:

                print("Waiting for server ...")
                request = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
                pr = GameProtocol()
                pr.from_message(request)
                self.flop = pr.flop
                print(">>>>>>>>>>>>>>>>>")
                print("Round num:" + str(pr.round_num))
                print("Game jackpot:", pr.jackpot)
                print("My cards:" + str(pr.your_hand.cards))
                # print("Flop cards:" + str(gameMsg.getGame().get_flop()))
                othersAnswer = ""
                for pl in pr.players:
                    if pl.id != pr.your_hand.id:
                        othersAnswer += "Player " + str(pl.id) + " says " + str(pl.responseAct) + " ;"
                print("Other Players:" + othersAnswer)

                if pr.your_hand.responseAct == HandAct.FOLD:
                    break

                res = self.printGameMenu(pr)
                player = pr.your_hand
                player.responseAct = res
                if pr.round_num == 1:
                    if player.responseAct != HandAct.FOLD:
                        player.bid = pr.round_bid
                        self.player.money -= pr.round_bid

                if player.responseAct == HandAct.RAISE:
                    new_bet = self.printRaiseMenu(pr)
                    player.bid = new_bet
                    self.player.money -= new_bet

                if player.responseAct == HandAct.BET or player.responseAct == HandAct.CALL:
                    self.player.money -= pr.round_bid
                    player.bid = pr.round_bid

                msg = pr.create_message(ProtocolAct.GAME, player)
                self.send(msg)

        except Exception as e:
            print(e)

    def printRaiseMenu(self, pr: GameProtocol):
        while True:
            user_input = input("Enter new bet:")
            return int(user_input)

    def printGameMenu(self, pr: GameProtocol):
        while True:
            if pr.round_status == HandAct.NO_DEF:
                print("Menu Options: fold (f), check (k), bet (b), call (l), raise (r)")
            elif pr.round_status == HandAct.BET:
                print("Menu Options: fold (f), call (l), raise (r)")
            elif pr.round_status == HandAct.RAISE:
                print("Menu Options: fold (f), call (l), raise (r)")
            else:
                print("Menu Options: fold (f), check (k), bet (b), call (l), raise (r)")

            # Get user input
            user_input = input("Enter a command: ")
            act = 'no_def'
            if user_input == 'f':
                act = 'fold'
            elif user_input == 'k':
                act = 'check'
            elif user_input == 'b':
                act = 'bet'
            elif user_input == 'l':
                act = 'call'
            elif user_input == 'r':
                act = 'raise'
            action = HandAct(act)
            print("User input:" + act)
            return action
            # # Define dictionary of commands
            # commands = {
            #     "help": lambda: print("This is the help message"),
            #     "quit": lambda: exit(),
            #     "conn": lambda: self.initHand(),
            #     "print": lambda: print("This is the print command"),
            #     # Add more commands as needed
            # }
            #
            # # Check if user input is a valid command
            # if user_input in commands:
            #     # Execute the command
            #     commands[user_input]()
            # else:
            #     print("Invalid command")

    def printMenu(self):
        while True:
            print("Menu Options: conn , ")
            # Get user input
            user_input = input("Enter a command: ")

            # Define dictionary of commands
            commands = {
                "help": lambda: print("This is the help message"),
                "quit": lambda: exit(),
                "conn": lambda: self.initHand(),
                "print": lambda: print("This is the print command"),
                # Add more commands as needed
            }

            # Check if user input is a valid command
            if user_input in commands:
                # Execute the command
                commands[user_input]()
            else:
                print("Invalid command")

    def printMenu1(self):
        print("Menu Options: conn , ")
        self.initHand()

    def sendLogin(self):
        self.send()

    def receiveMessage(self):
        is_ok = False
        pr = GameProtocol()
        while True:
            try:
                message: str = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
                pr.from_message(message)

                print("Receive data:", message)
                if pr.protocolAct == ProtocolAct.MESSAGE:
                    is_ok = pr.message.startswith("INFO")
                return (is_ok, pr.message)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    vtab = VHand("127.0.0.1")
    vtab.printMenu1()
