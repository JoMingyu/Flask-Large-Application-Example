from config import Config


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 3000

    Config.SWAGGER['host'] = '{}:{}'.format(Config.REPRESENTATIVE_HOST or HOST, PORT)

    DEBUG = True
