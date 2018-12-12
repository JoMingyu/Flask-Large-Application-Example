from flask import Flask
from werkzeug.exceptions import HTTPException

from app.misc.log import log


def register_extensions(flask_app: Flask):
    from app import extensions

    extensions.cors.init_app(flask_app)


def register_views(flask_app: Flask):
    from app.views import route

    handle_exception_func = flask_app.handle_exception
    handle_user_exception_func = flask_app.handle_user_exception
    # register_blueprint 시 defer되었던 함수들이 호출되며, flask-restful.Api._init_app()이 호출되는데
    # 해당 메소드가 app 객체의 에러 핸들러를 오버라이딩해서, 별도로 적용한 handler의 HTTPException 관련 로직이 동작하지 않음
    # 따라서 두 함수를 임시 저장해 두고, register_blueprint 이후 함수를 재할당하도록 함

    route(flask_app)

    flask_app.handle_exception = handle_exception_func
    flask_app.handle_user_exception = handle_user_exception_func


def register_hooks(flask_app: Flask):
    from app.hooks.error import broad_exception_handler, http_exception_handler
    from app.hooks.request_context import after_request

    flask_app.after_request(after_request)
    flask_app.register_error_handler(HTTPException, http_exception_handler)
    flask_app.register_error_handler(Exception, broad_exception_handler)


def create_app(*config_cls) -> Flask:
    log(message='Flask application initialized with {}'.format(', '.join([config.__name__ for config in config_cls])),
        keyword='INFO')
            
    flask_app = Flask(__name__)

    for config in config_cls:
        flask_app.config.from_object(config)

    register_extensions(flask_app)
    register_views(flask_app)
    register_hooks(flask_app)

    return flask_app
