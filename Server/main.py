from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import config as cf
import logger


def create_app(config_name):
    """
    Creates Flask instance & initialize
    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_object(cf.config[config_name])

    CORS(app)
    JWTManager(app)

    logger.decorate(app)

    from blueprints import all_blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app

_app = create_app('dev')


if __name__ == '__main__':
    _app.run(host=_app.config['HOST'], port=_app.config['PORT'], threaded=True)
