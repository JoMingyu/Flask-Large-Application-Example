from config.base import *

HOST = 'localhost'
SWAGGER.update({'host': '{0}:{1}'.format(HOST, PORT)})

DEBUG = True

MONGODB_SETTINGS = {
    'db': '{0}-dev'.format(SERVICE_NAME),
    'host': 'localhost',
}
