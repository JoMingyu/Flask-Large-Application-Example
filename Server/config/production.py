import socket

from config import Config


class ProductionConfig(Config):
    HOST = socket.gethostbyname(socket.gethostname())

    if not Config.REPRESENTATIVE_HOST:
        Config.SWAGGER['host'] = '{}:{}'.format(HOST, Config.PORT)

    DEBUG = False

    MONGODB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'db': Config.SERVICE_NAME
    }
