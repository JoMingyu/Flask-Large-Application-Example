import socket

from config import *

HOST = socket.gethostbyname(socket.gethostname())
ENDPOINT = '{0}:{1}'.format(HOST, PORT)
SWAGGER.update({'host': ENDPOINT})

TEST = False
DEBUG = False

MONGODB_SETTINGS = {
    'db': '{0}-production'.format(SERVICE_NAME)
}
