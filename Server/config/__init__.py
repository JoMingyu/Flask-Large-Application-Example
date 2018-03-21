from datetime import timedelta
import os


class Config(object):
    REPRESENTATIVE_HOST = None
    PORT = 3000

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')
    # Secret key for any 3-rd party libraries
    SERVICE_NAME = 'Flask Large Application Example'

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)
    JWT_HEADER_TYPE = 'JWT'

    SWAGGER = {
        'title': SERVICE_NAME,
        'specs_route': '/docs/',
        'uiversion': 3,

        'info': {
            'title': SERVICE_NAME + ' API',
            'version': '1.0',
            'description': ''
        },

        'host': '{}:{}'.format(REPRESENTATIVE_HOST, PORT) if REPRESENTATIVE_HOST else None,
        'basePath': '/ '
    }
