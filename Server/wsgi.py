import os

from app import create_app
from config import Config, RemoteDBConfig

application = create_app(Config, RemoteDBConfig)

if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        print('[WARN] SECRET KEY is not set in the environment variable.')

    application.run()
