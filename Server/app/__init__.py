from argparse import ArgumentParser

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from app.docs import TEMPLATE
from app.models import Mongo
from app.views import ViewInjector
from app.middleware import ErrorHandler, Logger

cors = CORS()
# To Swagger, or Support AJAX

swagger = Swagger(template=TEMPLATE)
# To Swagger UI

db = Mongo()
# To Control MongoDB

view = ViewInjector()
# To Swagger Documentation

error_handler = ErrorHandler()
# To handler 4xx, 5xx errors

logger = Logger()
# To log in every context of Flask


def create_app(config_name):
    """
    Creates Flask instance & initialize

    :rtype: Flask
    """
    app_ = Flask(__name__)
    app_.config.from_pyfile(config_name)

    cors.init_app(app_)
    swagger.init_app(app_)
    db.init_app(app_)
    view.init_app(app_)
    error_handler.init_app(app_)
    logger.init_app(app_)

    return app_

parser = ArgumentParser('Arguments to set configs for server')
parser.add_argument('-c', '--config', required=True, help='Type of config(d : dev/p : production)')
parser.add_argument('-p', '--port', help='Port which the server will operate', type=int)
args = parser.parse_args()

assert args.config == 'd' or args.config == 'p'

if args.config == 'd':
    app = create_app('../config/dev.py')
else:
    app = create_app('../config/production.py')

if args.port:
    app.config['PORT'] = args.port
