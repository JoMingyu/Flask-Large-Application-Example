from flask import Blueprint, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from redis import Redis

from mongoengine import connect

from app.views import route

api_v1_blueprint = Blueprint('api', __name__)


def create_app(*config_cls) -> Flask:
    print('[INFO] Flask application initialized with {}'.format([config.__name__ for config in config_cls]))

    app_ = Flask(__name__)

    for config in config_cls:
        app_.config.from_object(config)

    CORS().init_app(app_)
    JWTManager().init_app(app_)
    Swagger(template=app_.config['SWAGGER_TEMPLATE']).init_app(app_)

    connect(**app_.config['MONGODB_SETTINGS'])
    app_.config['REDIS_CLIENT'] = Redis(**app_.config['REDIS_SETTINGS'])

    route(app_)

    return app_
