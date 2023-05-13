import pickle
import socket
import rsa

from EncryptionTool import EncryptionTool


class EncrClient:

    def __init__(self):
        self.id = 0
        self.public_key = None
        self.enc_tool: EncryptionTool = EncryptionTool()

    def myfunc(self):
        # Define TCP IP address and port
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((TCP_IP, TCP_PORT))

        # Receive the public key from the server
        public_key_data = client_socket.recv(1024)
        self.public_key = rsa.PublicKey.load_pkcs1(public_key_data)

        # Encrypt the data using the public key and send it to the server
        data = 'Hello, server!|'
        byte_data = bytes(data)
        obj_bytes = pickle.dumps(data + self.enc_tool.public_key_data)
        # encrypted_data = rsa.encrypt(obj_bytes,  self.public_key)
        client_socket.send(obj_bytes)

        # Close the connection
        client_socket.close()


if __name__ == '__main__':
    ec = EncrClient()
    ec.myfunc()
