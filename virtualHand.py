import tkinter as tk
from pokerpage import PokerScreen

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
        self.public_key = None



    def connect(self):
        try:
            self.client_sock.connect(self.addr)
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client_sock.send(pickle.dumps(data))
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

            if pr.game_status == GameStatus.INIT:
                send_msg = pr.create_message(self.player)
                self.send(send_msg)
                public_key_data = self.client_sock.recv(1024)
                self.public_key = rsa.PublicKey.load_pkcs1(public_key_data)
                print("key:", self.public_key)

            print("Receive player:" + str(self.player.id))
            self.player.password = 'CLIENT' + str(self.player.id)
            # self.send(gameMsg)
            print("Waiting for starting game" + str(self.player.id))

            message = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            pr = Protocol()
            pr.from_message(message)
            print("Game started" + str(pr.game_status))

            while pr.game_status == GameStatus.STARTED:
                print("Waiting for server ...")
                request = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
                pr = Protocol()
                pr.from_message(request)
                # print("Round num:" + str(game.round))
                print("My cards:" + str(pr.your_hand.cards))
                # print("Flop cards:" + str(gameMsg.getGame().get_flop()))

                othersAnswer = ""
                for pl in pr.players:
                    if pl.id != pr.your_hand.id:
                        othersAnswer += "Player " + str(pl.id) + " says " + str(pl.responseAct) + " ;"
                print("Other Players:" + othersAnswer)
                res = self.printGameMenu()
                player = pr.your_hand
                player.responseAct = res
                msg = pr.create_message(player)
                self.send(msg)
        except Exception as e:
            print(e)

    def printGameMenu(self):
        while True:
            print("Menu Options: pass, raise" )
            # Get user input
            user_input = input("Enter a command: ")
            print("User input:" + user_input)
            return HandAct(user_input)
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
