import socket

from config import Config


class ProductionConfig(Config):
    HOST = socket.gethostbyname(socket.gethostname())

    if not Config.DOMAIN:
        Config.SWAGGER.update({'host': '{}:{}'.format(HOST, Config.PORT)})

    DEBUG = False

    MONGODB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'db': '{}-production'.format(Config.SERVICE_NAME)
    }
