from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from app.models import Mongo
from app.views import Router

from config.dev import DevConfig
from config.production import ProductionConfig

WEB_FILE_ROOT_DIR = '../web_files'


def create_app(*config_cls):
    """
    Creates Flask instance & initialize

    Returns:
        Flask
    """
    print('[INFO] Flask application initialized with {}'.format(config_cls.__name__))

    app_ = Flask(
        __name__,
        # static_folder='{}/static'.format(WEB_FILE_ROOT_DIR),
        # template_folder='{}/templates'.format(WEB_FILE_ROOT_DIR)
    )

    for config in config_cls:
        app_.config.from_object(config)

    CORS().init_app(app_)
    JWTManager().init_app(app_)
    Swagger(template=app_.config['SWAGGER_TEMPLATE']).init_app(app_)
    Mongo().init_app(app_)
    Router().init_app(app_)

    return app_


app = create_app(DevConfig)
