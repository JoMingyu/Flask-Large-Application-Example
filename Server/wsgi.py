import os

from app import create_app
from config import Config, RemoteDBConfig
from app.misc.log import log

application = create_app(Config, RemoteDBConfig)

if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        log(message='SECRET KEY is not set in the environment variable.',
            keyword='WARN')

    application.run()
