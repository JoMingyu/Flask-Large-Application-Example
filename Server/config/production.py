import socket

from config import *

HOST = socket.gethostbyname(socket.gethostname())

TEST = False
DEBUG = False

MONGODB_SETTINGS = {
    'db': '{0}-production'.format(SERVICE_NAME)
}
