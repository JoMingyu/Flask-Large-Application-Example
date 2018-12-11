import os

from app import create_app
from app.misc.log import log
from config import Config, LocalDBConfig

app = create_app(Config, LocalDBConfig)

if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        log(message='SECRET KEY is not set in the environment variable.',
            keyword='WARN')

    app.run(**app.config['RUN_SETTING'])
