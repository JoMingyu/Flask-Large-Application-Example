import base64


def base64_encode(str):
    return base64.b64encode(bytes(str, 'utf-8')).decode('utf-8')


def base64_decode(str):
    return base64.b64decode(bytes(str, 'utf-8')).decode('utf-8')

