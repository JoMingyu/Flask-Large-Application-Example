from argparse import ArgumentParser
import os

from app import create_app

from config.dev import DevConfig
from config.production import ProductionConfig

if __name__ == '__main__':
    app = create_app(ProductionConfig)

    if 'SECRET_KEY' not in os.environ:
        print('[WARN] SECRET KEY is not set in the environment variable.')

    parser = ArgumentParser('해당 Flask 어플리케이션이 동작하기 위해 필요한 설정 값들을 다루기 위한 Argument Parser입니다.')

    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()

    app.run(host=app.config['HOST'], port=args.port or app.config['PORT'], debug=app.debug, threaded=True)
