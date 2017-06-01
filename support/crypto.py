from cryptography.fernet import Fernet
import hashlib

key = b'wWX4VyWSzKifCA-kZ_9j4y9LjRc5iGxVH_6AgDUBQXs='


def fernet_encrypt(s):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(s.encode('utf-8')).decode('utf-8')


def fernet_decrypt(s):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(s.encode('utf-8')).decode('utf-8')


def sha512_encrypt(s):
    h = hashlib.sha512()
    h.update(s.encode('utf-8'))
    return h.hexdigest()


def generate_key():
    print(Fernet.generate_key())

