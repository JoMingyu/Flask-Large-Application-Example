import socket

from config import Config


class ProductionConfig(Config):
    HOST = socket.gethostbyname(socket.gethostname())
    Config.SWAGGER['host'] = '{}:{}'.format(Config.REPRESENTATIVE_HOST or HOST, Config.PORT)

    DEBUG = False

    MONGODB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'db': Config.SERVICE_NAME
    }
