import base64
import hashlib
import random

import rsa
import pickle

from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
class EncryptionTool:


    def __init__(self):
        self.id = 0
        self.BUFFER_SIZE = 1024
        (self.public_key, self.private_key) = rsa.newkeys(1024)
        self.public_key_data = self.public_key.save_pkcs1()



    def myfunc(self):
        print("Hello my name is " + str(self.id))
        original_obj = {'name': 'Alice', 'age': 25}
        print('Original object:', original_obj)

        # Encrypt object using RSA public key
        encrypted_bytes = self.encrypt(original_obj)
        print('encrypted_bytes:', encrypted_bytes)
        # Decrypt object using RSA private key
        decrypted_obj = self.decrypt(encrypted_bytes)
        print('Decrypted object:', decrypted_obj)




    def encrypt_rsa(self, obj):

        # print('public_key_data:', public_key_data)
        # Convert object to bytes using pickle
        obj_bytes = pickle.dumps(obj)
        # Encrypt bytes using RSA public key
        encrypted_bytes = rsa.encrypt(obj_bytes, self.public_key)
        return encrypted_bytes

    def decrypt_rsa(self, encrypted_bytes):
        # Decrypt bytes using RSA private key
        decrypted_bytes = rsa.decrypt(encrypted_bytes, self.private_key)
        # Convert bytes back to object using pickle
        obj = pickle.loads(decrypted_bytes)
        return obj


    def generate_aes_key(self):
        key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        return key
        # print ('key', [x for x in key])


    def test1(self):
        key = self.generate_aes_key()
        private_key = base64.b64decode(hashlib.sha256(key.encode("utf-8")).digest())
        # init_vector = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])

        iv = Random.new().read(AES.block_size)
        aes = AES.new(private_key, AES.MODE_CBC, iv)
        data = 'hello world 1234' # <- 16 bytes
        plain_text = pad(data)
        encd = aes.encrypt(plain_text)

        aes1 = AES.new(key, AES.MODE_CBC, iv)
        decd = aes1.decrypt(encd)
        print("decd:", decd)


if __name__ == '__main__':
    et = EncryptionTool()
    et.test1()