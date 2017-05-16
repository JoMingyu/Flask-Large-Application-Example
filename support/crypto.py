import base64
import hashlib


def base64_encode(s):
    return base64.b64encode(bytes(s, 'utf-8')).decode('utf-8')


def base64_decode(s):
    return base64.b64decode(bytes(s, 'utf-8')).decode('utf-8')


def sha512_encrypt(s):
    h = hashlib.sha512()
    h.update(s.encode('utf-8'))
    return h.hexdigest()
