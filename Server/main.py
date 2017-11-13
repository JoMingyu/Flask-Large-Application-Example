from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
# from flask_sqlalchemy import SQLAlchemy

import config as cf
from logger import Logger

cors = CORS()
jwt = JWTManager()
db = MongoEngine()
# db = SQLAlchemy()
logger = Logger()


def create_app(config_name):
    """
    Creates Flask instance & initialize
    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_object(cf.config[config_name])

    cors.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    logger.init_app(app)

    from blueprints import all_blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app

_app = create_app('dev')


if __name__ == '__main__':
    _app.run(host=_app.config['HOST'], port=_app.config['PORT'], threaded=True)
