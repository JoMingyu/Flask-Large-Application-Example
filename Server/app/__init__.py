from flask import Flask
from flasgger import Swagger

from app.docs import TEMPLATE
from app.models import Mongo
from app.views import ViewInjector
from app.middleware import ErrorHandler, Logger

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


def create_app(config_name='dev'):
    """
    Creates Flask instance & initialize

    :rtype: Flask
    """
    config_path = '../config/{}.py'.format(config_name)
    # 인자로 config path를 통쨰로 넘겨주는 것보다 이상적

    app_ = Flask(__name__)
    app_.config.from_pyfile(config_path)

    swagger.init_app(app_)
    db.init_app(app_)
    view.init_app(app_)
    error_handler.init_app(app_)
    logger.init_app(app_)

    return app_


app = create_app()
