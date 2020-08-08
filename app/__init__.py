from flask import Flask
from werkzeug.exceptions import HTTPException

from app.misc.log import log


def register_extensions(flask_app: Flask):
    from app import extensions

    extensions.cors.init_app(flask_app)


def register_views(flask_app: Flask):
    from app.views import route

    route(flask_app)


def register_hooks(flask_app: Flask):
    from app.hooks.error import broad_exception_handler
    from app.hooks.request_context import after_request

    flask_app.after_request(after_request)
    flask_app.register_error_handler(Exception, broad_exception_handler)


def create_app(*config_cls) -> Flask:
    config_cls = [
        config() if isinstance(config, type) else config for config in config_cls
    ]

    log(
        message="Flask application initialized with {}".format(
            ", ".join([config.__class__.__name__ for config in config_cls])
        ),
        keyword="INFO",
    )

    flask_app = Flask(__name__)

    for config in config_cls:
        flask_app.config.from_object(config)

    register_extensions(flask_app)
    register_views(flask_app)
    register_hooks(flask_app)

    return flask_app
