from flask import Flask
from flask_cors import CORS

from middleware import Logger
from app.models import Mongo

cors = CORS()
# To Swagger, or Support AJAX

logger = Logger()
# To log in every context of Flask

db = Mongo()
# To Control MongoDB


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
    logger.init_app(app_)
    db.init_app(app_)

    return app_

app = create_app('../config/dev.py')
