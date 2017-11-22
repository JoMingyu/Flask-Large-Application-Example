from config.base import *

HOST = 'localhost'
SWAGGER_SETTINGS['API_DESC'] = SWAGGER_SETTINGS['API_DESC'].format(
    HOST,
    PORT
)

DEBUG = True

MONGODB_SETTINGS = {
    'db': 'sample.dev',
    'host': 'localhost',
}
