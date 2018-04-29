import socket

from config import Config


class ProductionConfig(Config):
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 80
    DEBUG = False

    Config.RUN.update({
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })

    Config.SWAGGER['host'] = '{}:{}'.format(Config.REPRESENTATIVE_HOST or HOST, PORT)
