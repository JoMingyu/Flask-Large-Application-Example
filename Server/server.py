from argparse import ArgumentParser
import os

from app import app

if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        print('[WARN] SECRET KEY is not set in the environment variable.')

    parser = ArgumentParser('해당 Flask 어플리케이션이 동작하기 위해 필요한 설정 값들을 다루기 위한 Argument Parser입니다.')

    parser.add_argument('-p', '--port')
    args = parser.parse_args()

    app.run(host=app.config['HOST'], port=int(args.port) if args.port else app.config['PORT'], debug=app.debug, threaded=True)
