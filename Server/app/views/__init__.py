from functools import wraps
import gzip
import time

import ujson

from flask import Response, abort, after_this_request, g, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.exceptions import HTTPException


def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'

    return response


def exception_handler(e):
    print(e)

    if isinstance(e, HTTPException):
        description = e.description
        code = e.code
    elif isinstance(e, BaseResource.ValidationError):
        description = e.description
        code = 400
    else:
        description = ''
        code = 500

    return jsonify({
        'msg': description
    }), code


def gzipped(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            if 'gzip' not in request.headers.get('Accept-Encoding', '')\
                    or not 200 <= response.status_code < 300\
                    or 'Content-Encoding' in response.headers:
                # 1. Accept-Encoding에 gzip이 포함되어 있지 않거나
                # 2. 200번대의 status code로 response하지 않거나
                # 3. response header에 이미 Content-Encoding이 명시되어 있는 경우
                return response

            response.data = gzip.compress(response.data)
            response.headers.update({
                'Content-Encoding': 'gzip',
                'Vary': 'Accept-Encoding',
                'Content-Length': len(response.data)
            })

            return response
        return fn(*args, **kwargs)
    return wrapper


def auth_required(model):
    def decorator(fn):
        @wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            raise NotImplementedError()

            # return fn(*args, **kwargs)
        return wrapper
    return decorator


def json_required(required_keys, check_blank_str=True):
    def decorator(fn):
        if fn.__name__ == 'get':
            print('[WARN] JSON with GET method? on "{}()"'.format(fn.__qualname__))

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(406)

            for key, typ in required_keys.items():
                if key not in request.json or type(request.json[key]) is not typ:
                    abort(400)
                if check_blank_str and typ is str and not request.json[key]:
                    abort(400)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs) -> Response:
        return Response(
            ujson.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )

    class ValidationError(Exception):
        def __init__(self, description='', *args):
            self.description = description

            super(BaseResource.ValidationError, self).__init__(*args)


class Router:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.after_request(after_request)
        app.register_error_handler(Exception, exception_handler)

        from app.views import sample
        app.register_blueprint(sample.api.blueprint)
