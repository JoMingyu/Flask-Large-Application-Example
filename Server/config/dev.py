from config import *

HOST = 'localhost'
ENDPOINT = '{0}:{1}'.format(HOST, PORT)
SWAGGER.update({'host': ENDPOINT})

TEST = True
DEBUG = True

MONGODB_SETTINGS = {
    'db': '{0}-dev'.format(SERVICE_NAME)
}
