from EncryptionTool import EncryptionTool
import socket

class EncServer:


    def __init__(self):
        self.id = 0
        self.enc_tool: EncryptionTool = EncryptionTool()

    def myfunc(self):
        # Define TCP IP address and port
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005

        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_socket.bind((TCP_IP, TCP_PORT))

        # Listen for incoming connections
        server_socket.listen(1)

        # Wait for a connection
        print('Waiting for a connection...')
        client_socket, addr = server_socket.accept()
        print('Connection address:', addr)

        # Send the public key to the client
        # public_key_data = public_key.save_pkcs1()
        client_socket.send(self.enc_tool.public_key_data)

        # Receive the encrypted data from the client and decrypt it
        data = client_socket.recv(1024)
        decrypted_data = self.enc_tool.decrypt(data)
        print('Received data:', decrypted_data)

        # Close the connection
        client_socket.close()
        server_socket.close()




if __name__ == '__main__':
    es = EncServer()
    es.myfunc()