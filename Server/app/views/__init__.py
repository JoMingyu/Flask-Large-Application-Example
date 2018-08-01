from functools import wraps
import json
import time

from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.exceptions import HTTPException


def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'

    return response


def auth_required(model):
    def decorator(fn):
        @wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            raise NotImplementedError()

            # return fn(*args, **kwargs)
        return wrapper
    return decorator


class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs) -> Response:
        return Response(
            json.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )

    class ValidationError(Exception):
        def __init__(self, description='', *args):
            self.description = description

            super(BaseResource.ValidationError, self).__init__(*args)


def _register_error_handlers(blueprint):
    from app import error_handlers

    blueprint.register_error_handler(HTTPException, error_handlers.http_exception_handler)
    blueprint.register_error_handler(BaseResource.ValidationError, error_handlers.validation_error_handler)
    blueprint.register_error_handler(Exception, error_handlers.broad_exception_error_handler)


def load_api():
    from app.views import sample


def route(app):
    from app import api_v1_blueprint

    _register_error_handlers(api_v1_blueprint)
    api_v1_blueprint.after_request(after_request)

    load_api()

    handle_exception_func = app.handle_exception
    handle_user_exception_func = app.handle_user_exception
    # register_blueprint 시 defer되었던 함수들이 호출되며, flask-restful.Api._init_app()이 호출되는데
    # 해당 메소드가 app 객체의 에러 핸들러를 오버라이딩해서, 별도로 적용한 handler의 HTTPException 관련 로직이 동작하지 않음
    # 따라서 두 함수를 임시 저장해 두고, register_blueprint 이후 함수를 재할당하도록 함

    app.register_blueprint(api_v1_blueprint)
    app.handle_user_exception = handle_exception_func
    app.handle_user_exception = handle_user_exception_func
