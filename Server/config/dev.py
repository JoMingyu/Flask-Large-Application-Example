from config import Config


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 3000
    DEBUG = True

    Config.RUN.update({
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })

    Config.SWAGGER['host'] = '{}:{}'.format(Config.REPRESENTATIVE_HOST or HOST, PORT)
