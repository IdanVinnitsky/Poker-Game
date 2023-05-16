
import pickle
import socket
import threading

import rsa

from GameStatus import GameStatus
from HandAct import HandAct
from player import Player
from protocol import Protocol
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
        if self.server_public_key == None:
            self.send1(data)
            return

        try:
            obj_bytes = pickle.dumps(data)
            encrypted_data = rsa.encrypt(obj_bytes, self.server_public_key)
            self.client_sock.send(encrypted_data)
        except socket.error as e:
            print(str(e))

    def initHand(self):
        try:
            self.client_sock.connect(self.addr)

            # gameMsg = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            message: str = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = Protocol()
            pr.from_message(message)
            self.player = pr.your_hand
            if(pr.game_status == GameStatus.INIT):
                send_msg = pr.create_message(self.player)
                self.send(send_msg)
                server_public_key_data = self.client_sock.recv(1024)
                self.server_public_key = rsa.PublicKey.load_pkcs1(server_public_key_data)
                print("key:" , self.server_public_key)

            print("Receive player:" + str(self.player.id))
            self.player.password = 'CLIENT' + str(self.player.id)
            print("Waiting for starting game" + str(self.player.id))
            message = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = Protocol()
            pr.from_message(message)
            print("Game started" + str(pr.game_status))
            while (pr.game_status == GameStatus.STARTED):
                print("Waiting for server ...")
                request = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
                pr = Protocol()
                pr.from_message(request)

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

                msg = pr.create_message(player)
                self.send(msg)
        except Exception as e:
            print(e)


    def printRaiseMenu(self, pr: Protocol):
        while True:
            user_input = input("Enter new bet:")
            return int(user_input)

    def printGameMenu(self, pr: Protocol):
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
            print("Menu Options: conn , " )
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

if __name__ == '__main__':
    vtab = VHand("127.0.0.1")
    vtab.printMenu1()
