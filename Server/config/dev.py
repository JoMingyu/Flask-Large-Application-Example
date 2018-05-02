from config import Config


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 5000
    DEBUG = True

    RUN = dict(Config.RUN, **{
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })

    Config.SWAGGER['host'] = '{}:{}'.format(Config.REPRESENTATIVE_HOST or HOST, PORT)
