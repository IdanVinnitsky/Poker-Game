import rsa
import pickle

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





if __name__ == '__main__':
    et = EncryptionTool()
    et.myfunc()