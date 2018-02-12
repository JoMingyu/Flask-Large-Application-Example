from config import Config


class DevConfig(Config):
    HOST = 'localhost'

    if not Config.REPRESENTATIVE_HOST:
        Config.SWAGGER['host'] = '{}:{}'.format(HOST, Config.PORT)

    DEBUG = True

    MONGODB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'db': '{}-dev'.format(Config.SERVICE_NAME)
    }
