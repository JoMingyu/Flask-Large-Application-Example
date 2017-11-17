from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

from blueprints import Blueprints
from logger import Logger

cors = CORS()
# To Swagger, or Support AJAX

jwt = JWTManager()
# To JWT Authentication

db = MongoEngine()
# To Control MongoDB

blueprints = Blueprints()

logger = Logger()
# To log in every context of Flask


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
    jwt.init_app(app_)
    db.init_app(app_)
    blueprints.init_app(app_)
    logger.init_app(app_)

    return app_

app = create_app('../config/development.py')
