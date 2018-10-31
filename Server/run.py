import os

from app import create_app
from config import Config, LocalDBConfig
from app.misc.logger import logger

app = create_app(Config, LocalDBConfig)

if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        logger(message='SECRET KEY is not set in the environment variable.',
               type='WARN')

    app.run(**app.config['RUN_SETTING'])
