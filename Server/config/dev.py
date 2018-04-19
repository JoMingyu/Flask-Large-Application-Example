from config import Config


class DevConfig(Config):
    HOST = 'localhost'
    Config.SWAGGER['host'] = '{}:{}'.format(Config.REPRESENTATIVE_HOST or HOST, Config.PORT)

    DEBUG = True

    MONGODB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'db': '{}-dev'.format(Config.SERVICE_NAME)
    }
