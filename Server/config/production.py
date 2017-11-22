import socket

from config.base import *

HOST = socket.gethostbyname(socket.gethostname())
SWAGGER_SETTINGS['API_DESC'] = SWAGGER_SETTINGS['API_DESC'].format(
    HOST,
    PORT
)

DEBUG = False

MONGODB_SETTINGS = {
    'db': 'sample.production',
    'host': 'localhost',
}
