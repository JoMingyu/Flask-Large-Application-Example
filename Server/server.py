import os

from app import app

if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        print('[WARN] SECRET KEY is not set in the environment variable.')

    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.debug, threaded=True)
