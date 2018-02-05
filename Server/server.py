from argparse import ArgumentParser
import os

from app import app

if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        print('[WARN] SECRET KEY is not set in the environment variable.')

    parser = ArgumentParser()

    parser.add_argument('-p', '--port')
    args = parser.parse_args()

    app.run(host=app.config['HOST'], port=int(args.port) if args.port else app.config['PORT'], debug=app.debug, threaded=True)
