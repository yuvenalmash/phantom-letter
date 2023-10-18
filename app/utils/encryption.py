from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_key_pair(passphrase):
    key = RSA.generate(2048)
    encrypted_key = key.export_key(passphrase=passphrase, pkcs=8, protection="scryptAndAES128-CBC")
    return key, encrypted_key

def save_key_to_file(key, filename):
    with open(filename, 'wb') as file:
        file.write(key)

def load_key_from_file(filename, passphrase):
    with open(filename, 'rb') as file:
        key = RSA.import_key(file.read(), passphrase=passphrase)
        return key
    
def rsa_encrypt(public_key, message):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted_message).decode()

def rsa_decrypt(private_key, encrypted_message):
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode()