import rsa


class RSACipher:
    def __init__(self, public_key, private_key):
        self.public_key = rsa.PublicKey.load_pkcs1(public_key)
        self.private_key = rsa.PrivateKey.load_pkcs1(private_key)

    def cipher(self, message):
        return rsa.encrypt(message.encode(), self.public_key)

    def decipher(self, ciphered_message):
        return rsa.decrypt(ciphered_message, self.private_key).decode()

