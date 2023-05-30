import rsa

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class RSACipher:
    def __init__(self, public_key, private_key):
        self.public_key = rsa.PublicKey.load_pkcs1(public_key)
        self.private_key = rsa.PrivateKey.load_pkcs1(private_key)

    def cipher(self, message):
        return rsa.encrypt(message.encode(), self.public_key)

    def decipher(self, ciphered_message):
        return rsa.decrypt(ciphered_message, self.private_key).decode()


class AESCipher:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, message):
        # Generate a random 16-byte initialization vector (IV)
        iv = algorithms.AES.generate_initialization_vector()

        # Create a new AES cipher with a random 256-bit key
        key = algorithms.AES.generate_key(bit_length=256)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

        # Pad the message using PKCS7 padding
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()

        # Encrypt the padded message
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()

        # Return the encrypted ciphertext, IV, and the AES key encrypted with the public key
        encrypted_key = self.public_key.encrypt(
            key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

        return ciphertext, iv, encrypted_key

    def decrypt(self, ciphertext, iv, encrypted_key):
        # Decrypt the AES key using the private key
        key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

        # Create an AES cipher with the decrypted key and IV
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

        # Decrypt the ciphertext
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpad the decrypted message
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()

        # Return the decrypted message
        return unpadded_message.decode()
