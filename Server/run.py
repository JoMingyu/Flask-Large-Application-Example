import os

from app import create_app
from config import Config, LocalDBConfig

app = create_app(Config, LocalDBConfig)

if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        print('[WARN] SECRET KEY is not set in the environment variable.')

    app.run(**app.config['RUN_SETTING'])
