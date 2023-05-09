
import pickle
import socket
import threading
from player import Player
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
            gameMsg =  pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            game = gameMsg.getGame()
            player = gameMsg.getPlayer()
            print("Receive player:" + str(player.id))
            player.password = 'CLIENT' + str(player.id)
            self.send(gameMsg);
            print("Waiting for starting game" + str(player.id))
            gameMsg = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
            game = gameMsg.getGame()
            print("Game started" + str(game.started))
            while (game.started == True):
                print("Waiting for server ...")
                gameMsg = pickle.loads(self.client_sock.recv(self.BUFFER_SIZE))
                game = gameMsg.getGame()
                print("Round num:" + str(game.round))
                print("My cards:" + str(gameMsg.getPlayer().cards))
                res = self.printGameMenu()
                player = gameMsg.getPlayer()
                player.response = res
                self.send(gameMsg)
        except Exception as e:
            print(e)

    def printGameMenu(self):
        while True:
            print("Menu Options: pass, raise" )
            # Get user input
            user_input = input("Enter a command: ")
            print("User input:" + user_input)
            return user_input
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
