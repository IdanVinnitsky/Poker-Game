import socket
import pickle
from player import Player


class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip  # IP of Idan's comp. you need to change the ip to your computer ip.
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = Player("name")
        self.p = self.connect()

    def get_client(self):
        return self.client

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(str(e))

