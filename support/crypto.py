import base64
import hashlib


def base64_encode(str):
    return base64.b64encode(bytes(str, 'utf-8')).decode('utf-8')


def base64_decode(str):
    return base64.b64decode(bytes(str, 'utf-8')).decode('utf-8')


def sha512_encrypt(str):
    h = hashlib.sha512()
    h.update(str.encode('utf-8'))
    return h.hexdigest()
