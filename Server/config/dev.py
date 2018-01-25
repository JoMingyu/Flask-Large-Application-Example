from config import Config


class DevConfig(Config):
    HOST = 'localhost'

    if not Config.DOMAIN:
        Config.SWAGGER.update({'host': '{}:{}'.format(HOST, Config.PORT)})

    DEBUG = True

    MONGODB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'db': '{}-dev'.format(Config.SERVICE_NAME)
    }
