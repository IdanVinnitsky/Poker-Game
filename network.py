import socket
import pickle

BUFFER_SIZE = 4096


class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_client(self):
        return self.client

    def getP(self):
        return self.p

    def receive(self):
        return pickle.loads(self.client.recv(BUFFER_SIZE))

    def connect(self):
        global BUFFER_SIZE
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(BUFFER_SIZE))
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(str(e))

