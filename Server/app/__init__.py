from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from app.docs import TEMPLATE
from app.models import Mongo
from app.views import ViewInjector
from app.middleware import ErrorHandler, Logger

cors = CORS()
swagger = Swagger(template=TEMPLATE)

db = Mongo()
view = ViewInjector()
error_handler = ErrorHandler()
logger = Logger()


def create_app(dev=True):
    """
    Creates Flask instance & initialize

    :rtype: Flask
    """
    app_ = Flask(__name__)
    if dev:
        from config.dev import DevConfig
        app_.config.from_object(DevConfig)
    else:
        from config.production import ProductionConfig
        app_.config.from_object(ProductionConfig)

    cors.init_app(app_)
    swagger.init_app(app_)
    db.init_app(app_)
    view.init_app(app_)
    error_handler.init_app(app_)
    logger.init_app(app_)

    return app_


app = create_app()
