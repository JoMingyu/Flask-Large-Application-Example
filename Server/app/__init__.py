from flask import Flask
from flask_cors import CORS

from middleware import ErrorHandler, Logger
from app.models import Mongo
from app.views import Swagger

cors = CORS()
# To Swagger, or Support AJAX

error_handler = ErrorHandler()

logger = Logger()
# To log in every context of Flask

db = Mongo()
# To Control MongoDB

swagger = Swagger()
# To Swagger Documentation


def create_app(config_name):
    """
    Creates Flask instance & initialize

    Came from 'Use Application Factory' : http://slides.skien.cc/flask-hacks-and-best-practices/#7

    :rtype: Flask
    """
    app_ = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )
    app_.config.from_pyfile(config_name)

    cors.init_app(app_)
    error_handler.init_app(app_)
    logger.init_app(app_)
    db.init_app(app_)
    swagger.init_app(app_)

    return app_

app = create_app('../config/dev.py')
